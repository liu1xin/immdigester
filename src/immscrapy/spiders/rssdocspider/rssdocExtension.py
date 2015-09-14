#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

from scrapy import signals
from scrapy.exceptions import NotConfigured
from rssdocUtils import closeRssDBConn


class rssdocExtension(object):

    def __init__(self, outdest, outfmt):
        self.outfmt = outfmt
        self.outdest = outdest

    @classmethod
    def from_crawler(cls, crawler):
        # load setting for indexdocspider
        crawler.settings.setmodule('immscrapy.spiders.rssdocspider.rssdocSetting')

        # sourcetype must be config
        if not crawler.settings.getint('RSSDOC_SOURCETYPE'):
            raise NotConfigured

        outdest = crawler.settings.getint('RSSDOC_OUTDEST', 0)
        outfmt = crawler.settings.getint('RSSDOC_OUTFMT', 0)

        # instantiate the extension object
        rssdoc_ext = cls(outdest, outfmt)
        rssdoc_ext.logext = crawler.settings.get('RSSDOC_LOGEXT', None)

        # connect the extension object to signals
        crawler.signals.connect(rssdoc_ext.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(rssdoc_ext.spider_closed,
                                signal=signals.spider_closed)
        crawler.signals.connect(rssdoc_ext.item_scraped,
                                signal=signals.item_scraped)

        return rssdoc_ext

    def spider_opened(self, spider):
        if 'rssdocSpider' != spider.name:
            return

        if None != self.logext:
            spider.loger.addHandler(self.logext)

        spider.outformat = self.outfmt
        spider.outdest = self.outdest

        spider.loger.info("opened spider %s" % spider.name)

    def spider_closed(self, spider):
        if 'rssdocSpider' != spider.name:
            return

        spider.loger.info("closed spider %s" % spider.name)
        if None != spider.dbconn:
            closeRssDBConn(spider.dbconn)
        if None != self.logext:
            self.logext.flush()
            self.logext.close()

    def item_scraped(self, item, spider):
        if 'rssdocSpider' != spider.name:
            return

        if None != self.logext:
            self.logext.flush()
