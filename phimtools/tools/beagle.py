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

    def __init__(self, config, toolstore, reference_version, chrom):
        """basical setting for beagle"""

        self.beagle = toolstore["beagle"]

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

    def __init__(self, toolstore, param_kw=[]):
        """basical setting for beagle"""

        if do.find_cmd("java"):
            self.java = do.find_cmd("java")
        else:
            Log.error("Couldn't find the java program.")
            Log.error("If java had been installed, please add it to the PATH.")
            sys.exit(1)

        self.beagle = toolstore["beagle"]
        self.param_kw = param_kw

    def run(self):
        """Run a beagle command with the provide options."""

        params = " ".join(self.param_kw)
        cmd = "%s -jar %s %s" % (self.java, self.beagle, params)
        subprocess.run(cmd, shell=True, encoding="utf-8")
        return
