#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
#  
#  Copyright (c) 2015 zhaoxiaohui.net, Inc. All Rights Reserved
#  
#**************************************************************************
"""
An request

Authors: downtownguy(downtownguy.hui@gmail.com)
Date:    2015-09-12
"""
class Request(object):
    """an request"""
    def __init__(self, request, index, timeout=1):
        """
        Args:
            request         - an instance that can be called by urllib2.urlopen
                              in this demo, it is just a full url string
            index           - the depth of this request
            timeout         - how much time you want me to wait for requesting this
                              request
        """
        self.__request = request
        self.__index = index
        self.__timeout = timeout
    
    def get_request(self):
        """get the request(i.e. the url)"""
        return self.__request
    
    def get_index(self):
        """get this request depth"""
        return self.__index
    
    def get_timeout(self):
        """get the time for this url to make a request"""
        return self.__timeout
