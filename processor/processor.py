#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#**************************************************************************
"""
This module specify the processor engines

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
import sys
import urllib
import logging

sys.path.append('../common')
import common.item
import common.request

class BaseProcessor(object):
    """
    processor base class, every processor should inherit this class
    and implement the process_item and process_link method
    """
    def process_item(self, item):
        """deal with the page resources"""
        return None
    
    def process_link(self, link):
        """deal with the page links"""
        return None


class Processor(BaseProcessor):
    """
    Simple processor saving the item and simply encapsulating
    a link to a request instance
    """
    def __init__(self, dest):
        BaseProcessor.__init__(self)
        self.__item_dest = dest

    def process_item(self, item):
        """saving this item to disk"""
        filename = urllib.quote_plus(item.get_url())
        dest = self.__item_dest + "/" + filename
        try:
            urllib.urlretrieve(item.get_url(), dest)
            logging.info("save %s to %s successfully" % (item.get_url(), dest))
        except IOError as e:
            logging.error("save %s encounter an problem, msg=%s" % (item.get_url(), str(e)))
        except urllib.ContentTooShortError as e:
            logging.error("save %s interrupted, msg=%s" % (item.get_url(), str(e)))
        return None

    def process_link(self, link):
        """simply encapsulate the link to a request instance"""
        return common.request.Request(link.get_url(), link.get_index())
