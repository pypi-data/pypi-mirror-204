from setuptools import setup


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="ncbimetadata",
    version="0.1.2",
    description="ncbimetadata is a package for fast fetching and parsing metadata from ncbi database, and more functionalities are on the way!",
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    author="Ryan Alloriadonis",
    author_email="yuantai78@gmail.com",
    url="https://github.com/RyanYuanSun/ncbimetadata",
    py_modules=['ncbimetadata'],
    python_requires='>3',
    packages=['ncbimetadata'],
    license=readfile('LICENSE'),
    install_requires=[
          'requests',
      ],
    entry_points={
        'console_scripts': ['ncbimetadata=ncbimetadata:main']
        },
)