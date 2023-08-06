#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages
import os, codecs

MAJOR = 0
MINOR = 1
PATCH = 0
PRE_RELEASE = 'rc'
# Use the following formatting: (major, minor, patch, prerelease)
VERSION = (MAJOR, MINOR, PATCH, PRE_RELEASE)

if os.path.exists('README.rst'):
    # codec is used for consistent encoding
    long_description = codecs.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'), 'r', 'utf-8'
    ).read()

else:
    long_description = "MSAdapter is a toolkit for support the PyTorch model running on Ascend.\n"
    long_description += "Usage: import msadapter.pytorch as ms_torch \n"
    long_description += "OpenI: https://openi.pcl.ac.cn/OpenI/MSAdapter \n"
    long_description += "Email: pcl.openi@pcl.ac.cn"

def req_file(filename, folder=''):
    with open(os.path.join(folder, filename)) as f:
        content = f.readlines()
    return [x.strip() for x in content]

setup(
    name="msadapter",
    version='.'.join(map(str, VERSION[:3])) + ''.join(VERSION[3:]),
    author="Peng Cheng Lab, HUAWEI",
    author_email="pcl.openi@pcl.ac.cn",
    description="MSAdapter is a toolkit for support the PyTorch model running on Ascend.",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://openi.pcl.ac.cn/OpenI/MSAdapter ",
    packages=find_packages(),
    install_requires=req_file("requirements.txt"),
    classifiers=[
        # How mature is this project? Common values are
        #  1 - Planning 2 - Pre-Alpha 3 - Alpha 4 - Beta 5 - Production/Stable 6 - Mature 7 - Inactive
        'Development Status :: 3 - Alpha',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3 :: Only',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",

        # Indicate what your project relates to
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Additionnal Settings
        'Operating System :: OS Independent',
    ],
    license='Apache 2.0',
    )
