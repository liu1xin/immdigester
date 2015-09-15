#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

from scrapy.settings import Settings
from immscrapy.spiders.rssdocspider import (RSSDOC_OUTDEST_NULL,
                                            RSSDOC_OUTFMT_NULL)
from immscrapy.spiders.rssdocspider.rssdocUtils import (rssdocItemReady,
                                                        rssdocItemSave,
                                                        getRssDBConn,
                                                        closeRssDBConn)


class rssdocSavePipeline(object):

    def __init__(self, outfmt, outdest):
        self.outfmt = outfmt
        self.outdest = outdest

    def process_item(self, item, spider):
        if 'rssdocSpider' != spider.name:
            return item

        itemready = rssdocItemReady(self.outfmt, item)

        result = rssdocItemSave(self.outdest, itemready, spider.dbconn)
        if True == result:
            spider.loger.info('save rssdoc item success!')
        else:
            spider.loger.warning('save rssdoc item fail!')

        return item

    @classmethod
    def from_crawler(cls, crawler):
        sett = Settings()
        sett.setmodule('immscrapy.spiders.rssdocspider.rssdocSetting')
        outfmt = sett.getint('RSSDOC_OUTFMT', RSSDOC_OUTFMT_NULL)
        outdest = sett.getint('RSSDOC_OUTDEST', RSSDOC_OUTDEST_NULL)

        pipeline = cls(outfmt, outdest)
        pipeline.logext = sett.get('RSSDOC_LOGEXT', None)

        return pipeline

    def open_spider(self, spider):
        if 'rssdocSpider' != spider.name:
            return

        # 尝试加载库连接和扩展日志
        if None == spider.dbconn:
            spider.dbconn = getRssDBConn()
        if None != self.logext:
            spider.loger.addHandler(self.logext)

        spider.loger.info("opened spider %s" % spider.name)

    def close_spider(self, spider):
        if 'rssdocSpider' != spider.name:
            return

        if None != spider.dbconn:
            closeRssDBConn(spider.dbconn)

        spider.loger.info("close spider %s" % spider.name)
