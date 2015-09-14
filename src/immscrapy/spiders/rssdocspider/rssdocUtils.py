#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

from collections import namedtuple
import immtools.sqliteoperator as sqlopt
import rssdocSetting

RS_RECORD = namedtuple('RS_RECORD', 'id uid name url')


def getRssSources(uid, dbconn=None):
    result = []

    if 1 == rssdocSetting.RSSDOC_SOURCETYPE:
        result.append(RS_RECORD(0, uid, u'TESTURL',
                                rssdocSetting.RSSDOC_SOURCEURL))
    elif 2 == rssdocSetting.RSSDOC_SOURCETYPE:
        query_sql = r'''select id, user_id uid, name,url from rss_source
                     where tag=1 and user_id=:uid'''
        query_para = {'uid': uid}
        rows = sqlopt.executeQuery(dbconn, query_sql, query_para)
        for row in rows:
            result.append(RS_RECORD(row[0], row[1], row[2], row[3]))
    else:
        result = []

    return result


def getRssMeta(response):
    pass


def rssdocItemReady(outformat, item):
    item_out = {}
    item_out['guid'] = item['guid']
    item_out['rssid'] = item['rssid']
    item_out['author'] = item['author']
    item_out['title'] = item['title']
    item_out['url'] = item['url']
    item_out['desc'] = item['desc']
    item_out['content'] = item['desc']
    item_out['pubdate'] = item['pubdate']
    item_out['category'] = item['category']

    if item_out['guid'] is None:
        item_out['guid'] = item_out['url']
    if item_out['category'] is None:
        item_out['category'] = ''

    return item_out


def rssdocItemSave(outdest, itemsave, dbconn=None):
    if rssdocSetting.RSSDOC_OUTDEST_NULL == outdest:
        return True
    elif rssdocSetting.RSSDOC_OUTDEST_DB == outdest:
        if dbconn is not None:
            sql = r'''select id from rss_content
                        where guid=:guid and rss_id=:rssid'''
            qresult = sqlopt.executeQuery(dbconn, sql, itemsave)
            if qresult is not None and 1 == len(qresult):
                return True
            sql = r'''insert into rss_content(guid, rss_id, pub_date, url,
                title, content, category) values(:guid, :rssid, :pubdate,
                :url, :title, :content, :category)'''
            sqlopt.executeSql(dbconn, sql, itemsave)
        else:
            return False
    elif rssdocSetting.RSSDOC_OUTDEST_FILE == outdest:
        pass
    else:
        pass

    return True


def getRssDBConn():
    dburl = rssdocSetting.RSSDOC_CONNECTINFO
    dbconn = sqlopt.getDbConn(dburl)
    return dbconn


def closeRssDBConn(dbconn):
    sqlopt.closeDbConn(dbconn)


if '__main__' == __name__:
    ''' do some test '''
    pass
