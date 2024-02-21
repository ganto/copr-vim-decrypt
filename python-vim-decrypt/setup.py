#! /usr/bin/env python3

import setuptools

setuptools.setup(
  name='vimdecrypt',
  version='2.0.0',
  author='Gertjan van Zwieten',
  py_modules=['vimdecrypt'],
  scripts=['vim-decrypt'],
  test_suite='vimdecrypt',
)
