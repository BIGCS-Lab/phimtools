pitools: A phasing and imputation tools for NGS data.
=====================================================

Introduction
------------

``pitools`` is a phasing and imputation tools for NGS data, which is the main
core of imputation server: https://imputation.cngb.org/. You can use pitools
as your own imputation pipeline in your local Linux cluster.

Quick start
-----------

pitools use `eagle <https://data.broadinstitute.org/alkesgroup/Eagle/>`__ for phasing 
and `Minimac3 <https://genome.sph.umich.edu/wiki/Minimac3>`__ for imputation.

Installation
~~~~~~~~~~~~

Install the released version by pip:

.. code:: bash

    pip install pitools

Or you may instead want to install the development version from github,
by running:

.. code:: bash

    pip install git+git://github.com/ShujiaHuang/pitools.git#egg=pitools

This command will install pitools in your system and you can use ``pitools`` in
your commandline.

Usage
~~~~~

You can find all the parameter for imputation process by running
``pitools impute --help``:

::

    usage: pitools impute [-h] -C CONFIG [-M IMPUTE_METHOD] [-P PHASE_METHOD] -I IN_VCF
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

Configuration file
~~~~~~~~~~~~~~~~~~

``pitools`` needs a configuration file for setting the path of phasing
program, imputation program, reference version and reference panel.
Here's one of the examples for how to create a config- uration file:
`config.yaml <./tests/config.yaml>`__.

Now you can use ``pitools`` as your powerful imputation pipeline, once you
have finished the setting.

Examples
~~~~~~~~

This command would be enough for most of your jobs.

.. code:: bash

    pitools impute -C config.yaml \
        -I your.vcf.gz \
        -O test_outprefix \
        --refpanel-version 1000G_P3_GRCh37 \
        --reference-build GRCh37 \
        --nCPU 4

What if you just want to preform the imputed process in some specific
regions. Here is an example for running ``pitools`` in genome region:
``21:38347375-38500731`` and ``22:17203103-17439826``.

.. code:: bash

    pitools impute -C config.yaml \
        -I your.vcf.gz \
        -O test_outprefix \
        --refpanel-version 1000G_P3_GRCh37 \
        --reference-build GRCh37 \
        --regions  21:38347375-38500731,22:17203103-17439826 \
        --nCPU 4

PI will perform pre-phasing automatically before perform the imputation
process. But sometimes your input VCF file has been phased already. And
you don't want to run it any more then you can set ``--unprephase``
argument to skip that process.

.. code:: bash

    pitools impute -C config.yaml \
        -I your.vcf.gz \
        -O test_outprefix \
        --refpanel-version 1000G_P3_GRCh37 \
        --reference-build GRCh37 \
        --unprephase \
        --nCPU 4

