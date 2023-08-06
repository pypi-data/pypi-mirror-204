#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (3, 0):
    raise NotImplementedError("you need python3 for honeypot.py")

setup(name='honeypot',
      version='0.1.1',
      description='bee approved utilities',
      py_modules=['honeypot'],
      entry_points={
          'console_scripts': [
              'b = honeypot:Honeypot',
          ],
      },
      license="AGPLv3",
      platforms='any',
      install_requires = [
          'flask',
          'prompt_toolkit',
          'rich'
      ])
