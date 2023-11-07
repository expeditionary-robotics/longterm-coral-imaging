"""Configuration for the fumes package."""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="loci",
    version="0.0.1",
    author="Victoria Preston",
    author_email='v.preston@northeastern.edu',
    description='Package for collecting, analyzing, and interrogating image and in situ data from coral reef surveys.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "loci"},
    packages=find_packages(where="loci"),
    install_requires=['numpy',
                      'matplotlib',
                      'scipy',
                      ],
    python_requires=">=3.7",
)
