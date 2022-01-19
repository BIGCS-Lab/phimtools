"""
Author: Shujia Huang
Date: 2019-05-21
"""
from phimtools.utils import Open


def get_chromlist(input_file):
    chr_list = set()
    with Open(input_file, "rt") as C:
        for line in C:
            if line.startswith("#"):
                continue

            # first column must be the chromosome id
            chr_id = line.strip().split()[0]
            chr_list.add(chr_id)

    return chr_list


def split2chrom(input_file, chrom, out_prefix):
    outVCF = Open("%s.unphased.vcf.gz" % (out_prefix), 'wt')
    with Open(input_file, "rt") as inVCF:
        for line in inVCF:
            if line.startswith("#"):
                outVCF.write(line)
            else:
                chr_id = line.strip().split()[0]
                if chr_id == chrom:
                    outVCF.write(line)
    return("%s.unphased.vcf.gz" % (out_prefix))
