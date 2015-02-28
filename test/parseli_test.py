#-*- coding: utf-8 -*-

"""
    parseli.test
    ~~~~~~~~~~~~
    nosetests for the parseli pkg

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import os
import json
import unittest
from BeautifulSoup import BeautifulSoup
from parseli import getli, crawli, parseli

EXAMPLE_FILENAME = 'test/example.html'
EXAMPLE_URL = "http://in.linkedin.com/in/mekarpeles"

class ParseliSageRosemaryTime_Test(unittest.TestCase):
    
    def test_crawli(self):
        jsn = getli(EXAMPLE_URL)
        del jsn['url']
        self.assertTrue(jsn['name']['full-name'] == 'Mek Karpeles',
                        "Tests data does not match live data from LinkedIn")

