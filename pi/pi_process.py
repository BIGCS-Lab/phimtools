#!/usr/bin/env python
"""The pipeline for phasing and imputation process.

Author: Shujia Huang
Date: 2019-05-22
"""
import sys
import argparse
import yaml

from datetime import datetime

from pi.utils import file_exists
from pi.launch import runfunction
from pi.log import Log

VERSION = "0.1.0"
LONG_DESC = """
------------------------------------------------------------------
       pi - A pipeline for phasing and imputation analysis.     
------------------------------------------------------------------
                   (c) 2019 - Shujia Huang                      
       Distributed under the GNU GPLv3+ open source license.    

Version {version}                                                     

URL = https://github.com/ShujiaHuang/pi                           
-----------------------------------------------------------------
""".format(version=VERSION)


def parse_commandline_args(args):
    """Parse input commandline arguments, handling multiple cases."""

    desc = "pi - A pipeline for phasing and imputation analysis."
    parser = argparse.ArgumentParser(description=desc)
    subparser = parser.add_subparsers(help="PI supplemental commands")

    impute_parser = subparser.add_parser("impute", help="Run imputation for NGS data.")
    impute_parser.add_argument("-C", "--conf", dest="config", required=True,
                               help="YAML configuration file specifying details information "
                                    "for imputation")

    impute_parser.add_argument("-M", "--methods", dest="impute_method", default="minimac",
                               help="Tool for imputation. [minimac]")
    # impute_parser.add_argument("-P", "--prephase-method", dest="phase_method", default="eagle",
    #                            help="Tool for pre-phase before imputation. "
    #                                 "If not set do not process pre-phase. [eagle]")

    impute_parser.add_argument("-I", "--input", dest="in_vcf", required=True,
                               help="Input one VCF file to analyze. Required")

    impute_parser.add_argument("-O", "--outprefix", dest="out_prefix", required=True,
                               help="Prefix for output files. Required")
    impute_parser.add_argument("--refpanel-version", dest="refpanel", required=True,
                               help="The version of haplotype data for reference panel. Required")
    impute_parser.add_argument("--reference-build", dest="refbuild", required=True,
                               help="The build version of reference, e.g: GRCh37")
    impute_parser.add_argument("--nCPU", dest="nCPU", type=int, default=1, help="Number of threads. [1]")

    return parser.parse_args(args)


def checkconfig(config, kwargs):
    """Check the most important parameters is setted or not."""

    conf_msg = "Please find an example: https://github.com/ShujiaHuang/pi/blob/master/tests/config.yaml"

    phase = "eagle"
    if phase not in config:
        Log.error("Missing '%s' in config file.\n%s\n" % (phase, conf_msg))
        sys.exit(1)

    if phase not in config[phase]:
        Log.error("Missing set '%s' path for phasing.\n%s\n" % (phase, conf_msg))
        sys.exit(1)

    if not file_exists(config[phase][phase]):
        Log.error("%s program is not existed in %s, please check your "
                  "configuration.\n" % (phase, config[phase][phase]))
        sys.exit(1)

    if "genetic_map_file" not in config[phase]:
        Log.error("Missing genetic_map_file for %s in config file.\n%s\n" % (phase, conf_msg))
        sys.exit(1)

    if kwargs.refbuild not in config[phase]["genetic_map_file"]:
        k = ",".join(config[phase]["genetic_map_file"].keys())
        Log.error("is not been setted for %s in config file. The key of genetic_map_file "
                  "can only be:\n%s\n%s\n" % (kwargs.refbuild, phase, k, conf_msg))
        sys.exit(1)

    impute = kwargs.impute_method
    if impute not in config:
        Log.error("Missing '%s' in config file.\n%s\n" % (impute, conf_msg))
        sys.exit(1)

    if impute not in config[impute]:
        Log.error("Missing set '%s' path for phasing.\n%s\n" % (impute, conf_msg))
        sys.exit(1)

    if not file_exists(config[impute][impute]):
        Log.error("%s program is not existed in %s, please check your "
                  "configuration.\n" % (impute, config[impute][impute]))
        sys.exit(1)

    if "reference_panel" not in config[impute]:
        Log.error("Missing reference_panel for %s in config file.\n%s\n" % (impute, conf_msg))
        sys.exit(1)

    if kwargs.refpanel not in config[impute]["reference_panel"]:
        k = ",".join(config[impute]["reference_panel"].keys())
        Log.error("%s is not been setted in config file. The key of reference_panel "
                  "can only be:\n%s\n%s\n" % (kwargs.refpanel, k, conf_msg))
        sys.exit(1)

    for _, v in config[impute]["reference_panel"][kwargs.refpanel].items():
        if not file_exists(v):
            Log.error("%s not exists, please check the configuration file.\n" % v)
            sys.exit(1)

    return


def main():
    """Main function"""
    start_time = datetime.now()

    sys.stderr.write("%s\n" % LONG_DESC)

    kwargs = parse_commandline_args(sys.argv[1:])

    if "config" not in kwargs:
        Log.error("missing YAML configuration files by -C (--conf).\n")
        sys.exit(1)

    with open(kwargs.config) as C:
        config = yaml.load(C)

    checkconfig(config, kwargs)

    if "impute" in sys.argv[1:] and kwargs:
        runfunction.imputation(kwargs, config)

    elapsed_time = datetime.now() - start_time
    Log.info("%s done, %d seconds elapsed.\n" % (sys.argv[1], elapsed_time.seconds))


if __name__ == "__main__":
    main()
