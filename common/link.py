#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
#  
#  Copyright (c) 2015 zhaoxiaohui.net, Inc. All Rights Reserved
#  
#**************************************************************************
"""
Original link extracted from the page

Authors: zhahohui11(downtownguy.hui@gmail.com)
Date:    2015-09-12
"""
class Link(object):
    """original link"""
    def __init__(self, url, index):
        """
        Args:
            url         - the full url
            index       - the depth of this link
        """
        self.__url = url
        self.__index = index
    
    def get_url(self):
        """get the full url"""
        return self.__url
    
    def get_index(self):
        """get the depth'"""
        return self.__index
