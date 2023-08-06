
import setuptools
import re
import os
import sys


setuptools.setup(
    name="neural-diffeqs",
    version="0.3.0",
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard@broadinstitute.org",
    url=None,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="Neural differential equations made easy.",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy==1.22.4",
        "torch>=2.0.0",
        "torch-nets>=0.0.4",
        "torchsde>=0.2.5",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
