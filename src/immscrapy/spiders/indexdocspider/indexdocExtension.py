#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured


class indexdocExtension(object):

    def __init__(self, zipped, savepath):
        self.zipp = zipped
        self.spath = savepath

    @classmethod
    def from_crawler(cls, crawler):
        # load setting for indexdocspider
        crawler.settings.setmodule('immscrapy.spiders.indexdocspider.indexdocSetting')

        # savepath must be config
        if not crawler.settings.get('INDEXDOC_SAVEPATH'):
            raise NotConfigured

        zipped = crawler.settings.getbool('INDEXDOC_ZIP', True)
        savepath = crawler.settings.get('INDEXDOC_SAVEPATH', '')

        # instantiate the extension object
        idxdoc_ext = cls(zipped, savepath)
        idxdoc_ext.logext = crawler.settings.get('INDEXDOC_LOGEXT', None)
        idxdoc_ext.skippre = crawler.settings.getlist('INDEXDOC_SKIPPREFIX', None)
        idxdoc_ext.skipsuf = crawler.settings.getlist('INDEXDOC_SKIPSUFFIX', None)
        # connect the extension object to signals
        crawler.signals.connect(idxdoc_ext.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(idxdoc_ext.spider_closed,
                                signal=signals.spider_closed)
        crawler.signals.connect(idxdoc_ext.item_scraped,
                                signal=signals.item_scraped)

        return idxdoc_ext

    def spider_opened(self, spider):
        if 'indexdocSpider' != spider.name:
            return
        
        if None != self.logext:
            spider.loger.addHandler(self.logext)

        spider.savepath = self.spath
        spider.skippre = self.skippre
        spider.skipsuf = self.skipsuf

        spider.loger.info("opened spider %s" % spider.name)


    def spider_closed(self, spider):
        spider.loger.info("closed spider %s" % spider.name)
        if None != self.logext:
            self.logext.flush()
            self.logext.close()

    def item_scraped(self, item, spider):
        if None != self.logext:
            self.logext.flush()
