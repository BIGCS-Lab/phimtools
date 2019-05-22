"""Run functions by provided a name with arguments.

Author: Shujia Huang
Date: 2019-05-22
"""
from pi.modules.imputation import minimac as minimac_impute


def imputation(kwargs, config):
    """Run imputation for VCF files"""

    # Todo: options parameter is not been used. Think about it!
    # Todo: we need multiple methods for impute and pre-phase
    if kwargs.methods == "minimac":
        minimac_impute(config,
                       kwargs.in_vcf,
                       kwargs.out_prefix,
                       nCPU=kwargs.nCPU,
                       reference_panel=kwargs.refpanel,
                       reference_version=kwargs.refbuild,
                       merge_multi_output=True,
                       is_prephase=True)

    return
