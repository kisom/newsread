#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: cron.py
# author: kyle isom <coder@kyleisom.net>
#
# python script to be run from a cron job to load the database with stories

import feeder
import os

def main( ):
    datadir = os.path.join(os.path.expanduser('~'), 'data', 'newsdb')

    F       = feeder.Feeder( os.path.join(datadir, 'news.db') )
    F.register_feeder('hackernews')
    F.register_feeder('rssfeed')

    F.feed()

if __name__ == '__main__':
    main()


