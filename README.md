
phimtools: A phasing and imputation tools for NGS data.
=====================================================

Introduction
------------

`phimtools` is a phasing and imputation tools for NGS data, which is the
main core of imputation server. You can use phimtools as your own imputation 
pipeline in your local Linux cluster.

Quick start
-----------

phimtools use [Eagle](https://data.broadinstitute.org/alkesgroup/Eagle/)
or [beagle](https://faculty.washington.edu/browning/beagle/beagle.html)(requires Java version 8)
for phasing and [Minimac3](https://genome.sph.umich.edu/wiki/Minimac3)
or [Minimac4](https://genome.sph.umich.edu/wiki/Minimac4)
for imputation.

### Installation

Install the released version by pip:

```bash
pip install phimtools
```

This command will install phimtools in your system and you can use
`phimtools` in your commandline.

### Important notes before starting
We have Eagle_v2.4.1 and beagle_5.2 built in phimtools.
However, ensure that Java version 8 (for beagle), and minimac4 (or minimac3) 
softwares are installed in your analysis environment.

Reference_panel or genetic_map files are necessities and should be download from:

- Eagle 
    + download: https://alkesgroup.broadinstitute.org/Eagle/downloads/Eagle_v2.4.1.tar.gz
- beagle
    + genetic_maps: http://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/
- Minimac4
    + install: 
    ```
    git clone https://github.com/statgen/Minimac4.git
    cd Minimac4
    bash install.sh
    ```
    + Detail and Reference Panels: https://genome.sph.umich.edu/wiki/Minimac4

### Usage

You can find all the submodules for phasing and imputation process by running:
`phimtools --help`:

    usage: phimtools {init, impute, eagle, beagle, minimac} [option] ...

    Initialization:
        init     Configure the absolute path for third-party softwares.

    Pipeline:
        impute   (Recommended) Run phasing and imputation pipeline for NGS data.

    Third-party programs:
        eagle    Run eagle independently.
        beagle   Run beagle independently.
        minimac  Run minimac independently (if availabled).


**Before running**:

Eagle/beagle/minimac softwares must be pre-configured (only needs to be configured once) via:

`phimtools init --help`:

    usage: phimtools init [-h] [-e EAGLE] [-b BEAGLE] [-m MINIMAC]

    optional arguments:
      -h, --help            show this help message and exit
      -e EAGLE, --eagle EAGLE
                            Specify the absolute path of the Eagle
      -b BEAGLE, --beagle BEAGLE
                            Specify the absolute path of the beagle
      -m MINIMAC, --minimac MINIMAC
                            Specify the absolute path of the Minimac3/minimac4

or run `phimtools init` to config the built-in Eagle/beagle/Minimac3 softwares, 
which are not recommended !


**impute pipeline**:

Once initialized, recommended phasing-impute pipeline is running:

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
                            Tool for pre-phase before imputation. [eagle, beagle]
      -I IN_VCF, --input IN_VCF
                            Input one VCF file to analyze. Required
      -O OUT_PREFIX, --outprefix OUT_PREFIX
                            Prefix for output files. Required
      --refpanel-version REFPANEL
                            The version of haplotype data for reference panel.
                            Required
      --reference-build REFBUILD
                            The build version of reference, e.g: GRCh37, GRCh38
      --unprephase          Do not perform pre-phased before the imputation
                            process.
      --regions chr:start-end
                            Skip positions which not in these regions. This
                            parameter could be a list of comma deleimited genome
                            regions(e.g.: chr:start-end,chr:start-end)
      --nCPU NCPU           Number of threads. [1]

**Configuration file**

`phimtools impute` needs a configuration file for setting the path of phasing
program, imputation program, reference version and reference panel.
Here\'s one of the examples for how to create a configuration file:
[config.yaml](./tests/config.yaml).


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

**third-party softwares**:
Once initialized, you can run the third-party softwares (Eagle/beagle/minimac) independently by:

`phimtools eagle`

`phimtools beagle`

`phimtools minimac`

Now you can use `phimtools` as your powerful imputation pipeline, once you
have finished the setting.