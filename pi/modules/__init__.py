"""
Author: Shujia Huang
Date: 2019-05-21
"""
import sys

from pi.utils import Open
from pi.log import Log


def get_chromlist(input_file):

    chr_list = set()
    with Open(input_file, "r") as C:
        for line in C:
            if line.startswith("#"):
                continue

            # first column must be the chromosome id
            chr_id = line.strip().split()[0]
            if chr_id[:3].upper() == "CHR":
                Log.error("Target VCF File contains chromosome: %s\n VCF File "
                          "can only contain chromosomes 1-22 and X without 'chr' in "
                          "the front!!!\n" % chr_id)
                sys.exit(1)

            chr_list.add(chr_id)

    return chr_list
