"""Work with Minimac commands.

Author: Shujia Huang
Date: 2019-05-22
"""
from pi.launch import do


class Minimac(object):
    """A class for Minimac3 program"""

    def __init__(self, config, reference_panel=None):
        """basical setting for Minimac"""

        if reference_panel is None:
            return

        self.minimac = config["minimac"]["minimac"]
        self.ref_panel = config["minimac"]["reference_panel"][reference_panel]

    def help(self):
        """Help information for Minimac program"""
        return do.run("%s --help" % self.minimac)

    def run(self, chr_id, options):
        """Run a Eagle command with the provide options.

        Parameters:
            ``chr_id``: String
                The chromosome id
            ``options``: A tuple like
                Options for Eagle.
        """
        cmd = " ".join([self.minimac] + ["--refHaps %s" % self.ref_panel[chr_id]] +
                       ["%s %s" % (p, v) for p, v in options])

        do.run(cmd)
        return
