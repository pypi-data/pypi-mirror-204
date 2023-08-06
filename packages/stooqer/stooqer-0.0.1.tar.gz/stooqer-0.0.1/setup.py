from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Stooq data download into pandas DataFrame'

# Setting up
setup(
    name="stooqer",
    version=VERSION,
    author="Septixu (Michał Lachowicz)",
    author_email="<michal.lachowicz@protnmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'stock', 'stooq', 'finance'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)