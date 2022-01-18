"""Run eagle/beagle/minimac independently.

Author: Chengrui Wang
Date: 2022-01-07
"""
import sys
import subprocess
from phimtools.log import Log
from phimtools.launch import do


class Thirdparty(object):
    """A class for running eagle/beagle/minimac program independently"""

    def __init__(self, toolstore, param_kw=[]):
        """basical setting for exec_module"""

        self.exec_module = toolstore[param_kw[0]]
        if len(param_kw) > 1:
            self.param_kw = param_kw[1:]
        else:
            self.param_kw = []

        params = " ".join(self.param_kw)
        if param_kw[0] == "beagle":
            if do.find_cmd("java"):
                self.java = do.find_cmd("java")
            else:
                Log.error("Couldn't find the java program. If java "
                          "had been installed, please add it to the PATH.")
                sys.exit(1)

            self.cmd = "%s -jar %s %s" % (self.java, self.exec_module, params)
        else:
            self.cmd = "%s %s" % (self.exec_module, params)

    def run(self):
        """Run exec_module command with the provide options."""
        
        subprocess.run(self.cmd, shell=True, encoding="utf-8")
        return
