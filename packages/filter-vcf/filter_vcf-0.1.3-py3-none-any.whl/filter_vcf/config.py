"""
  config

  routines to define and parse arguments
"""

import argparse

parser = argparse.ArgumentParser(
    description="Invoke vt/bedtools etc for manipulating vcf variant file."
)

subparsers = parser.add_subparsers(dest="command", help="command selection")
subparsers.required = True

# cmd: vt-combo
parser_vtcombo = subparsers.add_parser(
    "vt-combo", help="apply a series of decomposition, normalization, filter-unique steps"
)
parser_vtcombo.add_argument(
    "-d",
    "--notDecompose",
    action="store_true",
    help="Flag to skip splitting multiple alternative alleles to separate variant records. Default is to split",
)
parser_vtcombo.add_argument(
    "-n",
    "--notNormalize",
    action="store_true",
    help="Flag to skip normalizing. Default is to normalize the representation",
)
parser_vtcombo.add_argument(
    "-q",
    "--notUniq",
    action="store_true",
    help="Flag to skip filtering to unique set of variants. Default is to drop variants appearing later in the file",
)
parser_vtcombo.add_argument(
    "-r", "--reference", required=True, help="Reference genome file or directory"
)
parser_vtcombo.add_argument(
    "-i",
    "--input",
    required=True,
    action="append",
    help="Input vcf file (.vcf or .vcf.gz).  If multiple files are specified, they will be combined.",
)
parser_vtcombo.add_argument(
    "-o", "--output", required=False, help="Output vcf file (.vcf. or .vcf.gz)"
)
parser_vtcombo.add_argument(
    "-c", "--filterContig", action="store_true", help="Filters out unsupported contigs from the vcf"
)
parser_vtcombo.add_argument(
    "-t",
    "--notDepth",
    action="store_true",
    help="Not to calculate DP depth from summing the AD genotype field. Default is to add DP.",
)
parser_vtcombo.add_argument(
    "-f",
    "--userFilter",
    action="append",
    help="List of user specified FILTER labels to keep other than PASS",
)
