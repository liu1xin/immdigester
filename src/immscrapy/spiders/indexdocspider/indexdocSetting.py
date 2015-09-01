#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月27日

@author: liu1xin@outlook.com
'''

import logging


# add file log for indexdocspider
logfile = r'd:\indexdoc.log'
filehandle = logging.handlers.RotatingFileHandler(logfile)
filehandle.setLevel(logging.INFO)
INDEXDOC_LOGEXT = filehandle

# indexdocspider config
INDEXDOC_ZIP = True
INDEXDOC_SAVEPATH = r'd:\ttt'

# indexdocspider url config
INDEXDOC_SKIPPREFIX = ('irc:', 'mailto:', 'http://', 'https://')
INDEXDOC_SKIPSUFFIX = ('.zip', '.pdf', '.doc', '.tar')
