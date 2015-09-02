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


def getRssSources(uid):
    result = []

    if 1 == rssdocSetting.RSSDOC_SOURCETYPE:
        result.append(RS_RECORD(0, uid, u'TESTURL',
                                rssdocSetting.RSSDOC_SOURCEURL))
    elif 2 == rssdocSetting.RSSDOC_SOURCETYPE:
        dbconn = getRssDBConn()
        query_sql = r'''select id, user_id uid, name,url from rss_source
                     where tag=1 and user_id=:uid'''
        query_para = {'uid': uid}
        rows = sqlopt.executeQuery(dbconn, query_sql, query_para)
        for row in rows:
            result.append(RS_RECORD(row[0], row[1], row[2], row[3]))
        sqlopt.closeDbConn(dbconn)
    else:
        result = []

    return result


def getRssMeta(response):
    pass


def itemPrepare(outformat, item):
    item_p = None
    if outformat == rssdocSetting.RSSDOC_OUTFMT_TEXT:
        pass
    elif outformat == rssdocSetting.RSSDOC_OUTFMT_TUPLE:
        item_p = {}
        item_p['rssid'] = item['rssid']
        item_p['author'] = item['author'][0]
        item_p['title'] = item['title'][0]
        item_p['url'] = item['url'][0]
        item_p['desc'] = item['desc'][0]
        item_p['content'] = item['content']
        item_p['pubdate'] = item['pubdate'][0]
    elif outformat == rssdocSetting.RSSDOC_OUTFMT_JSON:
        pass
    elif outformat == rssdocSetting.RSSDOC_OUTFMT_XML:
        pass
    else:
        pass

    return item_p


def itemSave(outdest, itemsave, dbconn=None):
    if outdest == rssdocSetting.RSSDOC_OUTDEST_FILE:
        pass
    elif outdest == rssdocSetting.RSSDOC_OUTDEST_DB:
        dbconn = getRssDBConn()
        sql = r'''insert into rss_content(rss_id, pub_date, url, title, content)
                     values(:rssid, :pubdate, :url, :title, :content)'''
        sqlopt.executeSql(dbconn, sql, itemsave)
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
