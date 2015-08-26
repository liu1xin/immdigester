#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import os.path


class indexdocSavePipeline(object):

    def process_item(self, item, spider):
        ''' save index doc file '''
        spider.logger.info("doc %s save path %s" %
                           (item['docname'], item['savepath']))

        if not os.path.exists(os.path.dirname(item['savepath'])):
            os.mkdir(os.path.dirname(item['savepath']))

        if item['docvalid'] and item['docsave']:
            with open(item['savepath'], 'wb+') as f:
                f.write(item['docdata'])

        return item
