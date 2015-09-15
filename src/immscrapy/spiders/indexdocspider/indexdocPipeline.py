#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import os.path
from os.path import join as ospathjoin
from scrapy.settings import Settings


class indexdocSavePipeline(object):

    def __init__(self, zipped, savepath):
        self.zipped = zipped
        self.savepath = savepath

    def process_item(self, item, spider):
        ''' save index doc file '''
        if 'indexdocSpider' != spider.name:
            return item

        if not item['docvalid']:
            return None

        realpath = ospathjoin(self.savepath, spider.savename,
                              item['docpath'])
        spider.loger.info("doc %s save path %s" %
                          (item['docname'], realpath))

        if not os.path.exists(os.path.dirname(realpath)):
            os.makedirs(os.path.dirname(realpath))

        with open(realpath, 'wb+') as f:
            f.write(item['docdata'])

        return item

    @classmethod
    def from_crawler(cls, crawler):
        sett = Settings()
        sett.setmodule('immscrapy.spiders.indexdocspider.indexdocSetting')
        zipped = sett.getbool('INDEXDOC_ZIP', True)
        savepath = sett.get('INDEXDOC_SAVEPATH', '')
        skippre = sett.getlist('INDEXDOC_SKIPPREFIX', None)
        skipsuf = sett.getlist('INDEXDOC_SKIPSUFFIX', None)

        pipeline = cls(zipped, savepath)
        pipeline.logext = sett.get('INDEXDOC_LOGEXT', None)
        pipeline.skippre = skippre
        pipeline.skipsuf = skipsuf

        return pipeline

    def open_spider(self, spider):
        if 'indexdocSpider' != spider.name:
            return

        # 尝试加载扩展日志
        if None != self.logext:
            spider.loger.addHandler(self.logext)

        spider.savepath = self.savepath
        spider.skippre = self.skippre
        spider.skipsuf = self.skipsuf

        spider.loger.info("opened spider %s" % spider.name)

    def close_spider(self, spider):
        if 'indexdocSpider' != spider.name:
            return

        # zip
        if True == self.zipped:
            pass

        spider.loger.info("close spider %s" % spider.name)
