"""A program for phasing process.

Author: Shujia Huang
Date: 2019-05-20
"""
import sys
import os

from pi.tools.eagle import Eagle
from pi.utils import merge_files


def eagle(config, input_file, output_prefix, options=None, reference_version=None, merge_multi_output=True):
    """A function for running eagle.

    Parameters:
        ``format``: Must be VCF or PLINK
        ``options``: A tuple list of eagle parameters
        ``reference_version``: A string.
                set reference version for phasing process
    """
    # find the format of input file, default set to be "PLINK(bed/bim/fam)"
    input_format = "VCF" if input_file.endswith(".vcf.gz") or input_file.endswith(".vcf") else "PLINK"

    chromosomes = config["phasing_chromosome_1_22_X"][reference_version]

    # Todo: set one process for each chromosome?
    out_phased_files = []
    for chr_id in chromosomes:

        sub_outprefix = "%s.%s" % (output_prefix, chr_id)
        sub_out_phased_file = eagle_chromosome(config, input_file, sub_outprefix, chr_id,
                                               options=options, reference_version=reference_version)
        if sub_out_phased_file:
            out_phased_files.append(sub_out_phased_file)

    # Todo: do something if setting one process for each chromosome
    # Merge into one single final output file.
    if merge_multi_output:
        if input_format == "VCF":
            final_out_phased_file = "%s.vcf.gz" % output_prefix
            merge_files(out_phased_files, final_out_phased_file, is_del_raw_file=True)
            return final_out_phased_file
        else:
            # PLINK format
            final_out_haps_file = "%s.haps.gz" % output_prefix

            # Todo: Make a suitable function for mergeing subfiles PLINK format output
            # it's not work right now!
            merge_files([h for h, _ in out_phased_files], final_out_haps_file, is_del_raw_file=True)

            # remove other *.sample files, because they're the same, we can just keep the first one.
            for _, f in out_phased_files[1:]:
                os.remove(f)

            return final_out_haps_file, os.rename(out_phased_files[0][1], "%s.sample" % output_prefix)
    else:

        # Return a list of phased files
        return out_phased_files


def eagle_chromosome(config, input_file, output_prefix, chr_id, options=None, reference_version=None):
    """A phasing function by eagle for a single one chromosome.

    Parameters:
        ``format``: Must be VCF or PLINK
        ``chr_id``: Chromosome for phasing
        ``options``: A tuple list of eagle parameters
        ``reference_version``: A string.
                set reference version for phasing process
    """
    if options is None:
        options = []

    # find the format of input file, default set to be "PLINK(bed/bim/fam)"
    input_format = "VCF" if input_file.endswith(".vcf.gz") or input_file.endswith(".vcf") else "PLINK"

    # set input file
    if input_format == "VCF":
        options.append(("--vcf", input_file))

    else:
        # do not compress you PLINK data by gzip or bgzip.
        options.append(("--bfile", input_file))

    eagle_program = Eagle(config, reference_version=reference_version)

    sub_out_phased_file = "%s.vcf.gz" % output_prefix
    if input_format == "PLINK":
        # *.sample files are the same
        sub_out_phased_file = ["%s.haps.gz" % output_prefix, "%s.sample" % output_prefix]

    try:
        # Set output and run eagle phasing process.
        eagle_program.run(options + [("--chrom", chr_id), ("--outPrefix", output_prefix)])
        return sub_out_phased_file

    except:
        sys.stderr.write("[WARNING] job for phasing chrom %s is fail, can't find "
                         "chrom %s in %s.\n" % (chr_id, chr_id, input_file))
        return

