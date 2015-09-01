#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import immtools.sqliteoperator as sqlopt
import rssdocSetting


def getRssSource(uid):
    result = []

    if 1 == rssdocSetting.RSSDOC_SOURCETYPE:
        result.append((0, uid, u'TESTURL', rssdocSetting.RSSDOC_SOURCEURL))
    elif 2 == rssdocSetting.RSSDOC_SOURCETYPE:
        dbconn = getRssDBConn()
        query_sql = r'''select id, user_id uid, name,url from rss_source
                     where tag=1 and user_id=:uid'''
        query_para = {'uid': uid}
        result = sqlopt.executeQuery(dbconn, query_sql, query_para)
        sqlopt.closeDbConn(dbconn)
    else:
        result = []

    return result


def getRssMeta(response):
    pass


def getRssDBConn():
    dburl = rssdocSetting.RSSDOC_CONNECTINFO
    dbconn = sqlopt.getDbConn(dburl)
    return dbconn


def closeRssDBConn(dbconn):
    sqlopt.closeDbConn(dbconn)


if '__main__' == __name__:
    ''' do some test '''
    pass
