#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import os

from parseli import getli

parser = argparse.ArgumentParser(description="Parseli cooks a LinkedIn Profile into JSON")
parser.add_argument('url', nargs='?', metavar='<profile url>',
                    help="url of user's linkedin profile (e.g. http://linkedin.com/in/mekarpeles)")
args = parser.parse_args()
print getli(args.url)
