"""Work with eagle commands.

Author: Shujia Huang
Date: 2019-05-20
"""
import os
import sys
from phimtools.log import Log
from phimtools.launch import do


class Eagle(object):
    """A class for Eagle (Version 2.4.1) program"""

    def __init__(self, config, toolstore, reference_version):
        """basical setting for Eagle"""

        self.eagle = toolstore["eagle"]

        if os.path.exists(config["eagle"]["genetic_map_file"][reference_version]):
            self.genetic_map_file = config["eagle"]["genetic_map_file"][reference_version]
        else:
            Log.warn("Eagle genetic_map_hg##.txt.gz is missing.\n")
            sys.exit(1)
            
    def help(self):
        """Help information for Eagle"""
        return do.run("%s --help" % self.eagle)

    def run(self, **kwargs):
        """Run a Eagle command with the provide options.

        Parameters:
            ``kwargs``: A dict like
                key world parameter for Eagle
        """
        cmd = " ".join([self.eagle] + 
                       ["--geneticMapFile=%s" % self.genetic_map_file] +
                       ["--%s=%s" % (k, v) for k, v in kwargs.items()])
        do.run(cmd)
        return
