"""A program for phasing process.

Author: Shujia Huang
Date: 2019-05-20
"""
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

    chromosomes = config["phasing_chromosome_1_22_X"][reference_version]
    eagle_program = Eagle(config, reference_version=reference_version)

    # Todo: set one process for each chromosome?
    out_phased_files = []
    for chr_id in chromosomes:

        sub_outprefix = "%s.%s" % (output_prefix, chr_id)
        sub_out_phased_file = "%s.vcf.gz" % sub_outprefix
        if input_format == "PLINK":
            # *.sample files are the same
            sub_out_phased_file = ["%s.haps.gz" % sub_outprefix,
                                   "%s.sample" % output_prefix]

        # Set output and run eagle phasing process.
        eagle_program.run(options + [("--chrom", chr_id), ("--outPrefix", sub_outprefix)])
        out_phased_files.append(sub_out_phased_file)

    # Todo: do something if setting one process for each chromosome

    # Merge into one single final output file.
    if merge_multi_output:
        if input_format == "VCF":
            final_out_phased_file = "%s.vcf.gz" % output_prefix
            merge_files(out_phased_files, final_out_phased_file)
            return final_out_phased_file
        else:
            # PLINK format
            final_out_haps_file = "%s.haps.gz" % output_prefix
            merge_files([h for h, _ in out_phased_files], final_out_haps_file)
            return final_out_haps_file, out_phased_files[0][1]
    else:

        # Return a list of phased files
        return out_phased_files
