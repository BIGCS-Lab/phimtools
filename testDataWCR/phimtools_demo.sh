#!/bin/bash
phimtools impute -P beagle -M minimac -I bigcs_test.22.vcf.gz -O zzz1 -C config_demoWCR.yaml --refpanel-version BIGCS_test --reference-build GRCh38 --nCPU 8
phimtools impute -P eagle -M minimac -I bigcs_test.22.vcf.gz -O zzz2 -C config_demoWCR.yaml --refpanel-version BIGCS_test --reference-build GRCh38 --nCPU 8

