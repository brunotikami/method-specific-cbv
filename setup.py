#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

__version__ = '0.0.4'

# Package meta-data.
NAME = 'method_specific_views'
DESCRIPTION = 'Django HTTP method-specific class-based views'

REQUIRED = []
if os.path.exists('requirements/base.txt'):
    # What packages are required for this module to be executed?
    REQUIRED = [name for name in open('requirements/base.txt').readlines() if not name.startswith('-e')]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass

        sys.exit()

# Where the magic happens:
setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='ISC',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    cmdclass={
        'publish': PublishCommand,
    },
)
