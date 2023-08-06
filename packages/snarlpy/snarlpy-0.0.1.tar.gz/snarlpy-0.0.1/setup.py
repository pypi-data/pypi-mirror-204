import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "snarlpy",
    version = "0.0.1",
    author = "felixk1990",
    author_email = "felixuwekramer@proton.me",
    description = "The 'snarlpy' package provides the functionality and a set of examples for the calculation of linkage numbers and optimal cuts of spatially embedded network pairs.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/felixk1990/network-linkage",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.8',
)

from setuptools import setup, find_packages
