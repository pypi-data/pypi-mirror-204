from setuptools import setup


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="ncbimetadata",
    version="0.0.3",
    description="ncbimetadata is a package for fast fetching and parsing metadata from ncbi database, and more functionalities are on the way!",
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    author="Ryan Alloriadonis",
    author_email="yuantai78@gmail.com",
    url="https://github.com/RyanYuanSun/ncbi_metadata_parser",
    py_modules=['ncbimetadata'],
    license=readfile('LICENSE'),
    scripts=['bin/ncbimetadata'],
    install_requires=[
          'requests',
      ],
    zip_safe=False
)