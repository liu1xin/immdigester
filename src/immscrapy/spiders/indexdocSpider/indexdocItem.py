#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import scrapy


class IndexdocItem(scrapy.Item):
    docname = scrapy.Field()
    docurl = scrapy.Field()
    docsize = scrapy.Field()
    docdata = scrapy.Field()
    savepath = scrapy.Field()
    docsave = scrapy.Field()
    docvalid = scrapy.Field()
