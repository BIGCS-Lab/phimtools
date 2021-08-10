phimtools: A phasing and imputation tools for NGS data.
=====================================================

Introduction
------------

`phimtools` is a phasing and imputation tools for NGS data, which is the
main core of imputation server: <https://imputation.cngb.org/>. You can
use phimtools as your own imputation pipeline in your local Linux cluster.

Quick start
-----------

phimtools use [eagle](https://data.broadinstitute.org/alkesgroup/Eagle/)
for phasing and [Minimac3](https://genome.sph.umich.edu/wiki/Minimac3)
for imputation.

### Installation

Install the released version by pip:

```bash
pip install phimtools
```

Or you may instead want to install the development version from github,
by running:

```bash
pip install git+git://github.com/ShujiaHuang/phimtools.git#egg=phimtools
```

This command will install phimtools in your system and you can use
`phimtools` in your commandline.

### Usage

You can find all the parameter for imputation process by running
`phimtools impute --help`:

    usage: phimtools impute [-h] -C CONFIG [-M IMPUTE_METHOD] [-P PHASE_METHOD] -I IN_VCF
                     -O OUT_PREFIX --refpanel-version REFPANEL --reference-build
                     REFBUILD [--unprephase] [--regions chr:start-end]
                     [--nCPU NCPU]

    optional arguments:
      -h, --help            show this help message and exit
      -C CONFIG, --conf CONFIG
                            YAML configuration file specifying details information
                            for imputation
      -M IMPUTE_METHOD, --methods IMPUTE_METHOD
                            Tool for imputation. [minimac]
      -P PHASE_METHOD, --prephase-method PHASE_METHOD
                            Tool for pre-phase before imputation. [eagle]
      -I IN_VCF, --input IN_VCF
                            Input one VCF file to analyze. Required
      -O OUT_PREFIX, --outprefix OUT_PREFIX
                            Prefix for output files. Required
      --refpanel-version REFPANEL
                            The version of haplotype data for reference panel.
                            Required
      --reference-build REFBUILD
                            The build version of reference, e.g: GRCh37
      --unprephase          Do not perform pre-phased before the imputation
                            process.
      --regions chr:start-end
                            Skip positions which not in these regions. This
                            parameter could be a list of comma deleimited genome
                            regions(e.g.: chr:start-end,chr:start-end)
      --nCPU NCPU           Number of threads. [1]

### Configuration file

`phimtools` needs a configuration file for setting the path of phasing
program, imputation program, reference version and reference panel.
Here\'s one of the examples for how to create a config- uration file:
[config.yaml](./tests/config.yaml).

Now you can use `phimtools` as your powerful imputation pipeline, once you
have finished the setting.

### Examples

This command would be enough for most of your jobs, `--nCPU` is for
setting the number of threads.

```bash
phimtools impute -C config.yaml \
    -I your.vcf.gz \
    -O test_outprefix \
    --refpanel-version 1000G_P3_GRCh37 \
    --reference-build GRCh37 \
    --nCPU 4
```

What if you just want to preform the imputed process in some specific
regions. Here is an example for running `phimtools` in genome region:
`21:38347375-38500731` and `22:17203103-17439826`.

```bash
phimtools impute -C config.yaml \
    -I your.vcf.gz \
    -O test_outprefix \
    --refpanel-version 1000G_P3_GRCh37 \
    --reference-build GRCh37 \
    --regions  21:38347375-38500731,22:17203103-17439826 \
    --nCPU 4
```

`phimtools` will perform pre-phasing automatically before perform the
imputation process. But sometimes your input VCF file has been phased
already. And you don\'t want to run it again then you can set
`--unprephase` argument to skip that process.

```bash
phimtools impute -C config.yaml \
    -I your.vcf.gz \
    -O test_outprefix \
    --refpanel-version 1000G_P3_GRCh37 \
    --reference-build GRCh37 \
    --unprephase \
    --nCPU 4
```
