#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 zhaoxiaohui.net, Inc. All Rights Reserved
#
#**************************************************************************
"""
This module specify the spider engines

Authors: downtownguy(downtownguy.hui@gmail.com)
Date:    2015-09-12
"""
import sys
import urllib2
import logging

sys.path.append('../common')
import common.request
import common.response

class BaseSpider(object):
    """
    spdier base class, every spider should inherit this class
    and implement the crawl method
    """
    def crawl(self, request):
        """implemented by the children"""
        return None


class RedirectHandler(urllib2.HTTPRedirectHandler):
    """forbid redirect"""
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    
    http_error_301 = http_error_302 
    
    http_error_303 = http_error_302 
    
    http_error_307 = http_error_302


class Spider(BaseSpider):
    """spider using urllib2"""
    def __init__(self):
        BaseSpider.__init__(self)
        opener = urllib2.build_opener(RedirectHandler)
        urllib2.install_opener(opener)
    
    def crawl(self, request):
        try:
            response = urllib2.urlopen(request.get_request(), timeout=request.get_timeout())
            logging.info("get %s succeed" % (request.get_request()))
            return common.response.Response(response, \
                                            request.get_request(), \
                                            request.get_index())
        except urllib2.URLError as e:
            logging.warn("get %s faild, msg:%s" % (request.get_request(), str(e)))
            return common.response.Response(None, request.get_request(), request.get_index())
