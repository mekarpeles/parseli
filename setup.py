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

setup(
    name='parseli',
    version='0.0.4',
    url='',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'parseli',
        'test'
        ],
    platforms='any',
    scripts=['scripts/parseli'],
    license='LICENSE',
    install_requires=[
        'beautifulsoup',
    ],
    description="Parseli cooks public LinkedIn profile pages into json.",
    long_description=open('README.md').read(),
)
