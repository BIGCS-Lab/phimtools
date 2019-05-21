"""
Author: Shujia Huang
Date: 2019-05-21
"""
from pi.utils import Open


def get_vcf_chromlist(input_file):

    chr_list = set()
    with Open(input_file, "r") as C:
        for line in C:
            if line.startswith("#"):
                continue

            chr_id = line.strip().split()[0]
            chr_list.add(chr_id)

    return chr_list
