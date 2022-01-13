"""Work with beagle 5.2 commands.

Author: Chengrui Wang
Date: 2022-01-07
"""
import os
import sys
import subprocess
from phimtools.log import Log
from phimtools.launch import do


class Beagle(object):
    """A class for Beagle 5.2 program"""

    def __init__(self, config, reference_version=None, chrom=None):
        """basical setting for beagle"""

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools','/phimtools/third_party')

        if os.path.exists(config["beagle"]["beagle"]):
            self.beagle = config["beagle"]["beagle"]
        elif os.path.exists(bin_path + '/beagle.28Jun21.220.jar'):
            self.beagle = bin_path + '/beagle.28Jun21.220.jar'
        else:
            Log.error("beagle program is not existed\n")
            sys.exit(1)

        if "java" in config.keys() and os.path.exists(config["java"]):
            self.java = config["java"]
        else:
            self.java = do.find_cmd("java")

        if os.path.exists(config["beagle"]["genetic_map_file"][reference_version][chrom]):
            self.genetic_map_file = config["beagle"]["genetic_map_file"][reference_version][chrom]
        else:
            Log.warn("beagle plink.chr#.GRCh3#.map is missing.\n")
            Log.warn("Without map=<PLINK map file with cM units> parameter will be performed.\n")
            self.genetic_map_file = None

    def help(self):
        """Help information for beagle"""
        return do.run("%s -jar %s" % (self.java, self.beagle))

    def run(self, **kwargs):
        """Run a beagle command with the provide options.

        Parameters:
            ``kwargs``: A dict like
                key word parameter for beagle
        """
        if self.genetic_map_file:
            cmd = " ".join([self.java, '-jar', self.beagle] + 
                           ["map=%s" % self.genetic_map_file] + 
                           ["impute=false"] + 
                           ["%s=%s" % (k, v) for k, v in kwargs.items()])
        else:
            cmd = " ".join([self.java, '-jar', self.beagle] + 
                           ["impute=false"] + 
                           ["%s=%s" % (k, v) for k, v in kwargs.items()])
        do.run(cmd)
        return

class beagle_without_config(object):
    """A class for beagle 5.2 program"""

    def __init__(self, param_kw=[]):
        """basical setting for beagle"""

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools','/phimtools/third_party')

        if do.find_cmd("java"):
            self.java = do.find_cmd("java")
        else:
            Log.error("Couldn't find the java program.")
            Log.error("If java had been installed, please add it to the environment.")
            sys.exit(1)

        self.beagle = bin_path + '/beagle.28Jun21.220.jar'
        self.param_kw = param_kw

    def run(self):
        """Run a beagle command with the provide options.

        """
        cmd = "%s -jar %s %s"%(self.java, self.beagle, " ".join(self.param_kw))
        subprocess.run(cmd, shell=True, encoding="utf-8")
        return