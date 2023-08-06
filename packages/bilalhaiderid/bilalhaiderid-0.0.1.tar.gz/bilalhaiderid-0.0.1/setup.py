from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'bilalhaiderid'
LONG_DESCRIPTION = 'No technology thats connected to internet is unhackable'

# Setting up
setup(
    name="bilalhaiderid",
    version=VERSION,
    author="BilalHaiderID",
    author_email="bilalhaiderid@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['testing','bilalhaiderid'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
