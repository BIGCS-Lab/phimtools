"""Work with Minimac commands.

Author: Shujia Huang
Date: 2019-05-22
"""
from pi.log import Log
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

    def run(self, region, options=None):
        """Run a Minimac commands with provided options.

        Parameters:
            ``region``: String
                A genome region for imputation, format like chr_id:start-end
            ``options``: A tuple list like
                Options for Minimac. e.g: [("--parameter", value)]
        """
        if options is None:
            options = []

        cmd_options = options

        genome_region = region.split(":")
        chr_id = genome_region[0]
        if chr_id not in self.ref_panel:
            Log.warn("[WARNING] The reference panel does not contain chromosome %s, "
                     "imputation process stopped for this chromosome.\n" % chr_id)
            return False

        # set the region for Minimac
        cmd_options.append(("--chr", chr_id))
        if len(genome_region) > 1:
            start, end = genome_region.split("-")
            cmd_options.append(("--start", start))
            cmd_options.append(("--end", end))

        cmd = " ".join([self.minimac] + ["--refHaps %s" % self.ref_panel[chr_id]] +
                       ["%s %s" % (p, v) for p, v in cmd_options])
        do.run(cmd)

        return True
