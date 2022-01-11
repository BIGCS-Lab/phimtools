"""Release and publish the package to PyPI.

Author: Shujia Huang
Date: 2021-04-30
"""
import importlib
from subprocess import call

spec = importlib.util.spec_from_file_location("_", "./setup.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

call(["python", "setup.py", "sdist"])
tarball = "dist/{}-{}.tar.gz".format(module.meta.__DISTNAME__, module.meta.__VERSION__)
call(["twine", "upload", "-r", "pypi", tarball])

