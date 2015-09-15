#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import logging
from scrapy.spiders import XMLFeedSpider
from immscrapy.spiders.rssdocspider.rssdocItem import RssdocItem
from immscrapy.spiders.rssdocspider.rssdocUtils import (getRssSources,
                                                        getRssMeta,
                                                        getRssDBConn)


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

        self.loger.warning('<<get uid = %s>>' % uid)
        self.uid = uid
        self.dbconn = getRssDBConn()
        rsssources = getRssSources(uid, self.dbconn)
        if 0 == len(rsssources):
            self.loger.warning('rsssource not found for uid = %s!' % uid)
            return
        else:
            for record in rsssources:
                self.loger.info('rssid=%s url=[%s]' % (record.id, record.url))
            self.start_urls.extend([record.url for record in rsssources])
            self.rsssources = rsssources

        self.rsstype = 'RSS2.0'
        self.encoding = 'utf-8'

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
            rssitem['guid'] = selector.xpath('guid/text()').extract_first()
            rssitem['author'] = selector.xpath('author/text()').extract_first()
            rssitem['title'] = selector.xpath('title/text()').extract_first()
            rssitem['url'] = selector.xpath('link/text()').extract_first()
            rssitem['pubdate'] = selector.xpath('pubDate/text()').extract_first()
            rssitem['desc'] = selector.xpath('description/text()').extract_first()
            rssitem['category'] = selector.xpath('category/text()').extract_first()
            rssitem['content'] = ''

        return rssitem
