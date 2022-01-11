#!/bin/bash
phimtools impute -P beagle -M minimac -I data/beagle/test_input.vcf.gz -O z1 -C config.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 8
phimtools impute -P eagle -M minimac -I data/beagle/test_input.vcf.gz -O z2 -C config.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 8

