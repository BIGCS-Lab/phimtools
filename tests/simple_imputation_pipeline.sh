#!/bin/bash

#########################################
# Author: Shujia Huang                  #
# Date: 2019-05-17                      #
# Version 1.0 a very simple pipeline    #
#########################################

input=$1
config=$2
refbuild=$3
refpanel=$4

pi=/var/lib/docker/USER/huangshujia/project/201905_Imputation_server/bin/pi/venv/bin/pitools

### 
in_file_ext=`basename $input | awk 'BEGIN{FS=".";}{print $(NF-1)"."$NF}'`

# input file must be .vcf.gz
if [ ${in_file_ext} != "vcf.gz" ]; then
   echo "** input file must be *.vcf.gz"
   exit 1
fi

## set output prefix by the name of input file
out_prefix=`basename $input | awk 'BEGIN{FS=".vcf.gz"}{print $1}'`

## The whole pipeline
${pi} impute -C $config -I $input -O ${out_prefix} --refpanel-version ${refpanel} --reference-build ${refbuild} --nCPU 4 && echo "** Imputation by $pi done **"
