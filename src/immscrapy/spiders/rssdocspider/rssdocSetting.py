#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import logging


# add file log for indexdocspider
logfile = r'd:\rssdoc.log'
filehandle = logging.handlers.RotatingFileHandler(logfile)
filehandle.setLevel(logging.INFO)
RSSDOC_LOGEXT = filehandle

# indexdocspider config
RSSDOC_DBTYPE = 'sqlite3'
RSSDOC_CONNECT = r'imm.db'
RSSDOC_DATANAME = r'imm.db'
