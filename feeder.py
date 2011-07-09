#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: feeder.py
# author: kyle isom <coder@kyleisom.net>
#
# feeds the data into the system. contains hooks for parsing news stories
# from sites

import chardet
import imp
import os
import sqlite3
import urllib2

DBTYPE  = 'sqlite3'

class Feeder:
    
    sites       = None
    database    = None          # database target, ex. filename for sqlite3
    dbo         = None          # database object
    handlers    = None
    
    def __init__(self, database):
        self.handlers   = { }
        self.database   = database

        self._connect_database()
        self._load_sites()

    def _load_sites(self):
        # populate the site list
        pass
    

    def _load_url(self, url):
        # TODO: switch to a front-end for loading html and files
        page = urllib2.urlopen( url ).read() 

        try:
            page    = page.decode( 'utf-8' )
        except UnicodeDecodeError:
            guess   = chardet.detect(page)

            try:
                page = page.decode(guess['encoding'])
            except UnicodeDecodeError as e:
                print e
                print '[!] failed to decode url - assuming url is a file'
            except TypeError as e:
                print 'could not guess encoding, assuming url is a file!'
        return page

    def _get_stories(self, feeder):
        res     = feeder.fetch()

        for story in res:
            print '\t[+] storing story ', 
            try:
                print '%s' % story.encode('ascii')
            except UnicodeEncodeError, UnicodeDecodeError:
                print '<unicode error (url=%s>' % res[story]['url']
            cur     = self.dbo.cursor()
            cur.execute( 'SELECT * FROM raw WHERE title=?', ( story, ))
            rows    = cur.fetchone()

            if rows: 
                print '\t\t[+] skipping duplicate...'
                continue
            else:
                print '\t\t- url: %s ' % res[story]['url']

                story   = story
                url     = res[story]['url']
                ts      = int( res[story]['timestamp'] )

                if 'source' in res[story]:
                    source  = res[story]['source']
                else:
                    source  = feeder.__name__

                try:
                    page    = self._load_url( res[story]['url'] )
                except urllib2.URLError as e:
                    print '[!] skipping due to error loading url:', e
                    continue
                if not page:
                    continue

                cur.execute( 'INSERT INTO raw VALUES (?, ?, ?, ?, ?)', 
                             ( story, ts, url, page, source ))
                self.dbo.commit()
                cur.close()

    def _connect_database(self):
        if 'sqlite3' == DBTYPE:        
            self.dbo = sqlite3.connect( self.database )

            if not os.stat(self.database).st_size:
                cur      = self.dbo.cursor()
                cur.execute( 'CREATE TABLE raw (title text, timestamp integer, ' +
                                                'url text, content text, ' +
                                                'source text)' )
                self.dbo.commit()
                cur.close()
            
            #self.dbo.text_factory = str

    def feed(self):
        for handler in self.handlers:
            print '[+] loading database with feeder:', handler
            self._get_stories(self.handlers[handler])

    def register_feeder(self, feeder_name):
        # add a new site to the handler list

        # http://bugs.python.org/issue6448
        fp, pathname, description   = imp.find_module(feeder_name, ['./feeders'])

        try:
            feeder = imp.load_module( feeder_name, fp, pathname, description )
        except:
            return
        finally:
            if fp:
                fp.close()

        self.handlers[feeder_name] = feeder

           
