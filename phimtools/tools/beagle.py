"""Work with beagle 5.2 commands.

Author: Chengrui Wang
Date: 2022-01-07
"""
import os
from phimtools.launch import do


class Beagle(object):
    """A class for Beagle 5.2 program"""

    def __init__(self, config, reference_version=None, chrom=None):
        """basical setting for beagle"""

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools','/third_party')

        if os.path.exists(config["beagle"]["beagle"]):
            self.beagle = config["beagle"]["beagle"]
        else:
            self.beagle = bin_path + '/beagle.28Jun21.220.jar'

        self.java = config["java"]
        self.genetic_map_file = config["beagle"]["genetic_map_file"][reference_version][chrom]

    def help(self):
        """Help information for beagle"""
        return do.run("%s -jar %s" % (self.java, self.beagle))

    def run(self, **kwargs):
        """Run a beagle command with the provide options.

        Parameters:
            ``kwargs``: A dict like
                key word parameter for beagle
        """
        cmd = " ".join([self.java, '-jar', self.beagle] + 
                       ["map=%s" % self.genetic_map_file] + 
                       ["impute=false"] + 
                       ["%s=%s" % (k, v) for k, v in kwargs.items()])
        do.run(cmd)
        return
