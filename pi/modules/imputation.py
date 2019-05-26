"""A program for imputation process.

Author: Shujia Huang
Date: 2019-05-22
"""
import sys

from pi.tools.minimac3 import Minimac
from pi.modules.phasing import eagle_chromosome
from pi.utils import merge_files
from pi.log import Log
from . import get_chromlist


def minimac(config, input_file, output_prefix, nCPU=1, options=None, reference_panel=None,
            reference_version=None, merge_multi_output=True, is_prephase=True):
    """A function for running Minimac.

    Parameters:
        ``options``: A tuple list of Minimac parameters
        ``reference_panel``: A string.
                The reference panel for imputation process
    """
    if not input_file.endswith(".vcf.gz") and not input_file.endswith(".vcf"):
        Log.error("The format of input file is not a *.vcf.gz or *.vcf\n")
        sys.exit(1)

    chromosomes = get_chromlist(input_file)
    out_impute_files = []
    for chr_id in chromosomes:

        # ignore the chromosome which not in the reference panel, which may happen in chromosome X
        if chr_id not in config["minimac"]["reference_panel"][reference_panel]:
            Log.warn("[WARNING] chromosome %s is not in the panel: %s, which will not been "
                     "imputed in your final result.\n" % (chr_id, reference_panel))
            continue

        sub_outprefix = "%s.%s" % (output_prefix, chr_id)
        sub_out_impute_files = minimac_chromosome(config,
                                                  input_file,
                                                  sub_outprefix,
                                                  chr_id,
                                                  nCPU=nCPU,
                                                  options=options,
                                                  reference_panel=reference_panel,
                                                  reference_version=reference_version,
                                                  is_prephase=is_prephase)

        if sub_out_impute_files:
            out_impute_files.append(sub_out_impute_files)

    # Todo: Merge different kinds of output files
    if merge_multi_output:
        final_out_impute_file = "%s.final.vcf.gz" % output_prefix
        merge_files([f[0] for f in out_impute_files], final_out_impute_file,
                    is_del_raw_file=True)

        return final_out_impute_file

    return out_impute_files


def minimac_chromosome(config, input_file, output_prefix, chr_id, nCPU=1, options=None, reference_panel=None,
                       reference_version=None, is_prephase=True):
    """Impute for a single chromosome.

    Parameters:
        ``chr_id``: Chromosome for phasing
        ``options``: A tuple list of eagle parameters
        ``reference_version``: A string.
                set reference version for phasing process
    """
    Log.info("Performing imputation process for chromosome %s by using Minimac3." % chr_id)
    if options is None:
        options = []

    out_impute_vcf = "%s.dose.vcf.gz" % output_prefix
    out_impute_rec = "%s.rec" % output_prefix
    out_impute_erate = "%s.erate" % output_prefix
    out_impute_info = "%s.info" % output_prefix

    if is_prephase:
        # pre-phasing
        Log.info("Performing pre-phasing process by imputation.")
        phased_file = eagle_chromosome(config, input_file, output_prefix + ".phased", chr_id,
                                       options=[("--numThreads", nCPU)],
                                       reference_version=reference_version)
    else:
        Log.info("Do not perform pre-phase, usually because %s is already a phased result." % input_file)
        phased_file = input_file

    minimac_program = Minimac(config, reference_panel=reference_panel)

    # Todo: set reference region by --start and --end not just for the whole chromosome
    if "--cpus" not in options:
        options.append(("--cpus", nCPU))

    cmd_options = options + [("--haps", phased_file), ("--chr", chr_id), ("--prefix", output_prefix)]
    minimac_program.run(chr_id, cmd_options)

    return [out_impute_vcf, out_impute_rec, out_impute_erate, out_impute_info]

