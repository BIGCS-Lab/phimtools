"""Test module for Minimac3"""
import yaml

from pi.utils import safe_makedir
from pi.modules.imputation import minimac as minimac_impute
from pi.tools.minimac3 import Minimac


out_dir = safe_makedir("./test_impute")


def test_minimac_help_info(config):

    minimac = Minimac(config, reference_panel="1000G_P3_GRCh37")
    return minimac.help()


def test_impute_multi_process(config):
    minimac_impute(config,
                   "data/minimac/targetStudy.vcf",
                   "%s/test.imputed" % out_dir,
                   options=[("--cpus", 4)],
                   reference_panel="test_panel_GRCh37",
                   reference_version="GRCh37",
                   merge_multi_output=True,
                   is_prephase=False)


def test_impute(config):
    minimac_impute(config,
                   "data/minimac/targetStudy.vcf",
                   "%s/test.imputed" % out_dir,
                   reference_panel="test_panel_GRCh37",
                   reference_version="GRCh37",
                   merge_multi_output=True,
                   is_prephase=False)

    return


if __name__ == "__main__":

    with open("./config.yaml") as C:
        config = yaml.safe_load(C)

    # test_minimac_help_info(config)
    # test_impute(config)
    test_impute_multi_process(config)
