# -*- coding: utf-8 -*-
# file: hackernews.py
# author: kyle isom 
# license: ISC / public domain dual-license
#
# parse news feeds from hacker news

from BeautifulSoup import BeautifulSoup as Soup
import pdb
import re
import time
import urllib2

site      = "http://www.hackerne.ws"
index     = None

def load_index():
    global index

    try:
        index = urllib2.urlopen(site).read()
    except urllib2.URLError as e:
        print e
        return False
    else:
        return True

def is_link_tag(tag):
    if not len(tag.attrs) == 1: return False
    if not tag.attrs[0][0] == 'class':
        return False
    if not tag.attrs[0][1] == 'title':
        return False

    return True

def is_link(url):
    urlre = '[^\w\s]?([a-zA-Z]+://)?([a-z[A-Z]\w*\.)+(\w{2,8})+(/\w+)*[^\w\s]?'

    if not re.match(urlre, url): 
        return False
    if url.startswith('/'):
        return False

    return True



def process_tag(tag):
    td       = tag.contents[0]
    link     = td.attrs[0][1]             # [ ('href', LINK), ]
    title    = td.contents[0]             # [ text_inside_anchor, ]

    return (title, link)

def load_links():
    # we're looking for <td class="title"> tags which mark links
    link_tags = [ tag for tag in Soup(index).fetch('td')
                  if is_link_tag(tag) ]

    return link_tags

def load_stories(links):
    stories = { }
    for link in links:
        tl = process_tag(link)

        if tl[0] in stories.keys(): 
            continue
        if tl[1] in stories.values():
            continue 
        if not is_link(tl[1]):
            continue
        if 'More' == tl[0]:
            continue

        title           = tl[0]
        stories[title]  = { 'url': tl[1], 'timestamp': time.time() }

    return stories

def fetch():
    load_index()
    return load_stories(load_links())
