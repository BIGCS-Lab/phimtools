"""Run functions by provided a name with arguments.

Author: Shujia Huang
Date: 2019-05-22
"""
import sys

from pitools.modules.phasing import eagle_region
from pitools.modules.imputation import minimac
from pitools.utils import merge_files
from pitools.modules import get_chromlist
from pitools.log import Log


def imputation(kwargs, config):
    """Run imputation for VCF files
    """
    if kwargs.impute_method not in ["minimac"]:
        Log.error("%s is not one of imputation method in pitools pipeline." % kwargs.impute_method)
        sys.exit(1)

    if kwargs.phase_method not in ["eagle"]:
        Log.error("%s is not one of phasing method in pitools pipeline." % kwargs.phase_method)
        sys.exit(1)

    if not kwargs.in_vcf.endswith(".vcf.gz") and not kwargs.in_vcf.endswith(".vcf"):
        Log.error("The format of input file is not a *.vcf.gz or *.vcf\n")
        sys.exit(1)

    if not kwargs.regions:
        regions = get_chromlist(kwargs.in_vcf)
    else:
        regions = kwargs.regions.split(",")

    out_impute_files = []
    # perform for each chromosome or genome region
    for reg in regions:

        # ignore the chromosome which not in the reference panel, which may happen in chromosome X
        chr_id = reg.split(":")[0]
        if chr_id not in config[kwargs.impute_method]["reference_panel"][kwargs.refpanel]:
            Log.warn("[WARNING] chromosome %s is not in the panel: %s, which will not been "
                     "imputed in your final result.\n" % (chr_id, kwargs.refpanel))
            continue

        sub_outprefix = "%s.%s" % (kwargs.out_prefix, reg.replace(":", "-"))
        phased_file = kwargs.in_vcf
        if not kwargs.is_unprephase:
            # pre-phasing
            Log.info("Performing pre-phasing process before imputation.")
            if kwargs.phase_method == "eagle":
                phased_file = eagle_region(config,
                                           kwargs.in_vcf,
                                           kwargs.out_prefix + ".phased",
                                           reg,
                                           reference_version=kwargs.refbuild,
                                           options=[("numThreads", kwargs.nCPU)])
            else:
                Log.warn("Nothing output")
                return

            if not phased_file:
                continue

        if kwargs.impute_method == "minimac":
            sub_out_impute_files = minimac(config,
                                           phased_file,
                                           sub_outprefix,
                                           reg,
                                           reference_panel=kwargs.refpanel,
                                           options=[("cpus", kwargs.nCPU)])
            if sub_out_impute_files:
                out_impute_files.append(sub_out_impute_files)

    # Todo: Merge different kinds of output files
    final_out_impute_file = "%s.final.vcf.gz" % kwargs.out_prefix
    if out_impute_files:
        # Just merge the imputed VCF files
        merge_files([f[0] for f in out_impute_files], final_out_impute_file,
                    is_del_raw_file=True)

        return final_out_impute_file
    else:
        Log.warn("Nothing output")
        return
