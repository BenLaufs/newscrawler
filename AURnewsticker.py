# AUR NEWS TICKER - Ben Laufer, 10 Jul 2017
# RSS Feed Filter

import feedparser
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import webbrowser
import string
import time
import uuid
from project_util import translate_html


headers = {'User-Agent': 'Chrome/41.0.2228.0 Safari/537.3'}

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    print(url)
    req_url = url
    req = Request(url=req_url, headers=headers)
    soup = BeautifulSoup(urlopen(req).read(), "xml")
    ret = []
    itemlist = soup.find_all('item')

    for i in itemlist:
        guid = uuid.uuid4()
        if i.title == None:
            title = str("empty")
        else:
            title = i.title.string
        if i.description == None:
            subject = str("empty")
            summary = str("empty")
        else:
            subject = i.description.string
            summary = i.description.string
        if i.link == None:
            link == str("empty")
        else:
            link = i.link.string
        if i.pubDate == None:
            pubDate  = str("empty")
        else:
            pubDate = i.pubDate.string
        n = NewsStory(guid, title, subject, summary, link, pubDate)
        ret.append(n)
    return ret

#======================

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self,guid, title, subject,summary,link, pubDate):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
        self.pubDate = pubDate


    def getGuid(self):
        return self.guid
    def getTitle(self):
        return self.title
    def getSubject(self):
        return self.subject
    def getSummary(self):
        return self.summary
    def getLink(self):
        return self.link
    def getpubDate(self):
        return self.pubDate
#======================
# Part 3
# Filtering
#======================

def filterStories(stories, trigger):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    trigger = str(trigger)
    trigger = trigger.lower()
    filteredstories = []
    c = 0
    for s in stories:
        try:
            titlelow = s.title.lower()
            subjectlow = s.subject.lower()
            summarylow = s.summary.lower()
            if trigger in titlelow or trigger in subjectlow or trigger in summarylow:
                print("trigger found")
                print(s.title)
                c += 1
                summary_split = summarylow.split('>')
                i = len(summary_split) - 1
                s.summary = summary_split[i]
                if "https://https://" in s.link:
                    link = s.link.strip("https://https://")
                    link = "https://" + link
                    s.link = link
                filteredstories.append(s)
            else:
                pass
        except Exception as e:
            pass
    return filteredstories

def sortStories(filteredstories):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of  stories sorted by date.
    """
    date_sorted_stories = []
    unsorted_stories = []
    for s in filteredstories:
        try:
            print(s.pubDate)
            date = s.pubDate.feedparser._parse_date()
            print(date)
            date = date.strftime("%j%m%t")
            print(date)
            s.pubDate = date
            date_sorted_stories.append(s)
        except Exception as e:
            s.pubDate = "empty"
            unsorted_stories.append(s)
    date_sorted_stories = sorted(date_sorted_stories, key = lambda story: story.pubDate)
    sorted_stories = date_sorted_stories + unsorted_stories
    return sorted_stories

def readUrlConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    urlfile = open(filename, "r")
    all = [ line.rstrip() for line in urlfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    urls = []
    for line in lines:
        if line != "":
            urls.append(line)
    return urls
