"""Setup file and install script for phasing and imputation for NGS data.

Version 0.1.0 (May 22, 2019)
Copyright (c) 2019 Shujia Huang
"""
try:
    from setuptools import setup, find_packages
    _has_setuptools = True
except ImportError:
    from distutils.core import setup, find_packages


DESCRIPTION = "PI: A python package for phasing and imputation NGS data."
DISTNAME = 'pi'
MAINTAINER = 'Shujia Huang'
MAINTAINER_EMAIL = 'huangshujia9@gmail.com'
URL = 'https:'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = ''
VERSION = "0.1.0"
