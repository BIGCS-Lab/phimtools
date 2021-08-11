"""Test module for Minimac3"""
import yaml

from phimtools.utils import safe_makedir
from phimtools.modules.imputation import minimac as minimac_impute
from phimtools.tools.minimac3 import Minimac


out_dir = safe_makedir("./test_impute")


def test_minimac_help_info(config):

    minimac = Minimac(config, reference_panel="1000G_P3_GRCh37")
    return minimac.help()


def test_impute_multi_process(config):
    minimac_impute(config,
                   "data/eagle/EUR_test.vcf.gz",
                   "%s/test.imputed" % out_dir,
                   "22",
                   options=[("cpus", 4)],
                   reference_panel="1000G_P3_GRCh37")


if __name__ == "__main__":

    with open("./config.yaml") as C:
        config = yaml.safe_load(C)

    # test_minimac_help_info(config)
    # test_impute(config)
    test_impute_multi_process(config)
