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
        # load setting for indexdoc
        crawler.settings.setmodule('immscrapy.spiders.indexdocspider.indexdocSetting')

        # savepath must be config
        if not crawler.settings.get('INDEXDOC_SAVEPATH'):
            raise NotConfigured

        zipped = crawler.settings.getbool('INDEXDOC_ZIP', True)
        savepath = crawler.settings.get('INDEXDOC_SAVEPATH', '')

        # instantiate the extension object
        idxdoc_ext = cls(zipped, savepath)

        if crawler.settings.getbool('FILELOG_ENABLE', False):
            logfile = crawler.settings.get('FILELOG_NAME', 'indexdoc.log')
            filehandle = logging.handlers.RotatingFileHandler(logfile)
            filehandle.setLevel(crawler.settings.get('FILELOG_LEVEL', logging.INFO))
            idxdoc_ext.loghandle = filehandle
        else:
            idxdoc_ext.loghandle = None

        idxdoc_ext.skippre = crawler.settings.getlist('INDEXDOC_SKIPPREFIX', None)
        idxdoc_ext.skipsuf = crawler.settings.getlist('INDEXDOC_SKIPSUFFIX', None)
        # connect the extension object to signals
        crawler.signals.connect(idxdoc_ext.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(idxdoc_ext.spider_closed,
                                signal=signals.spider_closed)

        return idxdoc_ext

    def spider_opened(self, spider):
        spider.logger.info("opened spider %s" % spider.name)
        if 'indexdocSpider' == spider.name:
            if not self.loghandle:
                logger = logging.getLogger('immscrapy.spiders.indexdocspider.indexdocSpider')
                logger.addHandler(self.loghandle)

            spider.savepath = self.spath
            spider.skippre = self.skippre
            spider.skipsuf = self.skipsuf

    def spider_closed(self, spider):
        spider.logger.info("closed spider %s" % spider.name)
