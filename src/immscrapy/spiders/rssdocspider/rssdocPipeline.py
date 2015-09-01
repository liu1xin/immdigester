#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''


class rssdocSavePipeline(object):

    def process_item(self, item, spider):

        savetuple = itemToSavevalue(spider.rssid, item)
        saveRssDoc(spider.dbconn, savetuple)

        return item