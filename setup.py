#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2014 solute GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import setuptools

setuptools.setup(
    name='python-solute-epfl',
    version='0.43',
    author='Gunter Bach',
    author_email='gb@solute.de',
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=[],
    url='https://github.com/solute/pyramid_epfl/',
    license='LICENSE.txt',
    description='The EPFL Python Frontend Logic.',
    long_description=open('README.md').read(),
    install_requires=[
        "pyramid >= 1.4",
        "Jinja2 >= 2.7.2",
        "pyramid_jinja2 >= 1.10",
        "pyramid_webassets",
        "ujson >= 1.33",
        "pytz >= 2014.4",
        "python-dateutil",
        "redis",
        "statsd",
        "requests",
        "collections2",
        "Pillow",
    ],
    tests_require=[
        "pytest",
        "lxml",
    ],
    setup_requires=[
        "pytest-runner",
        "setuptools-git",
    ],
    entry_points="""\
    [pyramid.scaffold]
    pyramid_epfl_starter=solute.epfl.scaffolds:EPFLStarterTemplate
    pyramid_epfl_tutorial=solute.epfl.scaffolds:EPFLTutorialTemplate
    """
)
