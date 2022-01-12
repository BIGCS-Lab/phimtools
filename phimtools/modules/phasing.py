"""A program for phasing process.

Author: Shujia Huang
Date: 2019-05-20
"""
import os

from phimtools.tools.eagle import Eagle
from phimtools.tools.beagle import Beagle
from phimtools.utils import merge_files
from phimtools.log import Log
from . import get_chromlist


def eagle(config, input_file, output_prefix, options=None, reference_version=None, merge_multi_output=True):
    """A function for running eagle.

    Parameters:
        ``options``: A tuple list of eagle parameters
        ``reference_version``: A string.
                set reference version for phasing process
    """
    # find the format of input file, default set to be "PLINK(bed/bim/fam)"
    input_format = "VCF" if input_file.endswith(".vcf.gz") or input_file.endswith(".vcf") else "PLINK"

    if input_format == "VCF":
        chromosomes = get_chromlist(input_file)
    else:
        # PLINK format
        """
        *.bim file looks like below and the first column is the id of chromosome.
        
        21	rs11702480	0.415634	38347375	G	A
        21	rs7280358	0.415683	38349787	A	C
        21	rs7282108	0.415721	38352192	A	C
        21	rs58296537	0.415776	38358682	G	C
        21	rs150853915	0.415796	38361458	T	C
        """
        chromosomes = get_chromlist(input_file + ".bim")

    # Todo: set one process for each chromosome?
    out_phased_files = []
    for chr_id in chromosomes:

        sub_outprefix = "%s.%s" % (output_prefix, chr_id)
        sub_out_phased_file = eagle_region(config,
                                           input_file,
                                           sub_outprefix,
                                           chr_id,
                                           reference_version=reference_version,
                                           options=options)
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
            # it's NOT WORK right now!
            merge_files([h for h, _ in out_phased_files], final_out_haps_file, is_del_raw_file=True)

            # remove other *.sample files, because they're the same, we can just keep the first one.
            for _, f in out_phased_files[1:]:
                os.remove(f)

            return final_out_haps_file, os.rename(out_phased_files[0][1], "%s.sample" % output_prefix)
    else:
        # Return a list of phased files
        return out_phased_files

    return  # NULL


def eagle_region(config, input_file, output_prefix, region, reference_version=None, options=None):
    """A phasing function by eagle for a specific genome region.

    Parameters:
        ``region``: String
            A genome region for eagle, format like chr_id:start-end

        ``options``: A tuple list of eagle parameters

        ``reference_version``: A string.
                set reference version for phasing process
    """
    region = str(region)
    Log.info("Performing phasing process for %s by using Eagle." % region)
    if options is None:
        options = []

    # set parameter for eagle as a key-world pair.
    eagle_param_kw = {k: v for k, v in options}

    # find the format of input file, default set to be "PLINK(bed/bim/fam)"
    input_format = "VCF" if input_file.endswith(".vcf.gz") or input_file.endswith(".vcf") else "PLINK"

    # set input file
    if input_format == "VCF":
        eagle_param_kw["vcf"] = input_file

    else:
        # do not compress you PLINK data by gzip or bgzip.
        eagle_param_kw["bfile"] = input_file

    # set the region for eagle
    genome_region = region.split(":")
    eagle_param_kw["chrom"] = genome_region[0]

    if len(genome_region) > 1:
        start, end = genome_region[1].split("-")
        eagle_param_kw["bpStart"] = start
        eagle_param_kw["bpEnd"] = end

    # set output prefix for eagle
    eagle_param_kw["outPrefix"] = output_prefix
    try:
        # run eagle phasing process.
        eagle_program = Eagle(config, reference_version=reference_version)
        eagle_program.run(**eagle_param_kw)

        # get output files by ``output_prefix``
        sub_out_phased_file = "%s.vcf.gz" % output_prefix
        if input_format == "PLINK":
            # *.sample files are the same
            sub_out_phased_file = ["%s.haps.gz" % output_prefix, "%s.sample" % output_prefix]

        return sub_out_phased_file

    except Exception as e:
        Log.warn("Job for phasing %s has failed, there's something wrong happen "
                 "in %s in %s.\nError: %s\n Ignore phasing.\n" % (region, region, input_file, e))
        # Just return input file. This could be happen if there is only
        # one sample in input vcf.
        return input_file


def beagle_region(config, input_file, output_prefix, region, reference_version=None, options=None):
    """A phasing function by beagle for a specific genome region.

    Parameters:
        ``region``: String
            A genome region for beagle, format like chr_id:start-end
        ``options``: A tuple list of beagle parameters
        ``reference_version``: A string.
                set reference version for phasing process
    """
    region = str(region)
    Log.info("Performing phasing process for %s by using beagle." % region)
    if options is None:
        options = []

    # set parameter for beagle as a key-world pair.
    beagle_param_kw = {k: v for k, v in options}

    # find the format of input file, default set to be "PLINK(bed/bim/fam)"
    input_format = "VCF" if input_file.endswith(".vcf.gz") or input_file.endswith(".vcf") else "PLINK"

    # set input file
    if input_format == "VCF":
        beagle_param_kw["gt"] = input_file

    else:
        Log.warn("Job for phasing %s has failed, please input VCF format file for "
                 "beagle phasing.\nError: %s\n" % (region, input_file))
        # Just return input file. This could be happen if there is only
        # one sample in input vcf.
        return input_file

    # set the region for beagle
    genome_region = region  # chrom:start-end
    beagle_param_kw["chrom"] = genome_region

    # set output prefix for beagle
    beagle_param_kw["out"] = output_prefix
    try:
        # run beagle phasing process.
        beagle_program = Beagle(config, reference_version=reference_version,
                                chrom=genome_region.split(":")[0].lower().replace("chr", ""))
        beagle_program.run(**beagle_param_kw)

        # get output files by ``output_prefix``
        sub_out_phased_file = "%s.vcf.gz" % output_prefix
        return sub_out_phased_file

    except Exception as e:
        Log.warn("Job for phasing %s has failed, there's something wrong happen "
                 "in %s.\nError: %s\n Ignore phasing.\n" % (region, input_file, e))
        # Just return input file. This could be happen if there is only
        # one sample in input vcf.
        return input_file
