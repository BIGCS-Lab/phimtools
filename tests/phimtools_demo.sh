#!/bin/bash
phimtools impute -P beagle -M minimac -I data/beagle/test_input.vcf.gz -O z1 -C config.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 8
phimtools impute -P eagle -M minimac -I data/beagle/test_input.vcf.gz -O z2 -C config.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 8

#phimtools impute -P beagle -M minimac -I data/beagle/test_input.vcf.gz -O z1 -C config_wcr.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 4
#phimtools impute -P eagle -M minimac -I data/beagle/test_input.vcf.gz -O z2 -C config_wcr.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 4
#phimtools impute --unprephase -M minimac -I data/beagle/test_input.vcf.gz -O z3 -C config_wcr.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 4
#phimtools impute -P beagle -M minimac -I data/beagle/test_input.vcf.gz -O z4 -C config_wcr.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 4 --regions 22:20000000-40000000
#phimtools impute -P eagle -M minimac -I data/beagle/test_input.vcf.gz -O z5 -C config_wcr.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 4 --regions 22:20000000-40000000
#phimtools impute --unprephase -M minimac -I data/beagle/test_input.vcf.gz -O z6 -C config_wcr.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 4 --regions 22:20000000-40000000

## merge_files: TypeError: '<' not supported between instances of 'FileForQueueing' and 'FileForQueueing'
#phimtools impute --unprephase -M minimac -I data/beagle/test.21-22.vcf.gz -O x1 -C config_wcr.yaml --refpanel-version test_panel --reference-build GRCh38 --nCPU 4
