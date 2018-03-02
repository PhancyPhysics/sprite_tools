#!/usr/bin/env python

from setuptools import setup

try:
    import pypandoc
    longDesc = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    longDesc = open('README.md').read()

setup(name='sprite_tools',
    version = '0.1',
    description = 'Used to extract, create, and animate sprites',
    long_description = longDesc,
    url = 'https://github.com/PhancyPhysics/sprite_tools',
    author = 'Kenneth McIntyre',
    author_email = 'kennethianmcintyre@gmail.com',
    license = 'MIT',
    install_requires = ['opencv-python','numpy','scipy'],
    packages = ['sprite_tools'],
    include_package_data=True,
    zip_safe = False)
