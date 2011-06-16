# -*- coding: utf-8 -*-
# file: post.py
# author: kyle isom <coder@kyleisom.net>
#
# representation of a post

import imp
import os
from BeautifulSoup import BeautifulSoup as Soup

base_mod_dir    = os.path.join(  os.path.expanduser('~'),
                                'code', 'newsread', 'parsers' )

class Post:
    title       = None
    timestamp   = None
    url         = None
    content     = None

    parsers     = None

    def __init__(self, sql_t = None, title = None, timestamp = None, url = None,
                 content = None, source = None):

        if sql_t:
            self.title      = sql_t[0]
            self.timestamp  = sql_t[1]
            self.url        = sql_t[2]
            self.content    = sql_t[3]
            self.source     = sql_t[4]

        if title:
            self.title      = title

        if timestamp:
            self.timestamp  = int(timestamp)

        if url:
            self.url        = url

        if content:
            self.content    = content

        if source:
            self.source     = source

        self.parsers        = { }

    def parse(self, parser):
        if not parser in self.parsers:
            return None

        return self.parsers[parser](self.content)

    def register_parser(self, mod, pathname = base_mod_dir):
        fp, pathname, description   = imp.find_module(mod, [ pathname ])

        try:
            parsermod   = imp.load_module( mod, fp, pathname, description )
        except:
            print '[+] failed to load %s from %s' % (mod, pathname)
            raise
            return
        else:
            self.parsers[mod] = parsermod.parser
        finally:
            if fp:
                fp.close()

    def __str__(self):
        soup    = Soup(self.content)
        return soup.prettify()
