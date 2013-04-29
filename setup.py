#-*- coding: utf-8 -*-

"""
    parseli
    ~~~~~~~
    Dependencies

    Setup
    `````
    $ sudo pip install -e .
    $ sudo rm -rf build
"""

from distutils.core import setup
import os

setup(
    name='parseli',
    version='0.0.46',
    url='',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'parseli',
        ],
    platforms='any',
    scripts=['scripts/parseli'],
    license='LICENSE',
    install_requires=[
        'beautifulsoup >= 3.2.1',
        'requests >= 1.1.0'
    ],
    description="Parseli cooks public LinkedIn profile pages into json.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)
