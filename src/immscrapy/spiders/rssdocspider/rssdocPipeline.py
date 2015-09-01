#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

from rssdocUtils import itemPrepare, itemSave


class rssdocSavePipeline(object):

    def process_item(self, item, spider):

        if 'rssdocSpider' != spider.name:
            return item

        itemsave = itemPrepare(spider.outformat, item)
        itemSave(spider.outdest, itemsave)

        return item
