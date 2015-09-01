#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import logging
from scrapy.spiders import XMLFeedSpider
from rssdocItem import RssdocItem
from rssdocUtils import getRssSource, getRssMeta


class RssdocspiderSpider(XMLFeedSpider):
    name = 'rssdocSpider'
    allowed_domains = []
    start_urls = []
    iterator = 'iternodes'
    itertag = 'item'

    def __init__(self, uid=None, *args, **kwargs):
        super(RssdocspiderSpider, self).__init__(*args, **kwargs)

        self.loger = logging.getLogger('immscrapy.spiders.rssdocspider')

        if not uid:
            self.loger.warning('<<invalid uid = %s>> ' % uid)
            return
        else:
            self.loger.warning('<<get uid = %s>>' % uid)
            rsssource = getRssSource(uid)
            self.start_urls.extend([rss[3] for rss in rsssource])
            self.rsssource = rsssource
            self.uid = uid

        self.rsstype = 'RSS2.0'
        self.encoding = 'utf-8'
        self.outformat = 1
        self.outdest = 1

    def adapt_response(self, response):
        # 获取应答的RSS相关元信息，重新进行相关设置
        getRssMeta(response)

        rss_source = [rss for rss in self.rsssource if rss[3] == response.url]
        if rss_source:
            self.loger.info("parse rssid=%d name=%s" %
                            (rss_source[0][0], rss_source[0][2]))
            self.rssid = rss_source[0][0]
        else:
            self.rssid = 0

        return XMLFeedSpider.adapt_response(self, response)

    def parse_node(self, response, selector):
        rssitem = RssdocItem()
        rssitem['rssid'] = self.rssid
        rssitem['author'] = selector.xpath('author/text()').extract()
        rssitem['title'] = selector.xpath('title/text()').extract()
        rssitem['url'] = selector.xpath('link/text()').extract()
        rssitem['pubdate'] = selector.xpath('pubDate/text()').extract()
        rssitem['desc'] = selector.select('description/text()').extract()
        rssitem['content'] = ''

        return rssitem
