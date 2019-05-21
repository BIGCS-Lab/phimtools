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

if __name__ == "__main__":
    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=(open("README.md").read()),
          license=LICENSE,
          url=URL,
          download_url=DOWNLOAD_URL,
          packages=find_packages(),
          install_requires=[
              'pyaml',
          ],
          version=VERSION,
          include_package_data=True,
          classifiers=[
             'Intended Audience :: Science/Research',
             'Programming Language :: Python :: 2.7',
             'Programming Language :: Python :: 3.4',
             'License :: OSI Approved :: BSD License',
             'Topic :: Scientific/Engineering :: Bio-Informatics',
             'Topic :: Scientific/Engineering :: Tools',
             'Topic :: Multimedia :: WGS',
             'Operating System :: POSIX',
             'Operating System :: Linux/Unix',
             'Operating System :: MacOS'],
          )
