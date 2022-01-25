"""The pipeline for phasing and imputation process.
Author: Shujia Huang & Chengrui Wang
Date: 2019-2022
"""
import os
import sys
import stat
import argparse
import yaml

from datetime import datetime

from phimtools.log import Log
from phimtools.tools.check import check_vcf_format
from phimtools.utils import file_exists
from phimtools.launch import runfunction
from phimtools.tools.thirdparty import Thirdparty

USER_HOME = os.path.expanduser("~")
PHIMTOOLS_DIR = '.phimtools'
PHIMTOOLS_TOOLS = 'thirdparty.yaml'

VERSION = "1.1.0"
LONG_DESC = """
------------------------------------------------------------------
    phimtools - A program for phasing and imputation analysis.  
------------------------------------------------------------------
        (c) 2019-2022 - Shujia Huang & Chengrui Wang
        Distributed under the GNU GPLv3+ open source license.    
        Version {version}                                                     
        URL = https://github.com/BIGCS-Lab/phimtools
------------------------------------------------------------------
""".format(version=VERSION)


def parse_commandline_args(args):
    """Parse input commandline arguments, handling multiple cases."""

    desc = "phimtools - A pipeline for phasing and imputation analysis."
    parser = argparse.ArgumentParser(description=desc)
    subparser = parser.add_subparsers(help="phimtools supplemental commands")

    # For imputation
    impute_parser = subparser.add_parser("impute", help="Run phasing and "
                                         "imputation pipeline for NGS data.")
    impute_parser.add_argument("-C", "--conf", dest="config", required=True,
                               help="YAML configuration file specifying "
                                    "details information for imputation")
    impute_parser.add_argument("-M", "--methods", dest="impute_method", 
                               default="minimac",
                               help="Tools (minimac, beagle) for imputation. [minimac]")
    impute_parser.add_argument("-P", "--prephase-method", dest="phase_method", 
                               default="beagle",
                               help="Tools (eagle, beagle) for pre-phase "
                                    "before imputation. [beagle]")

    impute_parser.add_argument("-I", "--input", dest="in_vcf", required=True,
                               help="Input one VCF file to analyze. Required")
    impute_parser.add_argument("-O", "--outprefix", dest="out_prefix", 
                               required=True,
                               help="Prefix for output files. Required")
    impute_parser.add_argument("--refpanel-version", dest="refpanel", 
                               required=True,
                               help="The version of haplotype data for "
                               "reference panel. Required")
    impute_parser.add_argument("--reference-build", dest="refbuild", 
                               required=True,
                               help="The build version of reference, "
                               "e.g: GRCh38")

    impute_parser.add_argument("--unprephase", dest="is_unprephase", 
                               action="store_true", help="Do not perform "
                               "pre-phased before the imputation process.")
    impute_parser.add_argument("--regions", metavar="chr:start-end", type=str, 
                               dest="regions", default="", 
                               help="Skip positions which not in these "
                                    "regions. This parameter could be a list "
                                    "of comma deleimited genome regions"
                                    "(e.g.: chr:start-end,chr:start-end)")

    impute_parser.add_argument("--nCPU", dest="nCPU", type=int, default=1, 
                               help="Number of threads. [1]")

    # For phasing
    return parser.parse_args(args)


def init_commandline_args(args):
    """Parse input commandline arguments, handling multiple cases."""

    desc = ("Initialization - Configure the absolute path "
            "for third-party softwares.")
    parser = argparse.ArgumentParser(description=desc)
    subparser = parser.add_subparsers(help="phimtools initialization commands")

    # For third-party softwares configuration
    init_parser = subparser.add_parser("init", 
                                       help="Third-party softwares "
                                       "configuration.")

    init_parser.add_argument("-e", "--eagle", dest="eagle", 
                             help="Specify the absolute path of the Eagle")
    init_parser.add_argument("-b", "--beagle", dest="beagle", 
                             help="Specify the absolute path of the beagle")
    init_parser.add_argument("-m", "--minimac", dest="minimac",
                             help="Specify the absolute path of the "
                             "Minimac3/minimac4")

    return parser.parse_args(args)


def check_config(config, kwargs):
    """Check the most important parameters is setted or not."""

    conf_msg = ("Please find an example: https://github.com/BIGCS-Lab/"
                "phimtools/blob/master/tests/config.yaml")

    phase = kwargs.phase_method
    if phase not in config:
        Log.error("Missing '%s' in config file.\n%s\n" % (phase, conf_msg))
        sys.exit(1)

    if "genetic_map_file" not in config[phase]:
        Log.error("Missing genetic_map_file for "
                  "%s in config file.\n%s\n" % (phase, conf_msg))
        sys.exit(1)

    if kwargs.refbuild not in config[phase]["genetic_map_file"]:
        k = ",".join(config[phase]["genetic_map_file"].keys())
        Log.error("%s is not been setted for %s in config file."
                  " The key of genetic_map_file can "
                  "only be:\n%s\n%s\n" % (kwargs.refbuild, phase, k, conf_msg))
        sys.exit(1)

    impute = kwargs.impute_method
    if impute not in config:
        Log.error("Missing '%s' in config file.\n%s\n" % (impute, conf_msg))
        sys.exit(1)

    if "reference_panel" not in config[impute]:
        Log.error("Missing reference_panel for %s in config file.\n%s\n" % 
                  (impute, conf_msg))
        sys.exit(1)

    if kwargs.refpanel not in config[impute]["reference_panel"]:
        k = ",".join(config[impute]["reference_panel"].keys())
        Log.error("%s is not been setted in config file. "
                  "The key of reference_panel "
                  "can only be:\n%s\n%s\n" % (kwargs.refpanel, k, conf_msg))
        sys.exit(1)

    for _, v in config[impute]["reference_panel"][kwargs.refpanel].items():
        if not file_exists(v):
            Log.error("%s not exists, please check the configuration file.\n" % 
                      v)
            sys.exit(1)
    return


def check_file_exist(file_path):
    if os.path.exists(file_path):
        return(file_path)
    else:
        Log.warn("%s file is missing." % file_path)
        return


def initialization(kwargs2):
    """initialize Eagle/beagle/minimac softwares path"""

    p = os.path.join(USER_HOME, PHIMTOOLS_DIR)
    if not os.path.isdir(p):
        os.mkdir(p, stat.S_IRWXU)  # 0700

    p = os.path.join(p, PHIMTOOLS_TOOLS)

    module_path = os.path.dirname(__file__)

    with open(p, 'w') as toolstore:
        if kwargs2.eagle and check_file_exist(kwargs2.eagle):
            Log.info("Program Eagle (%s) be found and configured." % os.path.abspath(kwargs2.eagle))
            eagle_path = os.path.abspath(kwargs2.eagle)
        else:
            Log.warn("Program Eagle not find, set the built-in Eagle.")
            eagle_path = module_path + '/third_party/eagle'

        if kwargs2.beagle and check_file_exist(kwargs2.beagle):
            Log.info("Program beagle (%s) be found and configured." % os.path.abspath(kwargs2.beagle))
            beagle_path = os.path.abspath(kwargs2.beagle)
        else:
            Log.warn("Program beagle not find, set the built-in beagle.")
            beagle_path = module_path + '/third_party/beagle.28Jun21.220.jar'

        if kwargs2.minimac and check_file_exist(kwargs2.minimac):
            Log.info("Program minimac (%s) be found and configured." % os.path.abspath(kwargs2.minimac))
            minimac_path = os.path.abspath(kwargs2.minimac)
        else:
            Log.warn("Program minimac3/4 is not found, set the built-in "
                     "Minimac3, consequently. The built-in Minimac3 is not "
                     "recommended, please visit "
                     "https://genome.sph.umich.edu/wiki/Minimac4 to install "
                     "to your server and config it via <phimtools init -m "
                     "/path/to/install/minimac>")
            minimac_path = module_path + '/third_party/Minimac3'
        
        if not os.access(eagle_path, os.X_OK):
            os.chmod(eagle_path, stat.S_IRUSR + stat.S_IXUSR)  # 0500
        if not os.access(minimac_path, os.X_OK):
            os.chmod(minimac_path, stat.S_IRUSR + stat.S_IXUSR)  # 0500

        tool_obj = {
            "eagle": eagle_path,
            "beagle": beagle_path,
            "minimac": minimac_path
        }

        yaml.dump(tool_obj, toolstore)

    os.chmod(p, stat.S_IRUSR + stat.S_IWUSR)  # 0600
    Log.info("Eagle/beagle/minimac softwares are configured done!")


def check_yaml():
    yaml_file = os.path.join(USER_HOME, PHIMTOOLS_DIR, PHIMTOOLS_TOOLS)
    if not os.path.isfile(yaml_file):
        Log.error("Please run <phimtools init> to config "
                  "Eagle/beagle/minimac softwares firstly.")
        sys.exit(1)
    else:
        with open(yaml_file, 'r') as ToolsPath:
            toolstore = yaml.load(ToolsPath, Loader=yaml.FullLoader)
            for p in toolstore.keys():
                if not os.path.isfile(toolstore[p]):
                    Log.error("Program (%s) is not existed." % toolstore[p])
                    Log.error("Please run <phimtools init> to re-config "
                              "Eagle/beagle/minimac softwares.")
                    sys.exit(1)
            return toolstore


def phaseImpute(kwargs):
    """Phase and impute function"""

    start_time = datetime.now()
    toolstore = check_yaml()

    if "config" not in kwargs:
        Log.error("missing YAML configuration files by -C (--conf).\n")
        sys.exit(1)

    with open(kwargs.config) as C:
        config = yaml.load(C, Loader=yaml.FullLoader)

    check_config(config, kwargs)

    if "impute" in sys.argv[1:] and kwargs:
        check_vcf_format(kwargs.in_vcf)
        runfunction.imputation(kwargs, config, toolstore)

    elapsed_time = datetime.now() - start_time
    Log.info("%s successfully done, %d seconds elapsed.\n" % 
             (sys.argv[1], elapsed_time.seconds))


def run_thirdparty(param):
    """Run eagle/beagle/minimac independently"""

    toolstore = check_yaml()
    eagle_program = Thirdparty(toolstore, param)
    eagle_program.run()


def main():
    """
usage: phimtools {init, impute, eagle, beagle, minimac} [option] ...

    Initialization:
        init     Configure the absolute path for third-party softwares.

    Pipeline:
        impute   (Recommended) Run phasing and imputation pipeline for NGS data.
            
    Third-party programs:
        eagle    Run eagle independently.
        beagle   Run beagle independently.
        minimac  Run minimac independently (if availabled).
    """

    sys.stderr.write("%s\n" % LONG_DESC)

    if len(sys.argv) == 1:
        Log.warn(main.__doc__)
        sys.exit(1)
    else:
        if sys.argv[1] == "init":
            kwargs2 = init_commandline_args(sys.argv[1:])
            initialization(kwargs2)
        elif sys.argv[1] == "impute":
            kwargs = parse_commandline_args(sys.argv[1:])
            phaseImpute(kwargs)
        elif sys.argv[1] in ["eagle", "beagle", "minimac"]:
            run_thirdparty(sys.argv[1:])
        else:
            Log.warn(main.__doc__)
            sys.exit(1)


if __name__ == "__main__":
    main()
