from distutils.core import setup
from setuptools import find_packages
from codecs import open
from os import path

from pyway.version import __version__


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]

setup(
    name='pyway',
    version=__version__,
    description='Pyway is a database versioning and migration tool inspired by Flyway',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jasondcamp/pyway',
    download_url='https://github.com/jasondcamp/pyway/tarball/' + __version__,
    license='GPL',
    classifiers=[
      'Development Status :: 4 - Beta',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'Programming Language :: Python :: 3.11',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Jason Camp',
    install_requires=install_requires,
    author_email='me@jasoncamp.com'
)
