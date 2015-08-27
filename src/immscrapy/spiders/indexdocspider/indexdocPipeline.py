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
        spider.logger.debug("doc %s save path %s" %
                           (item['docname'], item['docpath']))

        if item['docvalid']:
            realpath = ospathjoin(spider.savepath, item['docpath'])

            if not os.path.exists(os.path.dirname(realpath)):
                os.mkdir(os.path.dirname(realpath))
            with open(realpath, 'wb+') as f:
                pass
                #f.write(item['docdata'])

        return item
