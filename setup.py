#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from setuptools import setup, find_packages
from codecs import open

requires = [
    'numpy',
    'pandas',
    'pygame',
]

version = ''
with open('argil/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.md', 'rb', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='argil',
    version=version,
    description="Robot and Crowd simulation",
    long_description=readme,
    author='Jeremy Kerfs',
    author_email='jkerfs@calpoly.edu',
    url='https://github.com/jkerfs/argil',
    packages=find_packages(),
    package_data={'mesa': ['visualization/resources/*']},
    include_package_data=True,
    install_requires=requires,
    keywords='robot crowd dynamic trajectory d3',
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Life',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ),
)