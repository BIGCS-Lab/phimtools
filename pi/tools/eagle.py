"""Work with eagle commands.

Author: Shujia Huang
Date: 2019-05-20
"""
from pi.launch import do


class Eagle(object):
    """A class for Eagle (Version 2.4.1) program"""
    def __init__(self, config, reference_version=None):
        """basical setting for Eagle"""

        self.eagle = config["eagle"]["eagle"]
        self.genetic_map_file = config["eagle"]["genetic_map_file"][reference_version]

    def help(self):
        """Help information for Eagle"""
        return do.run("%s --help" % self.eagle)

    def run(self, options):
        """Run a Eagle command with the provide options.

        Parameters:
            ``options``: A tuple like
                Options for Eagle.
        """
        cmd = " ".join([self.eagle] + ["--geneticMapFile=%s" % self.genetic_map_file] + 
                       ["%s=%s" % (p, v) for p, v in options])
        do.run(cmd)

        return







