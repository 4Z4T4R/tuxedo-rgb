#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tuxedo-rgb",
    version="0.1.0",
    author="Tuxedo RGB Contributors",
    description="GTK4 GUI for controlling RGB keyboard backlighting on Tuxedo laptops",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4Z4T4R/tuxedo-rgb",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyGObject>=3.42.0",
    ],
    entry_points={
        "console_scripts": [
            "tuxedo-rgb=tuxedo_rgb.gui:main",
            "tuxedo-rgb-cli=tuxedo_rgb.cli:main",
        ],
    },
    scripts=["scripts/tuxedo-rgb"],
)
