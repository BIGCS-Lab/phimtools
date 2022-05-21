"""Work with beagle 5.2 commands.

Author: Chengrui Wang
Date: 2022-01-07
"""
import os
from phimtools.log import Log
from phimtools.launch import do


class Beagle(object):
    """A class for Beagle 5.2 program"""

    def __init__(self, config, toolstore, reference_version, reference_panel, chrom):
        """basical setting for beagle"""

        self.beagle = toolstore["beagle"]

        if "java" in config.keys() and os.path.exists(config["java"]):
            self.java = config["java"]
        else:
            self.java = do.find_cmd("java")

        if os.path.exists(config["beagle"]["genetic_map_file"][reference_version][chrom]):
            self.genetic_map_file = config["beagle"]["genetic_map_file"][reference_version][chrom]
        else:
            Log.warn("beagle plink.chr#.GRCh3#.map is missing.")
            Log.warn("Without map=<...> parameter will be performed.")
            self.genetic_map_file = None

        if reference_panel:
            if os.path.exists(config["beagle"]["reference_panel"][reference_panel][chrom]):
                self.reference_panel = config["beagle"]["reference_panel"][reference_panel][chrom]
        else:
            Log.warn("running pre-phased without ref=<...>")
            self.reference_panel = None

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
            if self.reference_panel:
                cmd = " ".join([self.java, '-jar', self.beagle] + 
                               ["map=%s" % self.genetic_map_file] + 
                               ["ref=%s" % self.reference_panel] +
                               ["%s=%s" % (k, v) for k, v in kwargs.items()])
            else:
                cmd = " ".join([self.java, '-jar', self.beagle] + 
                               ["map=%s" % self.genetic_map_file] + 
                               ["%s=%s" % (k, v) for k, v in kwargs.items()])
        else:
            if self.reference_panel:
                cmd = " ".join([self.java, '-jar', self.beagle] + 
                               ["ref=%s" % self.reference_panel] +
                               ["%s=%s" % (k, v) for k, v in kwargs.items()])
            else:
                cmd = " ".join([self.java, '-jar', self.beagle] + 
                               ["%s=%s" % (k, v) for k, v in kwargs.items()])
        do.run(cmd)
        return
