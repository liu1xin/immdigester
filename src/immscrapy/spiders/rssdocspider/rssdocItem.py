#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import scrapy


class RssdocItem(scrapy.Item):
    rssid = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    content = scrapy.Field()
    pubdate = scrapy.Field()
    category = scrapy.Field()
