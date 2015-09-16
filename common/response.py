#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
#  
#  Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#  
#**************************************************************************
"""
A response encapsulation

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
class Response(object):
    """a response encapsulation"""
    def __init__(self, response, url, index):
        """
        Args:
            response            - an instanse return by the urllib2.urlopen
            url                 - which url called this response
            index               - the depth of this response(i.e. the request's depth)
        """
        self.__response = response
        self.__index = index
        self.__origin_url = url
    
    def get_response(self):
        """get the response(i.e. the instanse of the return of urllib2.urlopen)"""
        return self.__response
    
    def get_index(self):
        """get this page depth"""
        return self.__index
    
    def get_origin_url(self):
        """get this page real url"""
        return self.__origin_url
