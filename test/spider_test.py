#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
#**************************************************************************
"""
Spider test

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-15
"""
import sys
import unittest

sys.path.append('../')
import spider.spider
import common.request


class SpiderTest(unittest.TestCase):
    """Spider unit test"""
    def test_crawl(self):
        """make a request, get the response"""
        sp = spider.spider.Spider()
        res = sp.crawl(common.request.Request('http://www.baidu.com', 0))
        self.assertIsNotNone(res.get_response())

        res = sp.crawl(common.request.Request('http://x.o.com', 0))
        self.assertIsNone(res.get_response())


if __name__ == '__main__':
    unittest.main()
