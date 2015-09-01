#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

from scrapy import signals
from scrapy.exceptions import NotConfigured


class rssdocExtension(object):

    def __init__(self, zipped, savepath):
        self.zipp = zipped
        self.spath = savepath

    @classmethod
    def from_crawler(cls, crawler):
        # load setting for indexdocspider
        crawler.settings.setmodule('immscrapy.spiders.rssdocspider.rssdocSetting')

        # savepath must be config
        if not crawler.settings.get('INDEXDOC_SAVEPATH'):
            raise NotConfigured

        zipped = crawler.settings.getbool('INDEXDOC_ZIP', True)
        savepath = crawler.settings.get('INDEXDOC_SAVEPATH', '')

        # instantiate the extension object
        rssdoc_ext = cls(zipped, savepath)
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

        spider.loger.info("opened spider %s" % spider.name)

    def spider_closed(self, spider):
        if 'rssdocSpider' != spider.name:
            return

        spider.loger.info("closed spider %s" % spider.name)
        if None != self.logext:
            self.logext.flush()
            self.logext.close()

    def item_scraped(self, item, spider):
        if 'rssdocSpider' != spider.name:
            return

        if None != self.logext:
            self.logext.flush()
