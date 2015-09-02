#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年9月1日

@author: liu1xin@outlook.com
'''

import sqlite3


def getDbConn(dbfile):
    # 检查文件路径是否存在
    return sqlite3.connect(dbfile)


def closeDbConn(dbconn):
    # 检查连接
    dbconn.close()


def executeQuery(dbconn, sql, para=None):
    cur = dbconn.cursor()
    if para is not None:
        cur.execute(sql, para)
    else:
        cur.execute(sql)

    return cur.fetchall()


def executeSql(dbconn, sql, para=None):
    cur = dbconn.cursor()
    if para is not None:
        cur.execute(sql, para)
    else:
        cur.execute(sql)
    dbconn.commit()

    return True


if '__main__' == __name__:
    pass
