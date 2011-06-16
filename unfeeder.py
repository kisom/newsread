#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: unfeeder.py
# author: kyle isom <coder@kyleisom.net>
#
# unpack data from the feeder database

import os
import post
import sqlite3

DBTYPE  = 'sqlite3'

class Unfeeder:

    database    = None
    dbo         = None

    def __init__(self, database):
        self.database = database

        self._connect()

    def _connect(self):
        if 'sqlite3' == DBTYPE:
            self.dbo    = sqlite3.connect( self.database )
        
        if not os.stat( self.database ).st_size:
            self.dbo    = None
            print '[!] empty database!'

    def unfeed(self):
        cur     = self.dbo.cursor().execute('SELECT * FROM raw')
        return cur

    def get_post(self):
        import post

        c       = self.unfeed()
        for p in c:
            yield post.Post(sql_t = p)

    def post_count(self):
        i   = 0
        c   = self.dbo.cursor().execute('SELECT * FROM raw')
    
        while True:
            res = c.fetchone()
            if None == res: break

            i += 1

        return i


        



