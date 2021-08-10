"""A function for checking the format of a VCF is suit for phimtools

Author: Shujia Huang
Date: 2019-05-26
"""
import sys

from phimtools.log import Log
from phimtools.utils import Open


def check_gt_format(gt):
    if gt == ".":
        return True

    genos = gt.replace("|", "/").split("/")
    if len(genos) != 1 and len(genos) != 2:
        return False

    for g in genos:
        if g == "." or g.isdigit():
            continue

        return False

    return True


def check_vcf_format(in_vcf_file, chr_error_given=True):
    Log.info("Validating the format of %s" % in_vcf_file)

    if not in_vcf_file.endswith(".vcf") and not in_vcf_file.endswith(".vcf.gz"):
        Log.error("The format of %s is not a *.vcf.gz or *.vcf" % in_vcf_file)
        sys.exit(1)

    ACGT = set(['A', 'C', 'G', 'T'])
    ACGTM = set(['A', 'C', 'G', 'T', '.'])

    num = 0
    vcf_site_num = 0
    field_num = 0

    prev_pos = {}
    snp_site = set()
    with Open(in_vcf_file, 'r') as I:

        for line in I:
            if num % 10000 == 0 and num != 0:
                Log.info("[ %d ] lines processed" % num)

            num += 1

            if line.startswith("##"):
                continue

            if line.startswith("#CHROM"):
                col = line.strip().split()
                field_num = len(col)
                vcf_sample_num = field_num - 9
                if vcf_sample_num < 1:
                    Log.error("Your VCF file have 0 sample, please fix them and re-run")
                    sys.exit(1)

                elif len(set(col[9:])) != vcf_sample_num:
                    Log.error("Your VCF file have duplicated sample IDs, please fix them and re-run")
                    sys.exit(1)

                continue

            if line[:3].upper() == "CHR" and chr_error_given:
                Log.error("Detected that chromosome IDs have 'chr' prefix ... Can only allow "
                          "chromosome 1-22 and X without 'chr' in the front. Please consider using "
                          "the following command to clean your VCF file and re-run phimtools: \n"
                          "sed 's:^chr::' $your_old_vcf | bgzip -c > $your_vcf_file")
                sys.exit(1)

            vcf_site_num += 1
            col = line.strip().split()

            if len(col) != field_num:
                Log.error("Line [ %d ] does not have correct column number, program exiting! "
                          "Current line has %d columns.\n First 100 characters in current line is "
                          "[ %s ]" % (num, len(col), line.strip()[:100]))
                sys.exit(1)

            chrom, pos, rs_id, ref, alt, qual, filter_info, info, format_info = col[:9]
            if len(ref) != 1 or len(alt) != 1 or (ref not in ACGT or alt not in ACGTM):
                # non SNP variants
                continue

            site_key = chrom + ":" + pos
            if site_key in snp_site:
                Log.error("Hit duplicate sites [ %s ], please fix them and re-run. " % site_key)
                sys.exit(1)

            else:
                snp_site.add(site_key)

            # check VCF is in asending order or not
            if chrom in prev_pos:
                if prev_pos[chrom] > int(pos):
                    Log.error("Line [ %d ], genomics position is not in asending order, the position %s:%s "
                              "is before %s:%s " % (num, chrom, prev_pos[chrom], chrom, pos))
                    sys.exit(1)
            else:
                prev_pos[chrom] = int(pos)

            # check genotype information
            try:
                gt_idx = [i for i, g in enumerate(format_info.split(":")) if g == "GT"][0]
            except:
                Log.error("Line [ %d ] does not have GT defined in FORMAT field.\n First 100 characters "
                          "in current line is [ %s ]." % (num, line.strip()[:100]))
                sys.exit(1)

            try:
                genotypes = [g.split(":")[gt_idx] for g in col[9:]]
            except:
                Log.error("Missing GT field in at least one of the VCF samples\t Line: %d .\nFirst 100 "
                          "charaters in current line is [ %s ]." % (num, line.strip()[:100]))
                sys.exit(1)

    Log.info("The format of your input VCF looks good! Format verification is OK!")
    return True


if __name__ == "__main__":
    check_vcf_format(sys.argv[1], chr_error_given=True)
