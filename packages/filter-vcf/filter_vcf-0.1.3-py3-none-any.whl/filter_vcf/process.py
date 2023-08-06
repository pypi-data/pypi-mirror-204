import logging
import sys
import subprocess
import re
import os
import shutil
import uuid
from fuc import pyvcf
from lifeomic_logging import scoped_logger

from filter_vcf.util.userFilter import filter_vcf
from filter_vcf.util.readVcf import read_vcf
from filter_vcf.util.writeVcf import write_vcf
from filter_vcf.util.sortVcf import sort_vcf
from filter_vcf.util.addDepth import add_depth
from filter_vcf.util.cleanAD import clean_ad
from filter_vcf.util.cleanGT import clean_gt
from filter_vcf.util.removeNonRef import filter_non_ref
from filter_vcf.util.detectVcf import detect_vcf
from filter_vcf.util.convertChrName import convert_chr_name
from filter_vcf.util.unique import keep_unique_variants
from filter_vcf import config


def normalize_vcf():
    with scoped_logger(__name__) as log:
        args = config.parser.parse_args()
        print("Args: " + str(sys.argv))
        tmpDir = f"/tmp/normalize_vcf_{str(uuid.uuid4().hex)[:16]}"
        os.makedirs(f"{tmpDir}/ref/")

        if args.command == "vt-combo":
            ops_trigger = False
            compress_var = False

            print(args)

            # adding the option of a temporary '.tcf' file for when we are
            # working with an intermediary vcf
            if not args.output and len(args.input) == 1:
                if args.input[0].endswith((".vcf", ".vcf.gz")):
                    setattr(args, "output", args.input[0].replace(".vcf", ".nrm.vcf"))
                elif args.input[0].endswith((".tcf", ".tcf.gz")):
                    setattr(args, "output", args.input[0].replace(".tcf", ".nrm.vcf"))
            if args.output.endswith(".gz"):
                compress_var = True

            fileName = re.sub(" ", "", re.sub(r".*/", "", args.input[0]))
            inFile = tmpDir + "/" + fileName
            outFile = (
                tmpDir + "/out-" + re.sub(r"\..*", ".gz", fileName)
                if args.output.endswith(".gz")
                else tmpDir + "/out-" + re.sub(r"\..*", "", fileName)
            )
            vcf_in = read_vcf(args.input[0], log)
            sorted_vcf = sort_vcf(vcf_in, log)
            write_vcf(vcf_in=sorted_vcf, vcf_out=inFile, compression=compress_var, log=log)

            if os.path.isfile(args.reference):
                if args.reference.endswith("37.fa.gz"):
                    refFile = tmpDir + "/ref/GRCh37.fa.gz"
                    shutil.copyfile(f"{args.reference}", f"{tmpDir}/ref/GRCh37.fa.gz")
                elif args.reference.endswith("38.fa.gz"):
                    refFile = tmpDir + "/ref/GRCh38.fa.gz"
                    shutil.copyfile(f"{args.reference}", f"{tmpDir}/ref/GRCh38.fa.gz")
                else:
                    print(
                        "ERROR: genome reference .fa.gz must be GRCh38 or GRCh37. Given: "
                        + args.reference
                    )
                    sys.exit(3)
            else:
                print("ERROR: genome reference .fa.gz file not found: " + args.reference)
                sys.exit(3)

            if args.filterContig:
                if not inFile.endswith(".gz"):
                    subprocess.run(f"bgzip {inFile}", shell=True, check=True)
                    inFile = inFile + ".gz"
                subprocess.run(f"tabix -p vcf {inFile}", shell=True, check=True)
                regions = ",".join(
                    ["chr" + str(i) for i in range(1, 23)]
                    + [str(i) for i in range(1, 23)]
                    + ["X", "Y", "M", "MT", "chrX", "chrY", "chrM", "chrMT"]
                )
                subprocess.run(
                    f'bcftools view  -r "{regions}" {inFile} -o {tmpDir}/regions.vcf.gz -O z ',
                    shell=True,
                    check=True,
                )
                os.rename(f"{tmpDir}/regions.vcf.gz", inFile)
                ops_trigger = True

            # Always performed
            working_vcf = read_vcf(inFile, log).to_string()

            if not args.notDepth:
                working_vcf = add_depth(working_vcf, log)
                ops_trigger = True

            if not args.notDecompose:
                write_vcf(working_vcf, outFile, compress_var, log)
                subprocess.run(
                    f"vt decompose -s {inFile} -o {tmpDir}/decomposed.vcf", shell=True, check=True
                )
                os.system(f"gzip {tmpDir}/decomposed.vcf")
                os.rename(f"{tmpDir}/decomposed.vcf.gz", inFile)
                working_vcf = read_vcf(inFile, log).to_string()
                working_vcf = clean_gt(working_vcf, log)
                working_vcf = clean_ad(working_vcf, log)
                ops_trigger = True

            # Always performed
            working_vcf = filter_non_ref(working_vcf, log)

            if not args.notNormalize:
                vcfChr = detect_vcf(working_vcf, log)
                print("INFO: input vcf file <" + inFile + "> has type <" + vcfChr + ">")

                if vcfChr == "chr" and "GRCh37" in args.reference:
                    working_vcf = convert_chr_name(working_vcf, "num", log)
                    write_vcf(working_vcf, inFile, True, log)
                    subprocess.run(
                        f"vt normalize -n -r {refFile} {inFile} -o {tmpDir}/normalized.vcf",
                        shell=True,
                        check=True,
                    )
                    os.system(f"gzip {tmpDir}/normalized.vcf")
                    os.rename(f"{tmpDir}/normalized.vcf.gz", inFile)
                    working_vcf = read_vcf(inFile, log).to_string()
                    working_vcf = convert_chr_name(working_vcf, "chr", log)

                else:
                    write_vcf(working_vcf, inFile, True, log)
                    subprocess.run(
                        f"vt normalize -n -r {refFile} {inFile} -o {tmpDir}/normalized.vcf",
                        shell=True,
                        check=True,
                    )
                    os.system(f"gzip {tmpDir}/normalized.vcf")
                    os.rename(f"{tmpDir}/normalized.vcf.gz", inFile)
                    working_vcf = read_vcf(inFile, log).to_string()
                ops_trigger = True

            # Always performed
            working_vcf = sort_vcf(working_vcf, log)

            if not args.notUniq:
                working_vcf = keep_unique_variants(working_vcf, log)
                ops_trigger = True

            if args.userFilter:
                working_vcf = filter_vcf(working_vcf, ":".join(args.userFilter), log)

            if ops_trigger == True:
                write_vcf(working_vcf, args.output, compress_var, log)
            else:
                print("WARN: vt-combo no operation selection")
        else:
            print("WARN: unknown selection")


if __name__ == "__main__":
    normalize_vcf()
