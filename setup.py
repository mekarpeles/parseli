#-*- coding: utf-8 -*-

"""
    parseli
    ~~~~~~~

    Setup
    `````

    $ TODO
"""

from distutils.core import setup

setup(
    name='parseli',
    version='0.1.2',
    url='',
    author='mek',
    author_email='mek@ark.com',
    packages=[
        'parseli',
        'parseli.test'
        ],
    platforms='any',
    scripts=[],
    license='LICENSE',
    install_requires=[
        'BeautifulSoup >= 3.2.0',
        'nose >= 1.1.2'
    ],
    description="Crawls LinkedIn urls and returns json.",
    long_description=open('README.md').read(),
)
