"""
Author: Shujia Huang
Date: 2019-05-21
"""
from phimtools.utils import Open


def get_chromlist(input_file):

    chr_list = set()
    with Open(input_file, "r") as C:
        for line in C:
            if line.startswith("#"):
                continue

            # first column must be the chromosome id
            chr_id = line.strip().split()[0]
            chr_list.add(chr_id)

    return chr_list
