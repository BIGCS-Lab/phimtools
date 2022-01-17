"""Work with Minimac commands.

Author: Shujia Huang
Date: 2019-05-22
"""
import os
import sys
import stat
import subprocess
from phimtools.log import Log
from phimtools.launch import do


class Minimac(object):
    """A class for Minimac3/Minimac4 program"""

    def __init__(self, config, reference_panel=None):
        """basical setting for Minimac"""

        if reference_panel is None:
            return

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools', '/phimtools/third_party')

        if os.path.exists(config["minimac"]["minimac"]):
            self.minimac = config["minimac"]["minimac"]
        elif do.find_cmd("minimac4"):
            self.minimac = do.find_cmd("minimac4")
        elif do.find_cmd("Minimac3"):
            self.minimac = do.find_cmd("Minimac3")
        elif os.path.exists(bin_path + '/Minimac3'):
            os.chmod(bin_path + '/Minimac3', stat.S_IXUSR)
            self.minimac = bin_path + '/Minimac3'
        else:
            Log.error("Couldn't find the minimac program.")
            Log.error("If minimac had been installed, please add it to the environment.")
            sys.exit(1)

        self.ref_panel = config["minimac"]["reference_panel"][reference_panel]

    def help(self):
        """Help information for Minimac program"""
        return do.run("%s --help" % self.minimac)

    def run(self, **kwargs):
        """Run a Minimac commands with provided options.

        Parameters:
            ``kwargs``: A dict like
                key world parameter for minimac
        """
        if "chr" not in kwargs:
            Log.error("Missing 'chr' for reference panel in the Minimac command")
            return False

        cmd = " ".join([self.minimac] + ["--refHaps %s" % self.ref_panel[kwargs["chr"]]] +
                       ["--%s %s" % (k, v) for k, v in kwargs.items()])
        do.run(cmd)
        return True


class minimac_without_config(object):
    """A class for minimac program"""

    def __init__(self, param_kw=["--help"]):
        """basical setting for minimac"""

        module_path = os.path.dirname(__file__)
        bin_path = module_path.replace('/phimtools/tools', '/phimtools/third_party')

        if do.find_cmd("minimac4"):
            self.minimac = do.find_cmd("minimac4")
        elif do.find_cmd("Minimac3"):
            self.minimac = do.find_cmd("Minimac3")
        elif os.path.exists(bin_path + '/Minimac3'):
            os.chmod(bin_path + '/Minimac3', stat.S_IXUSR)
            self.minimac = bin_path + '/Minimac3'
        else:
            Log.error("Couldn't find the minimac program.")
            Log.error("If minimac had been installed, please add it to the environment.")
            sys.exit(1)

        self.param_kw = param_kw

    def run(self):
        """Run a minimac command with the provide options."""
        cmd = self.minimac + ' %s'%(" ".join(self.param_kw))
        subprocess.run(cmd, shell=True, encoding="utf-8")
        return
