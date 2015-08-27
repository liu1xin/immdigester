#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月27日

@author: liu1xin@outlook.com
'''

import logging

FILELOG_ENABLE = False
FILELOG_LEVEL = logging.DEBUG
FILELOG_NAME = r'd:\indexdoc.log'

INDEXDOC_ZIP = True
INDEXDOC_SAVEPATH = r'd:\ttt'

INDEXDOC_SKIPPREFIX = ('irc:', 'mailto:', 'http://', 'https://')
INDEXDOC_SKIPSUFFIX = ('.zip', '.pdf', '.doc', '.tar')
