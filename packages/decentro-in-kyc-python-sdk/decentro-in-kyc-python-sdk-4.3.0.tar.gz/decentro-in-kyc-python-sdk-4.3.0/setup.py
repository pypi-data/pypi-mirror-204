# coding: utf-8

"""
    decentro-in-kyc

    KYC & Onboarding

    The version of the OpenAPI document: 1.0.0
    Contact: admin@decentro.tech
    Created by: https://decentro.tech
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "decentro-in-kyc-python-sdk"
VERSION = "4.3.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

# read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

REQUIRES = [
    "certifi >= 2022.12.7",
    "frozendict ~= 2.3.4",
    "python-dateutil ~= 2.7.0",
    "setuptools >= 21.0.0",
    "typing_extensions ~= 4.3.0",
    "urllib3 ~= 1.26.7",
    "validators ~= 0.20.0",]

setup(
    name=NAME,
    version=VERSION,
    description="decentro-in-kyc",
    author="Decentro",
    author_email="admin@decentro.tech",
    url="https://decentro.tech",
    keywords=["decentro-in-kyc"],
    license="MIT",
    python_requires=">=3.7",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
