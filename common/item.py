#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
#  
#  Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#  
#**************************************************************************
"""
Resource element(e.g. png/gif/bmp...)

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
class Item(object):
    """page resource element"""
    def __init__(self, url, type='png'):
        """
        Args:
            url         - the full link
            type        - type of the resource
        """
        self.__url = url
        self.__type = type
    
    def get_url(self):
        """get the full url"""
        return self.__url
    
    def get_type(self):
        """get the item type"""
        return self.__type
