#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月26日

@author: liu1xin@outlook.com
'''

import scrapy
import os.path
from os.path import join as ospathjoin
from os.path import split as ospathsplit
from indexdocItem import IndexdocItem


class IndexdocspiderSpider(scrapy.Spider):
    '''
    classdocs
    '''
    name = "indexdocSpider"
    allowed_domains = []
    start_urls = []

    def __init__(self, url=None, savedir=None, *args, **kwargs):
        super(IndexdocspiderSpider, self).__init__(*args, **kwargs)

        if not url:
            return
        elif not url.endswith('index.html'):
            return
        else:
            self.base_url = url.rstrip('index.html')

        if savedir:
            self.savedir = savedir
        else:
            self.savedir = ''

        self.start_urls.append(url)
        # self.allowed_domains.append()

    def parse(self, response):
        self.logger.info('get url %s' % response.url)

        doc = self._indexdoc(response.url)
        if doc['docvalid']:
            doc['docdata'] = response.body
        yield doc

        conttype = response.headers.get('Content-Type', '')

        if 'index.html' == doc['docname']:
            for linkpath in response.xpath('//script/@src'):
                link_url = IndexdocspiderSpider.getnewurl(linkpath.extract())
                if '' == link_url:
                    continue
                else:
                    href_url = response.urljoin(link_url)
                    yield scrapy.Request(href_url, callback=self.parse)
            for linkpath in response.xpath('//link/@href'):
                link_url = IndexdocspiderSpider.getnewurl(linkpath.extract())
                if '' == link_url:
                    continue
                else:
                    href_url = response.urljoin(link_url)
                    yield scrapy.Request(href_url, callback=self.parse)

        if 'text/html' in conttype:
            for linkpath in response.xpath('//a/@href'):
                link_url = IndexdocspiderSpider.getnewurl(linkpath.extract())
                if '' == link_url:
                    continue
                else:
                    href_url = response.urljoin(link_url)
                    yield scrapy.Request(href_url, callback=self.parse)

    def _indexdoc(self, url):
        ''' create index doc info from url '''
        doc = IndexdocItem()
        doc['docurl'] = url
        doc['docsize'] = 0
        doc['docsave'] = True
        doc['docvalid'] = False

        if url.startswith(self.base_url):
            filepath = url.replace(self.base_url, '')
        else:
            doc['docname'] = ''
            return doc

        if '' == filepath:
            doc['docname'] = ''
        else:
            doc['docvalid'] = True
            doc['savepath'] = ospathjoin(self.savedir,
                                         filepath.replace("/", os.path.sep))
            doc['docname'] = ospathsplit(doc['savepath'])[-1]

        return doc

    @staticmethod
    def getnewurl(linkurl):
        ''' check url can be request '''
        if not linkurl or '#' in linkurl:
            return ''
        if linkurl.startswith('/'):
            return ''
        if linkurl.startswith('http://') or linkurl.startswith('https://'):
            return ''
        if linkurl.endswith('zip') or linkurl.endswith('pdf'):
            return ''
        if linkurl.startswith('irc:') or linkurl.startswith('mailto:'):
            return ''

        return linkurl
