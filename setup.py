#!/usr/bin/env python

from setuptools import setup

try:
    import pypandoc
    longDesc = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    longDesc = open('README.md').read()

setup(name='sprite_tools',
    version = '0.1.0',
    description = 'Used to extract, create, and animate sprites',
    long_description = longDesc,
    url = 'https://github.com/PhancyPhysics/sprite_tools',
    download_url = 'https://github.com/PhancyPhysics/sprite_tools/archive/0.1.0.tar.gz',
    author = 'Kenneth McIntyre',
    author_email = 'kennethianmcintyre@gmail.com',
    license = 'MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Editors :: Raster-Based',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
    ],
    keywords = 'sprite frame animator animation extractor graphics transform',
    install_requires = ['opencv-python','numpy','scipy'],
    packages = ['sprite_tools'],
    include_package_data=True,
    zip_safe = False)


