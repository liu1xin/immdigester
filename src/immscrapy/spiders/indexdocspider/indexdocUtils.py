#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Created on 2015年8月27日

@author: liu1xin@outlook.com
'''

import urlparse
import urllib2
import os.path
from os.path import split as ospathsplit
from immscrapy.spiders.indexdocspider.indexdocItem import IndexdocItem


def checkurlvalid(url):
    if not url:
        return False
    elif not url.endswith('index.html'):
        return False

    try:
        urlfile = urllib2.urlopen(url)
        if 200 != urlfile.getcode():
            return False
    except:
        return False

    return True


def getbasedomin(url):
    if not url or 0 == len(url):
        return ''
    up = urlparse.urlparse(url)
    return up.netloc


def createItem(url, baseurl):
    ''' create index doc info from url '''
    doc = IndexdocItem()
    doc['docurl'] = url
    doc['docvalid'] = False

    if url.startswith(baseurl):
        filepath = url.replace(baseurl, '')
    else:
        doc['docname'] = ''
        return doc

    if '' == filepath:
        doc['docname'] = ''
    else:
        doc['docvalid'] = True
        doc['docpath'] = filepath.replace("/", os.path.sep)
        doc['docname'] = ospathsplit(doc['docpath'])[-1]

    return doc


def parselinkurl(linkurl, skippre, skipsuf):
    ''' check url can be request '''
    if not linkurl or '#' in linkurl:
        return ''
    if linkurl.startswith('/'):
        return ''

    for prefix in skippre:
        if linkurl.startswith(prefix):
            return ''

    for suffix in skipsuf:
        if linkurl.endswith(suffix):
            return ''

    return linkurl


if '__main__' == __name__:
    ''' do some test '''
    pass
