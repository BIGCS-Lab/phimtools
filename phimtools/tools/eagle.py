"""Work with eagle commands.

Author: Shujia Huang
Date: 2019-05-20
"""
import os
import stat
import sys
import subprocess
from phimtools.log import Log
from phimtools.launch import do


class Eagle(object):
    """A class for Eagle (Version 2.4.1) program"""

    def __init__(self, config, reference_version=None):
        """basical setting for Eagle"""

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools','/phimtools/third_party')

        if os.path.exists(config["eagle"]["eagle"]):
            self.eagle = config["eagle"]["eagle"]
        elif os.path.exists(bin_path + '/eagle'):
            os.chmod(bin_path + '/eagle', stat.S_IXUSR)
            self.eagle = bin_path + '/eagle'
        else:
            Log.error("Eagle program is not existed\n")
            sys.exit(1)

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
        cmd = " ".join([self.eagle] + ["--geneticMapFile=%s" % self.genetic_map_file] +
                       ["--%s=%s" % (k, v) for k, v in kwargs.items()])
        do.run(cmd)
        return

class Eagle_without_config(object):
    """A class for Eagle (Version 2.4.1) program."""

    def __init__(self, param_kw=["--help"]):
        """basical setting for Eagle"""

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools','/phimtools/third_party')

        self.eagle = bin_path + '/eagle'
        self.param_kw = param_kw

    def run(self):
        """Run a Eagle command with the provide options."""
        cmd = self.eagle + ' %s'%(" ".join(self.param_kw))
        subprocess.run(cmd, shell=True, encoding="utf-8")
        return