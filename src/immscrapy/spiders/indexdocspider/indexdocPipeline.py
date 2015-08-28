#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import os.path
from os.path import join as ospathjoin


class indexdocSavePipeline(object):

    def process_item(self, item, spider):
        ''' save index doc file '''
        if 'indexdocSpider' != spider.name:
            return item
        
        if not item['docvalid']:
            return None
        
        realpath = ospathjoin(spider.savepath, spider.savename, item['docpath'])
        spider.loger.info("doc %s save path %s" %
                              (item['docname'], realpath))

        if not os.path.exists(os.path.dirname(realpath)):
            os.makedirs(os.path.dirname(realpath))
        
        with open(realpath, 'wb+') as f:
            f.write(item['docdata'])
                
        return item
