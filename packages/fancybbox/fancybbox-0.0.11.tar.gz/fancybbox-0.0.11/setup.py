from setuptools import setup, find_packages
import codecs
import os


def readme():
    with open('README.md') as f:
        README = f.read()
    return README

VERSION = '0.0.11'
DESCRIPTION = 'Fancy Bounding Box - Rectangle for Object Detection'

# Setting up
setup(
    name="fancybbox",
    version=VERSION,
    author="Prashant27050 (Prashant Verma)",
    author_email="prashant27050@gmail.com",
    long_description_content_type='text/markdown',
    description=DESCRIPTION,
    long_description= readme(),
    packages=find_packages(),
    install_requires=['opencv-python'],
    keywords=['python', 'image processing', 'bbox', 'bbox regtangle', 'fancy rectangle', 'bounding box'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)