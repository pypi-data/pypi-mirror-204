# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import setup, find_packages
from Mornay import __VERSION__


with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Mornay",
    version=__VERSION__,
    author="DSA",
    description="MornayMornay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    platforms=["any"],
    keywords=["life-science"],
    packages=find_packages(),
    package_dir={"Mornay": "Mornay"},
    install_requires=[
        i.strip() for i in Path("../requirements.txt").read_text("utf-8").splitlines()
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "Mornay=Mornay.Mornay:main",
        ]
    },
)
