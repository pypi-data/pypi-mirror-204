from setuptools import setup
import sys
import os


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


if sys.platform == 'win32' or os.name == 'nt':
    script = "bin/ncbimetadata.exe"
else:
    script = "bin/ncbimetadata"


setup(
    name="ncbimetadata",
    version="0.0.9",
    description="ncbimetadata is a package for fast fetching and parsing metadata from ncbi database, and more functionalities are on the way!",
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    author="Ryan Alloriadonis",
    author_email="yuantai78@gmail.com",
    url="https://github.com/RyanYuanSun/ncbimetadata",
    platforms=['Linux', 'MacOS X'],
    py_modules=['ncbimetadata'],
    packages=['ncbimetadata'],
    license=readfile('LICENSE'),
    scripts=[script],
    install_requires=[
          'requests',
      ],
    zip_safe=False
)