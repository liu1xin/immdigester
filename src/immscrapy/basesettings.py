#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import logging
from scrapy.settings.default_settings import LOG_ENABLED, LOG_LEVEL,\
    ITEM_PIPELINES

BOT_NAME = 'immscrapy'

SPIDER_MODULES = ['immscrapy.spiders.indexdocspider',
                  'immscrapy.spiders.rssdocspider']
NEWSPIDER_MODULE = 'immscrapy.spiders'

LOG_ENABLED = True
LOG_LEVEL = logging.DEBUG

AUTOTHROTTLE_ENABLED = True

ITEM_PIPELINES = {
    'immscrapy.spiders.indexdocspider.indexdocPipeline.indexdocSavePipeline': 200,
    'immscrapy.spiders.rssdocspider.rssdocPipeline.rssdocSavePipeline': 300,
}


EXTENSIONS = {
    'immscrapy.spiders.indexdocspider.indexdocExtension.indexdocExtension': 500,
    'immscrapy.spiders.rssdocspider.rssdocExtension.rssdocExtension': 600,
}
