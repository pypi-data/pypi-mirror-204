import numpy as np
from logging import Logger
from natsort import index_natsorted
from fuc import pyvcf


def sort_vcf(vcf_frame: pyvcf.VcfFrame, log: Logger) -> str:
    # Perform natural sort on CHROM, POS, REF, and ALT columns
    if isinstance(vcf_frame, str):
        vcf_frame = pyvcf.VcfFrame.from_string(vcf_frame)

    vcf_frame.df.sort_values(
        by=["CHROM", "POS", "REF", "ALT"],
        key=lambda x: np.argsort(
            index_natsorted(
                zip(
                    vcf_frame.df["CHROM"],
                    vcf_frame.df["POS"],
                    vcf_frame.df["REF"],
                    vcf_frame.df["ALT"],
                )
            )
        ),
        inplace=True,
        ignore_index=True,
    )

    return vcf_frame.to_string()
