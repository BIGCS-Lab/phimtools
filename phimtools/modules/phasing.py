"""A program for phasing process.

Author: Shujia Huang
Date: 2019-05-20
"""
from phimtools.tools.eagle import Eagle
from phimtools.tools.beagle import Beagle
from phimtools.log import Log


def eagle_region(config, toolstore, input_file, output_prefix, region, reference_version=None, options=None):
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
        eagle_program = Eagle(config, toolstore, reference_version=reference_version)
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


def beagle_region(config, toolstore, input_file, output_prefix, region, reference_version=None, reference_panel=None, options=None):
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
    genome_region = region  # chrom:start-end or chrom
    beagle_param_kw["chrom"] = genome_region

    # set output prefix for beagle
    beagle_param_kw["out"] = output_prefix
    try:
        # run beagle phasing process.
        beagle_program = Beagle(config, toolstore, 
                                reference_version=reference_version,
                                reference_panel=reference_panel,
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
