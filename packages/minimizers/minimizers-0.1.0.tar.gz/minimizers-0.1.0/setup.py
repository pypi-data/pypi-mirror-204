import sys

import setuptools

from minimizers.minimizers import __version__

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 6):
    sys.exit(
        "MetaSBT requires Python 3.6 or higher. Your current Python version is {}.{}.{}\n".format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2]
        )
    )

setuptools.setup(
    author="Fabio Cumbo",
    author_email="fabio.cumbo@gmail.com",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    description="A Python package for extracting minimizers from sequence data",
    download_url="https://pypi.org/project/minimizers/",
    entry_points={"console_scripts": ["minimizers=minimizers.minimizers:main"]},
    install_requires=[
        "biopython"
    ],
    keywords=[
        "bioinformatics",
        "minimizers",
        "sketches"
    ],
    license="MIT",
    license_files=["LICENSE"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    name="minimizers",
    packages=setuptools.find_packages(),
    project_urls={
        "Issues": "https://github.com/cumbof/minimizers/issues",
        "Source": "https://github.com/cumbof/minimizers",
    },
    python_requires=">=3.6",
    url="http://github.com/cumbof/minimizers",
    version=__version__,
    zip_safe=False,
)
