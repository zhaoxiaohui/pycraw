#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
#**************************************************************************
"""
This module provides thread safe set operation

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
import threading
import tools

class SafeDict(object):
    """
    thread safe cache
    used to store the urls crawled
    """
    def __init__(self):
        self.__links = set()
        self.__items = set()
        self.__link_lock = threading.Lock()
        self.__item_lock = threading.Lock()

    def check_link_in(self, url):
        """
        check url of a new link, if not exists, the url 
        will be put into the cache
        Args:
            url             - a full url of a link
        Returns
            True            - url exists
            False           - url not exists
        """
        url_hash = tools.url_hash(url)
        if url_hash not in self.__links:
            self.__link_lock.acquire()
            self.__links.add(url_hash)
            self.__link_lock.release()
            return False
        else:
            return True

    def check_item_in(self, url):
        """
        check url of a new item, if not exists, the url 
        will be put into the cache
        Args:
            url             - a full url of a item
        Returns
            True            - url exists
            False           - url not exists

        """
        item_hash = tools.url_hash(url)
        if item_hash not in self.__items:
            self.__item_lock.acquire()
            self.__items.add(item_hash)
            self.__item_lock.release()
            return False
        else:
            return True
