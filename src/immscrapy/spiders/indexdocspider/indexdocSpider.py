#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import logging
import scrapy
from indexdocUtils import getbasedomin, checkurlvalid
from indexdocUtils import createItem, parselinkurl


class IndexdocspiderSpider(scrapy.Spider):
    '''
    classdocs
    '''
    name = "indexdocSpider"
    allowed_domains = []
    start_urls = []

    def __init__(self, url=None, name=None, *args, **kwargs):
        super(IndexdocspiderSpider, self).__init__(*args, **kwargs)

        # init indexdocspider logger
        self.loger = logging.getLogger('immscrapy.spiders.indexdocspider')        
            
        if not checkurlvalid(url):
            self.loger.warning('<<invalid url = %s>> ' % url)
            return
        else:
            self.loger.warning('<<input url = %s>>' % url)

        self.base_url = url.rstrip('index.html')
        self.base_domain = getbasedomin(url)

        if name:
            self.savename = name
        else:
            self.savename = self.base_domain

        self.allowed_domains.append(self.base_domain)
        self.start_urls.append(url)
        # self.allowed_domains.append()

    def parse(self, response):
        self.loger.info('get url %s' % response.url)

        conttype = response.headers.get('Content-Type', '')
        doc = createItem(response.url, self.base_url)
        if doc['docvalid']:
            doc['docdata'] = response.body
            doc['doctype'] = conttype
            yield doc

        if 'index.html' == doc['docname']:
            for linkpath in response.xpath('//script/@src'):
                link_url = parselinkurl(linkpath.extract(),
                                        self.skippre, self.skipsuf)
                if '' == link_url:
                    continue
                else:
                    href_url = response.urljoin(link_url)
                    yield scrapy.Request(href_url, callback=self.parse)
            for linkpath in response.xpath('//link/@href'):
                link_url = parselinkurl(linkpath.extract(),
                                        self.skippre, self.skipsuf)
                if '' == link_url:
                    continue
                else:
                    href_url = response.urljoin(link_url)
                    yield scrapy.Request(href_url, callback=self.parse)

        if 'text/html' in conttype:
            for linkpath in response.xpath('//a/@href'):
                link_url = parselinkurl(linkpath.extract(),
                                        self.skippre, self.skipsuf)
                if '' == link_url:
                    continue
                else:
                    href_url = response.urljoin(link_url)
                    yield scrapy.Request(href_url, callback=self.parse)
