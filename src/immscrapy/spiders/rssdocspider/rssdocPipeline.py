#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

from rssdocUtils import rssdocItemReady, rssdocItemSave


class rssdocSavePipeline(object):

    def process_item(self, item, spider):

        if 'rssdocSpider' != spider.name:
            return item

        itemready = rssdocItemReady(spider.outformat, item)

        result = rssdocItemSave(spider.outdest, itemready, spider.dbconn)
        if True == result:
            spider.loger.info('save rssdoc item success!')
        else:
            spider.loger.warning('save rssdoc item fail!')

        return item
