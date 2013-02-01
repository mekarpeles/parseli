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
import urllib2
from operator import add
from BeautifulSoup import BeautifulSoup
from utils import Storage

# String templates for BeautifulSoup element selecting
EMPLOY_SEC_CLS = 'position  {} experience vevent vcard summary-{}'
EDU_SEC_CLS = 'position {} education vevent vcard'
PROFILE_URL = "http://linkedin.com/profile?id={}"

def getli(url, raw=False):
    """Get LinkedIn: json results for any linkedin url
    
    XXX Consider renaming raw to 'dumps'

    params:
        raw - False if dict, True if raw str dump / txt
    """
    soup = crawli(url)
    parsely = parseli(soup, raw=raw)
    return parsely

def crawli(url):
    """Crawl LinkedIn: Returns html soup for any linkedin url"""
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla 3.10')
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
            "url": '',
            "name": {},
            "location": {},
            "headline": '',
            "industry": '',
            "viewers": [],
            "employment": [],
            "education": [],
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
                career_selectors = [overview_sec[0].findAll('div', {'class': 'summary-current'}),
                                    overview_sec[0].findAll('div', {'class': 'summary-past'}),
                                    overview_sec[0].findAll('div', {'class': 'past'})]
                # prune any selector which returns no results, i.e. [], are not lists
                career_lsts = filter(lambda x: type(x) is list, career_selectors)

                # if career_lsts contains any non empty lists
                if any(career_lsts):
                    # reduce on list concat
                    careers = reduce(add, [lst[0] for lst in career_lsts])
                    print '-'*10
                    print careers
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

    def similar(profile):
        """Returns a list of similar profile urls, if they exist"""
        try:
            ppl = soup.findAll('div', {'id': 'extra'})[0].findAll('a')
            profile['similar'] = [a['href'] for a in ppl]
        except:
            pass
        return profile

    profile = similar(header(overview(education(employment(meta(profile))))))
    return profile if not raw else json.dumps(profile)
