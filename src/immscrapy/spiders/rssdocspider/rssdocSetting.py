#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import logging


# add file log for rssdocspider
logfile = r'd:\rssdoc.log'
filehandle = logging.handlers.RotatingFileHandler(logfile)
filehandle.setLevel(logging.INFO)
RSSDOC_LOGEXT = None

# rssdocspider input config
RSSDOC_SOURCETYPE = 2
RSSDOC_SOURCEURL = r'http://www.infoq.com/cn/feed'

# rssdocspider db config
RSSDOC_DBTYPE = 'sqlite3'
RSSDOC_CONNECTINFO = r'../data/imm.db'
RSSDOC_DBNAME = r'imm_db'

# rssdocspider output config
RSSDOC_OUTDEST = 1
RSSDOC_OUTFMT = 1
RSSDOC_DESTFILE = r''
