# -*- coding: utf-8 -*-
# file: rssfeed.py
# author: kyle isom <coder@kyleisom.net>
#
# parse RSS feeds from various sources

import feedparser
import os
import sqlite3
import time

dbfile  = './config/rss.db'
dbo     = None
feeds   = [ ]


def create_db():
    cur         = dbo.cursor()

    cur.execute( 'CREATE TABLE feeds (name TEXT, url TEXT, aggregate BOOLEAN)' )
    dbo.commit()
    cur.close()

def connect_db():
    global dbo

    dbo         = sqlite3.connect( dbfile )

    if not os.stat( dbfile ).st_size:
        create_db( )

def load_feeds():
    global feeds

    cur         = dbo.cursor()
    cur.execute( 'SELECT * FROM feeds' )

    feeds       = [ feed[1] for feed in cur.fetchall() ]
    dbo.commit()
    cur.close()
    
def load_entries():
    stories     = { }
    for feed in feeds:
        feed    = feedparser.parse( feed )

        for entry in feed.entries:
            title   = entry['title']
            link    = entry['link']

            if title in stories:
                continue
            stories[title]  = { 'url': link, 'timestamp': time.time(), 
                                'source': feed.feed['title']}

    return stories

def fetch():
    if not dbo: connect_db()
    load_feeds()
    
    return load_entries()

def add_feed(name, url, aggregate):
    if not dbo: connect_db()
    params  = (name, url, aggregate)

    cur     = dbo.cursor()
    cur.execute( 'INSERT INTO feeds VALUES (?, ?, ?)', params)
    dbo.commit()
    cur.close()
