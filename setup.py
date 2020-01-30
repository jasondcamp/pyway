from setuptools import setup, find_packages
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
    description='Pyway is a database versioning and migration tool inspired on Flyway',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sergiosbx/pyway',
    download_url='https://github.com/sergiosbx/pyway/tarball/' + __version__,
    license='GPL',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Sérgio Ferreira Filho',
    install_requires=install_requires,
    author_email='sergio.ferreira.filho@gmail.com',
    py_modules=['pyway'],
    entry_points={
        'console_scripts': ['pyway=pyway.scripts.main:cli']
    }
)
