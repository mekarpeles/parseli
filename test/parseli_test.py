#-*- coding: utf-8 -*-

"""
    parseli.test
    ~~~~~~~~~~~~
    nosetests for the parseli pkg

    :copyright: (c) 2012 by Mek - Ark.com
    :license: BSD, see LICENSE for more details.
"""

import os
import json
import unittest
from BeautifulSoup import BeautifulSoup
from parseli import getli, crawli, parseli

EXAMPLE_FILENAME = 'test/example.html'
EXAMPLE_FILE = open(EXAMPLE_FILENAME, 'r').read()
EXAMPLE_URL = "http://in.linkedin.com/in/abesh"
EXAMPLE_DATA = \
    {'education': [
        {'degree': u'B.E.',
         'dtend': u'2003-12-31',
         'dtstart': u'1999-01-01',
         'institution': u'National Institute of Technology, Trichy',
         'major': u'Mechanical Engineering'},
        {'degree': '',
         'dtend': u'1998-12-31',
         'dtstart': u'1996-01-01',
         'institution': u'St Xaviers School Durgapur',
         'major': ''}],
     'employment': [
        {'current': 1,
         'date': {'end': '', 'start': u'2009-10-01'},
         'institution': u'IBM',
         'location': '',
         'title': u'SAP MII Integration Architect'},
        {'current': 0,
         'date': {'end': u'2009-10-01', 'start': u'2005-11-01'},
         'institution': u'SAP Labs India Pvt. Ltd.',
         'location': '',
         'title': u'Principal Software Engineer'},
        {'current': 0,
         'date': {'end': u'2005-10-01', 'start': u'2004-07-01'},
         'institution': u'Iflex Solutions',
         'location': '',
         'title': u'Oracle DBA'},
        {'current': 0,
         'date': {'end': u'2004-07-01', 'start': u'2003-07-01'},
         'institution': u'Thermax Babcock &amp; Wilcox Ltd.',
         'location': '',
         'title': u'Project Engineer'}],
     'headline': u'SAP MII Integration &amp; Application Architect, SAP Press Author and SAP Mentor',
     'id': '11403419',
     'industry': u'Computer Software',
     'location': {'area': u'Kolkata Area, India',
                  'locality': u'Kolkata, West Bengal, India'},
     'name': {'family-name': u'Bhattacharjee', 'given-name': u'Abesh'},
     'viewers': []}

class ParseliSageRosemaryTime_Test(unittest.TestCase):
    
    def test_crawli(self):
        jsn = getli(EXAMPLE_URL)
        del jsn['url']
        self.assertTrue(EXAMPLE_DATA == jsn,
                        "Tests data does not match live data from LinkedIn")

    def test_getli(self):
        soup1 = crawli(EXAMPLE_URL)
        soup2 = BeautifulSoup(EXAMPLE_FILE)
        p1 = parseli(soup1)
        p2 = parseli(soup2)
        # urls removed since not a good indicator of match (/pub v. /in v. id)
        del p1['url']
        del p2['url']
        self.assertTrue(p1 == p2,
                        "Expected results of parseli to be the same " \
                            "for realtime + test date but they weren't")

    def test_parseli(self):
        soup = BeautifulSoup(EXAMPLE_FILE)
        jsn = parseli(soup)
        del jsn['url']
        self.assertTrue(EXAMPLE_DATA == jsn,
                        "Example data does not match the results of " \
                            "paresli on example file")

