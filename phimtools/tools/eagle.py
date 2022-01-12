"""Work with eagle commands.

Author: Shujia Huang
Date: 2019-05-20
"""
import os
from phimtools.launch import do


class Eagle(object):
    """A class for Eagle (Version 2.4.1) program"""

    def __init__(self, config, reference_version=None):
        """basical setting for Eagle"""

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools','/phimtools/third_party')

        if os.path.exists(config["eagle"]["eagle"]):
            self.eagle = config["eagle"]["eagle"]
        else:
            self.eagle = bin_path + '/eagle'
        self.genetic_map_file = config["eagle"]["genetic_map_file"][reference_version]

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
