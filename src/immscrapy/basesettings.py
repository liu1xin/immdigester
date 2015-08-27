#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import logging
from scrapy.settings.default_settings import LOG_ENABLED, LOG_LEVEL

BOT_NAME = 'immscrapy'

SPIDER_MODULES = ['immscrapy.spiders.indexdocspider',
                  'immscrapy.spiders.rssdocspider']
NEWSPIDER_MODULE = 'immscrapy.spiders'

LOG_ENABLED = True
LOG_LEVEL = logging.INFO

AUTOTHROTTLE_ENABLED = True
