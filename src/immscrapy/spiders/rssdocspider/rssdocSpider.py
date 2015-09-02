#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import logging
from scrapy.spiders import XMLFeedSpider
from rssdocItem import RssdocItem
from rssdocUtils import getRssSources, getRssMeta


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
            rsssources = getRssSources(uid)
            if 0 == len(rsssources):
                self.loger.warning('rsssource not found for uid = %s!' % uid)
                return
            else:
                for record in rsssources:
                    self.loger.info('rssid=%s url=[%s]' % (record.id, record.url))
                self.start_urls.extend([record.url for record in rsssources])
                self.rsssources = rsssources

        self.uid = uid
        self.rsstype = 'RSS2.0'
        self.encoding = 'utf-8'
        self.outformat = 0
        self.outdest = 0

    def adapt_response(self, response):
        # 获取应答的RSS相关元信息，重新进行相关设置
        getRssMeta(response)

        rss_record_list = [record for record in self.rsssources
                           if record.url == response.url]

        if 1 == len(rss_record_list):
            rss_record = rss_record_list[0]
            self.loger.info("parse rssid=%d name=%s" %
                            (rss_record.id, rss_record.name))
            self.rssid = rss_record.id
        else:
            self.loger.warning('rsssource not found for url = %s!'
                               % response.url)
            self.rssid = 0

        return XMLFeedSpider.adapt_response(self, response)

    def parse_node(self, response, selector):
        rssitem = RssdocItem()
        rssitem['rssid'] = self.rssid
        if 'RSS2.0' == self.rsstype:
            rssitem['author'] = selector.xpath('author/text()').extract()
            rssitem['title'] = selector.xpath('title/text()').extract()
            rssitem['url'] = selector.xpath('link/text()').extract()
            rssitem['pubdate'] = selector.xpath('pubDate/text()').extract()
            rssitem['desc'] = selector.select('description/text()').extract()
            rssitem['content'] = ''

        return rssitem
