Parseli
=======

![Build Status](https://travis-ci.org/mekarpeles/parseli.png)

A suite of modules for parsing linkedin public pages into clean json

Installation
------------

   pip install parseli

Demo
----

### Command Line

Retrieve

    # by default, assumes the prefix http://linkedin.com/in/
    $ parseli mekarpeles
    {'name': {'given-name': u'Mek', 'family-name': u'Karpeles'}, 'headline': u'Founder at Hackerlist', 'similar': [u'http://www.linkedin.com/in/jeffweiner08', u'http://www.linkedin.com/in/sbalaban?trk=pub-pbmap', u'http://www.linkedin.com/in/sbalaban?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelsiedlecki?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelsiedlecki?trk=pub-pbmap', u'http://www.linkedin.com/pub/zephyr-pellerin/39/938/515?trk=pub-pbmap', u'http://www.linkedin.com/pub/zephyr-pellerin/39/938/515?trk=pub-pbmap', u'http://www.linkedin.com/in/turian?trk=pub-pbmap', u'http://www.linkedin.com/in/turian?trk=pub-pbmap', u'http://www.linkedin.com/in/kevingao1?trk=pub-pbmap', u'http://www.linkedin.com/in/kevingao1?trk=pub-pbmap', u'http://www.linkedin.com/pub/zachary-crockett/24/568/521?trk=pub-pbmap', u'http://www.linkedin.com/pub/zachary-crockett/24/568/521?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelazamloot?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelazamloot?trk=pub-pbmap', u'http://www.linkedin.com/in/jjuran?trk=pub-pbmap', u'http://www.linkedin.com/in/jjuran?trk=pub-pbmap', u'http://www.linkedin.com/pub/gavin-knight/46/732/2b1?trk=pub-pbmap', u'http://www.linkedin.com/pub/gavin-knight/46/732/2b1?trk=pub-pbmap', u'http://www.linkedin.com/in/sashyrichmond?trk=pub-pbmap', u'http://www.linkedin.com/in/sashyrichmond?trk=pub-pbmap'], 'industry': u'Internet', 'url': 'http://linkedin.com/profile?id=112557365', 'location': {'area': '', 'locality': u'San Francisco Bay Area'}, 'education': [{'major': u'Computer Science', 'dtstart': u'2010-01-01', 'dtend': u'2015-12-31', 'institution': u'Unviersity of Delaware', 'degree': u'Ph.D Computer and Information Systems (On Leave)'}, {'major': u'Computer Science', 'dtstart': u'2006-01-01', 'dtend': u'2010-12-31', 'institution': u'University of Vermont', 'degree': u'BS Computer Science'}, {'major': '', 'dtstart': u'2002-01-01', 'dtend': u'2006-12-31', 'institution': u'Cheshire High School', 'degree': ''}], 'employment': [{'current': 1, 'date': {'start': u'2012-12-01', 'end': ''}, 'location': u'San Francisco Bay Area', 'institution': u'Hackerlist', 'title': u'Founder and CEO'}, {'current': 0, 'date': {'start': u'2011', 'end': u'2012-10-01'}, 'location': u'San Francisco', 'institution': u'Hyperink', 'title': u'Principal Architect'}, {'current': 0, 'date': {'start': u'2010', 'end': u'2011'}, 'location': u'San Francisco', 'institution': u'Babo Labs', 'title': u'Co-Founder, CTO'}, {'current': 0, 'date': {'start': u'2010-08-01', 'end': u'2011-08-01'}, 'location': '', 'institution': u'University of Delaware', 'title': u'Ph.D Candidate'}, {'current': 0, 'date': {'start': u'1998', 'end': u'2011'}, 'location': u'United States', 'institution': u'Hackathons', 'title': u'Hacker'}, {'current': 0, 'date': {'start': u'2009', 'end': u'2010'}, 'location': '', 'institution': u'University of Vermont', 'title': u'CSSA President'}, {'current': 0, 'date': {'start': u'2007', 'end': u'2009'}, 'location': '', 'institution': u'MicroStrain, Inc.', 'title': u'Intern'}], 'id': '112557365', 'viewers': []}

    $ parseli http://linkedin.com/in/mekarpeles
    {'name': {'given-name': u'Mek', 'family-name': u'Karpeles'}, 'headline': u'Founder at Hackerlist', 'similar': [u'http://www.linkedin.com/in/jeffweiner08', u'http://www.linkedin.com/in/sbalaban?trk=pub-pbmap', u'http://www.linkedin.com/in/sbalaban?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelsiedlecki?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelsiedlecki?trk=pub-pbmap', u'http://www.linkedin.com/pub/zephyr-pellerin/39/938/515?trk=pub-pbmap', u'http://www.linkedin.com/pub/zephyr-pellerin/39/938/515?trk=pub-pbmap', u'http://www.linkedin.com/in/turian?trk=pub-pbmap', u'http://www.linkedin.com/in/turian?trk=pub-pbmap', u'http://www.linkedin.com/in/kevingao1?trk=pub-pbmap', u'http://www.linkedin.com/in/kevingao1?trk=pub-pbmap', u'http://www.linkedin.com/pub/zachary-crockett/24/568/521?trk=pub-pbmap', u'http://www.linkedin.com/pub/zachary-crockett/24/568/521?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelazamloot?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelazamloot?trk=pub-pbmap', u'http://www.linkedin.com/in/jjuran?trk=pub-pbmap', u'http://www.linkedin.com/in/jjuran?trk=pub-pbmap', u'http://www.linkedin.com/pub/gavin-knight/46/732/2b1?trk=pub-pbmap', u'http://www.linkedin.com/pub/gavin-knight/46/732/2b1?trk=pub-pbmap', u'http://www.linkedin.com/in/sashyrichmond?trk=pub-pbmap', u'http://www.linkedin.com/in/sashyrichmond?trk=pub-pbmap'], 'industry': u'Internet', 'url': 'http://linkedin.com/profile?id=112557365', 'location': {'area': '', 'locality': u'San Francisco Bay Area'}, 'education': [{'major': u'Computer Science', 'dtstart': u'2010-01-01', 'dtend': u'2015-12-31', 'institution': u'Unviersity of Delaware', 'degree': u'Ph.D Computer and Information Systems (On Leave)'}, {'major': u'Computer Science', 'dtstart': u'2006-01-01', 'dtend': u'2010-12-31', 'institution': u'University of Vermont', 'degree': u'BS Computer Science'}, {'major': '', 'dtstart': u'2002-01-01', 'dtend': u'2006-12-31', 'institution': u'Cheshire High School', 'degree': ''}], 'employment': [{'current': 1, 'date': {'start': u'2012-12-01', 'end': ''}, 'location': u'San Francisco Bay Area', 'institution': u'Hackerlist', 'title': u'Founder and CEO'}, {'current': 0, 'date': {'start': u'2011', 'end': u'2012-10-01'}, 'location': u'San Francisco', 'institution': u'Hyperink', 'title': u'Principal Architect'}, {'current': 0, 'date': {'start': u'2010', 'end': u'2011'}, 'location': u'San Francisco', 'institution': u'Babo Labs', 'title': u'Co-Founder, CTO'}, {'current': 0, 'date': {'start': u'2010-08-01', 'end': u'2011-08-01'}, 'location': '', 'institution': u'University of Delaware', 'title': u'Ph.D Candidate'}, {'current': 0, 'date': {'start': u'1998', 'end': u'2011'}, 'location': u'United States', 'institution': u'Hackathons', 'title': u'Hacker'}, {'current': 0, 'date': {'start': u'2009', 'end': u'2010'}, 'location': '', 'institution': u'University of Vermont', 'title': u'CSSA President'}, {'current': 0, 'date': {'start': u'2007', 'end': u'2009'}, 'location': '', 'institution': u'MicroStrain, Inc.', 'title': u'Intern'}], 'id': '112557365', 'viewers': []}

### Python

    >>> import parseli
    >>> parseli.getli('http://linkedin.com/in/mekarpeles')
    <Storage {'name': {'given-name': u'Mek', 'family-name': u'Karpeles'}, 'headline': u'Founder at Hackerlist', 'similar': [u'http://www.linkedin.com/in/jeffweiner08', u'http://www.linkedin.com/in/sbalaban?trk=pub-pbmap', u'http://www.linkedin.com/in/sbalaban?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelsiedlecki?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelsiedlecki?trk=pub-pbmap', u'http://www.linkedin.com/pub/zephyr-pellerin/39/938/515?trk=pub-pbmap', u'http://www.linkedin.com/pub/zephyr-pellerin/39/938/515?trk=pub-pbmap', u'http://www.linkedin.com/in/turian?trk=pub-pbmap', u'http://www.linkedin.com/in/turian?trk=pub-pbmap', u'http://www.linkedin.com/in/kevingao1?trk=pub-pbmap', u'http://www.linkedin.com/in/kevingao1?trk=pub-pbmap', u'http://www.linkedin.com/pub/zachary-crockett/24/568/521?trk=pub-pbmap', u'http://www.linkedin.com/pub/zachary-crockett/24/568/521?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelazamloot?trk=pub-pbmap', u'http://www.linkedin.com/in/michaelazamloot?trk=pub-pbmap', u'http://www.linkedin.com/in/jjuran?trk=pub-pbmap', u'http://www.linkedin.com/in/jjuran?trk=pub-pbmap', u'http://www.linkedin.com/pub/gavin-knight/46/732/2b1?trk=pub-pbmap', u'http://www.linkedin.com/pub/gavin-knight/46/732/2b1?trk=pub-pbmap', u'http://www.linkedin.com/in/sashyrichmond?trk=pub-pbmap', u'http://www.linkedin.com/in/sashyrichmond?trk=pub-pbmap'], 'industry': u'Internet', 'url': 'http://linkedin.com/profile?id=112557365', 'location': {'area': '', 'locality': u'San Francisco Bay Area'}, 'education': [{'major': u'Computer Science', 'dtstart': u'2010-01-01', 'dtend': u'2015-12-31', 'institution': u'Unviersity of Delaware', 'degree': u'Ph.D Computer and Information Systems (On Leave)'}, {'major': u'Computer Science', 'dtstart': u'2006-01-01', 'dtend': u'2010-12-31', 'institution': u'University of Vermont', 'degree': u'BS Computer Science'}, {'major': '', 'dtstart': u'2002-01-01', 'dtend': u'2006-12-31', 'institution': u'Cheshire High School', 'degree': ''}], 'employment': [{'current': 1, 'date': {'start': u'2012-12-01', 'end': ''}, 'location': u'San Francisco Bay Area', 'institution': u'Hackerlist', 'title': u'Founder and CEO'}, {'current': 0, 'date': {'start': u'2011', 'end': u'2012-10-01'}, 'location': u'San Francisco', 'institution': u'Hyperink', 'title': u'Principal Architect'}, {'current': 0, 'date': {'start': u'2010', 'end': u'2011'}, 'location': u'San Francisco', 'institution': u'Babo Labs', 'title': u'Co-Founder, CTO'}, {'current': 0, 'date': {'start': u'2010-08-01', 'end': u'2011-08-01'}, 'location': '', 'institution': u'University of Delaware', 'title': u'Ph.D Candidate'}, {'current': 0, 'date': {'start': u'1998', 'end': u'2011'}, 'location': u'United States', 'institution': u'Hackathons', 'title': u'Hacker'}, {'current': 0, 'date': {'start': u'2009', 'end': u'2010'}, 'location': '', 'institution': u'University of Vermont', 'title': u'CSSA President'}, {'current': 0, 'date': {'start': u'2007', 'end': u'2009'}, 'location': '', 'institution': u'MicroStrain, Inc.', 'title': u'Intern'}], 'id': '112557365', 'viewers': []}>

Company search:

    >>> import parseli
    >>> parseli.company_search('google', limit=1)
    [{u'displayName': u'LinkedIn',
    u'headLine': u'LinkedIn',
    u'id': u'1337',
    u'imageUrl': u'http://media.licdn.com/mpr/mpr/shrink_40_40/p/3/000/248/137/3f632c3.png',
    u'size': {'lower': 1001, 'upper': 5000},
    u'subLine': u'Internet; 1001-5000 employees',
    u'url': u'http://www.linkedin.com/company/1337'}]

People search:

    >>> import parseli
    >>> parseli.people_search(first='mek', limit=3)
    {'people': [{'location': u'&#xc5;rhus Area, Denmark',
                 'name': {'first': u'Mek', 'last': u'Falk'},
                 'title': u'Owner at Alive Music',
                 'url': u'http://dk.linkedin.com/pub/mek-falk/1b/8a2/4a9'},
                {'location': u'Copenhagen Area, Denmark',
                 'name': {'first': u'Mek', 'last': u'Nielsen'},
                 'title': '',
                 'url': u'http://dk.linkedin.com/in/meknielsen'},
                {'location': u'San Francisco Bay Area',
                 'name': {'first': u'Mek', 'last': u'Karpeles'},
                 'title': u'Founder and CEO at Hackerlist, Inc',
                 'url': u'http://www.linkedin.com/in/mekarpeles'}],
     'summary': {'limit': 25, 'total': 169}
    }

