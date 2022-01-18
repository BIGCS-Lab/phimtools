"""
Author: Shujia Huang
Date: 2019-05-21
"""
from phimtools.utils import Open


def get_chromlist(input_file):
    chr_region = {}
    chr_list = []
    with Open(input_file, "rt") as C:
        for line in C:
            if line.startswith("#"):
                continue

            # first column must be the chromosome id
            chr_id = line.strip().split()[0]
            chr_region.setdefault(chr_id,[]).append(int(line.strip().split()[1]))
            if len(chr_region[chr_id]) > 1:
                chr_region[chr_id] = [sorted(chr_region[chr_id])[0], sorted(chr_region[chr_id])[-1]]
            
    for chrom in chr_region.keys():
        chr_list.append("%s:%d-%d" % (chrom,chr_region[chrom][0],chr_region[chrom][1]))

    return chr_list
