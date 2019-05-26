"""Run functions by provided a name with arguments.

Author: Shujia Huang
Date: 2019-05-22
"""
import sys

from pi.modules.phasing import eagle_chromosome
from pi.modules.imputation import minimac
from pi.utils import merge_files
from pi.modules import get_chromlist
from pi.log import Log


def imputation(kwargs, config, is_prephase=True):
    """Run imputation for VCF files
    """
    if kwargs.impute_mehtod not in ["minimac"]:
        Log.error("%s is not one of imputation method in pi pipeline." % kwargs.impute_mehtod)
        sys.exit(1)

    if not kwargs.in_vcf.endswith(".vcf.gz") and not kwargs.in_vcf.endswith(".vcf"):
        Log.error("The format of input file is not a *.vcf.gz or *.vcf\n")
        sys.exit(1)

    chromosomes = get_chromlist(kwargs.in_vcf)
    out_impute_files = []

    # perform for each chromosome or genome region
    for chr_id in chromosomes:

        # ignore the chromosome which not in the reference panel, which may happen in chromosome X
        if chr_id not in config["minimac"]["reference_panel"][kwargs.refpanel]:
            Log.warn("[WARNING] chromosome %s is not in the panel: %s, which will not been "
                     "imputed in your final result.\n" % (chr_id, kwargs.refpanel))
            continue

        sub_outprefix = "%s.%s" % (kwargs.out_prefix, chr_id)
        phased_file = kwargs.in_vcf
        if is_prephase:
            # pre-phasing
            Log.info("Performing pre-phasing process by imputation.")
            phased_file = eagle_chromosome(config,
                                           kwargs.in_vcf,
                                           kwargs.out_prefix + ".phased",
                                           chr_id,
                                           reference_version=kwargs.refbuild,
                                           options=[("--numThreads", kwargs.nCPU)])

        if kwargs.impute_method == "minimac":
            sub_out_impute_files = minimac(config,
                                           phased_file,
                                           sub_outprefix,
                                           chr_id,
                                           reference_panel=kwargs.refpanel,
                                           options=[("--cpus", kwargs.nCPU)])
            if sub_out_impute_files:
                out_impute_files.append(sub_out_impute_files)

    # Todo: Merge different kinds of output files
    final_out_impute_file = "%s.final.vcf.gz" % kwargs.out_prefix
    merge_files([f[0] for f in out_impute_files], final_out_impute_file,
                is_del_raw_file=True)

    return final_out_impute_file
