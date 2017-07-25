#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

description = 'A curses application using sqlite and pyaml'

setup(
        name='PyCurses',
        version='0.4.0',
        author='Sam Whang',
        author_email='sangwoowhang@gmail.com',
        maintainer='Sam Whang',
        maintainer_='sangwoowhang@gmail.com',
        keywords='Curses, Python, Yaml, SQLite',
        description=description,
        license='MIT',
        long_description=description,
        url='https://github.com/whitegreyblack/PyCurses',
        install_requires=['yaml'],
)
