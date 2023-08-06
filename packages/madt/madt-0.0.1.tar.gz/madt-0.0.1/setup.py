from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here,"README.md"),encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Processing open-source amplicon database for ecology'
LONG_DESCRIPTION = 'A package that allows to download, quality control, file error-correction and match of open-source amplicon data'

setup(
    name='madt',
    version=VERSION,
    packages=find_packages(),
    author="Yufei Zeng",
    author_email="yfzeng0827@hotmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'madt_DataIndex = madt.madt_DataIndex:main',
            'madt_LibCheck = madt.madt_LibCheck:main',
            'madt_LipMap = madt.madt_LipMap:main'
        ]
    },
    keywords=['python', 'bioinformatic', 'amplicon', 'ecology'],
    install_requires=[
        'biopython',
        'pandas',
        'seqkit',
        'bbmap'
    ]
)
