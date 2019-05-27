"""Test module for Eagle"""
import yaml
from pi.modules.phasing import eagle as eagle_phasing
from pi.tools.eagle import Eagle
from pi.utils import safe_makedir


out_dir = safe_makedir("./test_eagle")


def test_out_eagle_help_info(config):
    eagle = Eagle(config, reference_version="GRCh37")
    return eagle.help()


def test_phasing_multi_process(config):
    eagle_phasing(config,
                  "data/eagle/EUR_test.vcf.gz",
                  "%s/EUR_test.phased" % out_dir,
                  options=[("numThreads", 4)],
                  reference_version="GRCh37",
                  merge_multi_output=True)
    return


def test_phasing_vcf_format(config):
    eagle_phasing(config,
                  "data/eagle/EUR_test.vcf.gz",
                  "%s/EUR_test.phased" % out_dir,
                  reference_version="GRCh37",
                  merge_multi_output=True)
    return


def test_phasing_PLINK_format(config):
    eagle_phasing(config,
                  "data/eagle/EUR_test",
                  "%s/EUR_test.phased" % out_dir,
                  reference_version="GRCh37",
                  merge_multi_output=False)
    return


if __name__ == "__main__":

    with open("./config.yaml") as C:
        config = yaml.load(C)

    # test_out_eagle_help_info(config)
    # test_phasing_vcf_format(config)
    test_phasing_PLINK_format(config)
    # test_phasing_multi_process(config)
