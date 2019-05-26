"""A program for imputation process.

Author: Shujia Huang
Date: 2019-05-22
"""
from pi.tools.minimac3 import Minimac
from pi.log import Log


def minimac(config, input_file, output_prefix, region, reference_panel=None, options=None):
    """Impute for a single chromosome.

    Parameters:
        ``region``: chr_id:start-end
            A genome region for imputation
        ``reference_version``: A string.
                set reference version for phasing process
        ``options``: A tuple list of eagle parameters
    """
    Log.info("Performing imputation process for %s by using Minimac3." % region)
    if options is None:
        options = []

    out_impute_vcf = "%s.dose.vcf.gz" % output_prefix
    out_impute_rec = "%s.rec" % output_prefix
    out_impute_erate = "%s.erate" % output_prefix
    out_impute_info = "%s.info" % output_prefix

    minimac = Minimac(config, reference_panel=reference_panel)

    cmd_options = options + [("--haps", input_file), ("--prefix", output_prefix)]
    is_good = minimac.run(region, cmd_options)

    if is_good:
        return [out_impute_vcf, out_impute_rec, out_impute_erate, out_impute_info]
    else:
        return

