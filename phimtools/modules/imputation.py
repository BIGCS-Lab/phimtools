"""A program for imputation process.

Author: Shujia Huang
Date: 2019-05-22
"""
from phimtools.tools.minimac3 import Minimac
from phimtools.log import Log


def minimac(config, input_file, output_prefix, region, reference_panel=None, options=None):
    """Impute for a single chromosome.

    Parameters:
        ``region``: chr_id:start-end
            A genome region for imputation
        ``reference_panel``: A string.
                set reference panel for imputation process, must be the same name
                in configuration file.
        ``options``: A tuple list of eagle parameters
    """
    region = str(region)

    Log.info("Performing imputation process for %s by using Minimac3." % region)
    if options is None:
        options = []

    # set parameter as a key-world pair.
    minimac_param_kw = {k: v for k, v in options}
    minimac_param_kw["haps"] = input_file
    minimac_param_kw["prefix"] = output_prefix

    genome_region = region.split(":")
    chr_id = genome_region[0]
    if chr_id not in config["minimac"]["reference_panel"][reference_panel]:
        Log.warn("[WARNING] The reference panel does not contain chromosome %s, "
                 "imputation process stopped for this chromosome.\n" % chr_id)
        return

    # set the region for Minimac
    minimac_param_kw["chr"] = chr_id
    if len(genome_region) > 1:
        start, end = genome_region[1].split("-")
        minimac_param_kw["start"] = start
        minimac_param_kw["end"] = end

    minimac = Minimac(config, reference_panel=reference_panel)

    try:
        is_good = minimac.run(**minimac_param_kw)
        if is_good:
            out_impute_vcf = "%s.dose.vcf.gz" % output_prefix
            out_impute_rec = "%s.rec" % output_prefix
            out_impute_erate = "%s.erate" % output_prefix
            out_impute_info = "%s.info" % output_prefix

            return [out_impute_vcf, out_impute_rec, out_impute_erate, out_impute_info]
        else:
            return

    except:
        Log.warn("job for imputation %s is fail, may because can't find chromosome "
                 "%s in %s.\n" % (region, region, input_file))
        return

