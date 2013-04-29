#-*- coding: utf-8 -*-

"""                  .    
 ,-. ,-. ,-. ,-. ,-. |  * 
 | | ,-| |   `-. |-' |  | 
 |-' `-^ '   `-' `-' `' ' 
 |
    parseli
    ~~~~~~~
    Crawler and Parser for LinkedIn which retrieves and consumes HTML
    pages, extracts key values and converts them to dict (json) output

    :copyright: (c) 2012 by Mek
    :license: BSD, see LICENSE for more details.
"""

import json
from urllib import urlencode
import urllib2
import requests
from operator import add
from BeautifulSoup import BeautifulSoup
from utils import Storage

# String templates for BeautifulSoup element selecting
EMPLOY_SEC_CLS = 'position  {} experience vevent vcard summary-{}'
EDU_SEC_CLS = 'position {} education vevent vcard'
PROFILE_URL = "http://linkedin.com/profile?id={}"

def getli(url, raw=False):
    """Get LinkedIn: json results for any linkedin url
    
    params:
        raw - False if desired output is a python dict,
              True if raw json dump
    """
    # allow search by li username
    if '/' not in url:
        username = url
        url = 'http://linkedin.com/in/%s' % username

    soup = crawli(url)
    parsely = parseli(soup, raw=raw)
    return parsely

def crawli(url, user_agent=('User-agent', 'Mozilla 3.10')):
    """Crawl LinkedIn: Returns html soup for any linkedin url"""
    url = url.replace('https://', 'http://')
    req = urllib2.Request(url)
    req.add_header(*user_agent)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    return soup    

def parseli(soup, raw=False):
    """Parse LinkedIn: Scrapes, scrubs, and returns a dictionary of
    key LinkedIn data

    # TODO: Extend profile to include interests + Viewers 
    """
    profile = Storage({            
            "id": '',
            "avatar": '',
            "url": '',
            "name": {},
            "location": {},
            "headline": '',
            "industry": '',
            "viewers": [],
            "employment": [],
            "education": [],
            "connections": '',
            })

    def meta(profile):
        """gets metadata like unique_id, and profile url"""
        jstxt = str(soup.findAll('script'))

        def get_id(x):
            try:
                start_id = x.index("newTrkInfo = '") + 14
                end_id = x.index(',', start_id)
                return x[start_id:end_id]
            except:
                try:
                    start_id = x.index("user_id: ")
                    end_id = x.index(',', start_id)
                    return x[start_id:end_id]
                except:
                    member_id = soup.findAll('div', {'class': 'masthead'})
                    if member_id:
                        return member_id[0]['id']
            return ''

        liid = get_id(jstxt)

        def get_url():
            canonical_url = soup.findAll('link', {'rel': 'canonical'})
            return canonical_url[0]['href'] if canonical_url \
                else PROFILE_URL.format(liid)

        profile.id = liid
        profile.url = get_url()
        return profile

    def header(profile):
        """Parses the profile-header section

        +------------------------------------------+
        | +-------+  given_name family_name
        | |       |  title [at institution]
        | |  pic  |  locality [(area)] | Industry
        | |       |
        | +-------+
        """
        header_sec = soup.findAll('div', {'class': 'profile-header'})

        if header_sec:
            header_sec = header_sec[0]
            
            avatar = header_sec.findAll('div', {'id': 'profile-picture'})
            if avatar:
                profile.avatar = avatar[0].findAll('img')[0]['src']
            demographic = soup.findAll('dl', {"class": 'demographic-info adr'})
            name = header_sec.findAll('span', {"class": "full-name"})            
            headline = header_sec.findAll("p", {"class": "headline-title title"})

            # Generally headline is of the form: "Title at Institution"
            if headline:                
                profile.headline = headline[0].text
                if not profile.employment:
                    if ' at ' in profile.headline:
                        try:
                            title, institution = profile.headline.split(' at ')
                            profile["employment"].append({"institution": institution, "title": title})
                        except:
                            pass

            if name:
                given_name = name[0].findAll('span', {'class': 'given-name'})
                family_name = name[0].findAll('span', {'class': 'family-name'})

                profile.name.update({
                        'given-name': given_name[0].text if given_name else '',
                        'family-name': family_name[0].text if family_name else ''
                        })

            # Fetch industry, location + area from header section
            if demographic:
                demos = demographic[0].findAll('dd')
                if demos:
                    if len(demos) == 2:
                        industry = demos[1].text
                        profile.industry = industry
                    try:
                        location, area = demos[0].text.replace(")", "").split("(")
                    except:
                        location, area = demos[0].text, ""
                    profile.location = {"locality": location, "area": area}

        return profile

    def overview(profile):
        """Parses the "Overview" section: The overview is used as a
        last resort to fill in any missing information which could not
        be obtained by the 'experience' (employment) and 'education'
        sections. The quality of information it provides is inferior
        to the aforementioned.

        given_name family_name's Overview
        ---------------------------------
                Current  title at institution <0 or n>
                   Past  title at institution <0 or n>
              Education  institution <0 or n>
        """
        overview_sec = soup.findAll('dl', {'id': 'overview'})
        if overview_sec:
            if not profile.employment:
                career_selectors = [\
                    overview_sec[0].findAll('div', {'class': 'summary-current'}),
                    overview_sec[0].findAll('div', {'class': 'summary-past'}),
                    overview_sec[0].findAll('div', {'class': 'past'})
                    ]
                # prune any selector which returns no results, i.e. [], are not lists
                career_lsts = filter(lambda x: type(x) is list, career_selectors)

                # if career_lsts contains any non empty lists
                if any(career_lsts):
                    # reduce on list concat
                    careers = reduce(add, [lst[0] for lst in career_lsts])
                    for career in careers:
                        title, institution = str(career)[4:-5]\
                            .replace("\n", "").split('<span class="at">at </span>')
                        profile["employment"].append({"institution": institution, "title": title})

            if not profile.education:
                edu_subsec = overview_sec[0].findAll('dd', {'class': 'summary-education'})
                if edu_subsec:
                    edus = edu_subsec[0].findAll('li')
                    for edu in edus:
                        profile['education'].append({'summary': edu.text})
        return profile

    def employment(profile):
        """Parses the "Experience" section

        Notes:
        either dtstatus or dtend is present (exactly one of them)
        dtstamp signified 'Present' employee
        dtstamp is resolved to a binary value (1/0) for profile.current

        given_name family_name's Experience
        -----------------------------------
        # employers <1 to n>
        title
        institution
        dtstart - [dtstamp|dtend] | location         
        """
        jobs = soup.findAll('div', {'id': 'profile-experience'})

        # If profile "Experience Section" exists
        if jobs:
            jobs = jobs[0]
            careers = jobs.findAll('div', {'class': EMPLOY_SEC_CLS.format("first", "current")}) + \
                jobs.findAll('div', {'class': EMPLOY_SEC_CLS.format('', 'current')}) + \
                jobs.findAll('div', {'class': EMPLOY_SEC_CLS.format('', 'past')})

            for career in careers:
                title = career.findAll("span", {'class': 'title'})
                institution = career.findAll("span", {'class': 'org summary'})
                location = career.findAll("span", {'class': 'location'})
                dtstart = career.findAll('abbr', {'class': "dtstart"})
                dtstamp = career.findAll('abbr', {'class': "dtstamp"})
                dtend = career.findAll('abbr', {'class': "dtend"})
                job = {"title": title[0].text if title else '',
                       "institution": institution[0].text if institution else '',
                       "current": 1 if dtstamp else 0,
                       "location": location[0].text if location else '',
                       "date": {
                        "start": dtstart[0]['title'] if dtstart else '',
                        "end": dtend[0]['title'] if dtend else ''
                        }
                       }
                profile["employment"].append(job)
        return profile

    def education(profile):
        """Parses the "Education" section"""        
        section_edu = soup.findAll('div', {'id': 'profile-education'})
        if section_edu:
            section_edu = section_edu[0]
            edus = section_edu.findAll("div", {"class": EDU_SEC_CLS.format(' first')}) + \
                section_edu.findAll("div", {"class": EDU_SEC_CLS.format('')})  
            for school in edus:
                institution = school.findAll("h3")
                degree = school.findAll('span', {'class': 'degree'})
                major = school.findAll('span', {'class': 'major'})
                dtstart = school.findAll('abbr', {'class': "dtstart"})
                dtend = school.findAll('abbr', {'class': "dtend"})
                edu = {"institution": institution[0].text if institution else '',
                       "degree": degree[0].text if degree else '',
                       "major": major[0].text if major else '',
                       "dtstart": dtstart[0]['title'] if dtstart else '',
                       "dtend": dtend[0]['title'] if dtend else ''
                       }
                profile["education"].append(edu)
        return profile

    def conns(profile):
        """User's network size"""
        cs = soup.findAll('dd', {'class': 'overview-connections'})
        if cs:
            profile['connections'] = cs[0].findAll('strong')[0].text
        return profile

    def similar(profile):
        """Returns a list of similar profile urls, if they exist"""
        try:
            ppl = soup.findAll('div', {'id': 'extra'})[0].findAll('a')
            profile['similar'] = list(set([a['href'] for a in ppl]))
        except:
            pass
        return profile

    def techtags(profile):
        """Adds tech tags if they exist"""
        tags = soup.findAll('ol', {'id': 'skills-list'})
        if tags:
            profile['skills'] = [li.text for li in tags[0].findAll('li')]
        return profile

    def interests(profile):
        """Estimate interests based on groups / affiliations"""
        groups = soup.findAll('dd', {'id': 'pubgroups'})
        if groups:
            interests = [i.text for i in groups[0].findAll('li')]
            profile['interests'] = interests
        return profile
        
    profile = similar(interests(techtags(conns(header(overview(
                        education(employment(meta(profile)))))))))
    return profile if not raw else json.dumps(profile)

def custom_search(query, types="mynetwork,company,group,sitefeature,skill"):
    """Returns a json dict whose keys are the 'types'.

    params:
    :param query: string to search for
    :param types: 'mynetwork,company,group,sitefeature,skill'
    """
    def restructure(results):
        """Removes the unecessary 'resultList' key and maps the type
        directory to a list of results
        """
        for t in results:
            results[t] = results[t]['resultList']
        return results

    def fill_missing_types(results):
        """Fill in missing types (keys) which weren't returned by
        linkedin
        """
        for t in types.split(','):
            if t not in results:
                results[t] = []
        return results

    url = "http://www.linkedin.com/ta/federator?query=%s&types=%s" % (query, types)
    r = requests.get(url)
    results = r.json()

    return fill_missing_types(restructure(results))

def people_search(first="", last="", limit=None):
    """http://www.linkedin.com/pub/dir/?search=Search
    :params first, last, company:

    usage:
    >>> from parseli import people_search
    >>> people_search(first='mek', limit=3)
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
    """
    def parse_serp(html, limit):
        """params:
        :param html: html of the people results page
        :parma limit: only return 'limit' people
        """
        serp = {'people': []}
        soup = BeautifulSoup(html)
        serpcnt = soup.findAll('ul', {'class': 'result-summary same-name-dir'})
        if serpcnt:
            pagetotal, of, total = serpcnt[0].text.split(" ")[:3]
            serp['summary'] = {'limit': int(pagetotal.replace(',', '')),
                               'total': int(total.replace(',', ''))
                               }
        vcards = soup.findAll('li', {'class': 'vcard'})
        for vcard in vcards[:limit]:
            person = {}
            details = vcard.findAll('h2')[0].findAll('a')[0]
            location = vcard.findAll('span', {'class': 'location'})
            title = vcard.findAll('dd', {'class': 'current-content'})
            names = (name.text for name in details.findAll('span'))
            try:
                person['name'] = dict(zip(('first', 'last'), names))
            except:
                person['name'] = {'nick': names[0]}
            person['url'] = details['href']
            person['location'] = location[0].text if location else ""
            person['title'] = title[0].text if title else ""
            serp['people'].append(person)            
        return serp
    url = "http://www.linkedin.com/pub/dir/" \
        "?first=%s&last=%s&search=Search&searchType=fps" % (first, last)
    r = requests.post(url)
    html = r.content
    return parse_serp(html, limit)

def company_search(company, limit=None):
    """Search for companies 

    usage:
    >>> from parseli import company_search
    >>> company_search('google', limit=1)
    [{u'displayName': u'LinkedIn',
    u'headLine': u'LinkedIn',
    u'id': u'1337',
    u'imageUrl': u'http://media.licdn.com/mpr/mpr/shrink_40_40/p/3/000/248/137/3f632c3.png',
    u'size': {'lower': 1001, 'upper': 5000},
    u'subLine': u'Internet; 1001-5000 employees',
    u'url': u'http://www.linkedin.com/company/1337'}]
    """
    url = "http://www.linkedin.com/ta/company?query=%s" % company
    r = requests.get(url)
    companies = r.json()['resultList'][:limit]
    for company in companies:
        if 'headLine' in company and '<strong>' in company['headLine']:
            company['headLine'] = company['headLine'].replace("<strong>", "")\
                .replace("</strong>", "")
        if 'subLine' in company:
            try:
                size, _ = company['subLine'].split(" ")[-2:]
                size = size.replace('+', '').replace(',', '')
                size1, size2 = (size, size) if "-" not in size else size.split('-')
                size1, size2 = int(size1), int(size2)
            except:
                size1, size2 = (None, None)
            company[u'size'] = {'lower': size1, 'upper': size2}
    return companies
