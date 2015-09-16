#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
#**************************************************************************
"""
Extractor test

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-15
"""
import sys
import unittest

sys.path.append('../')
import spider.spider
import common.request
import extractor.extractor

class ExtractorTest(unittest.TestCase):
    """get an response, extract links"""
    def test_parse(self):
        """parse"""
        sp = spider.spider.Spider()
        res = sp.crawl(common.request.Request('http://pycm.baidu.com:8081', 0))
        ex = extractor.extractor.Extractor()
        links, items = ex.parse(res)
        self.assertEqual(5, len(links))
        self.assertEqual(0, len(items))

        res = sp.crawl(common.request.Request('http://pycm.baidu.com:8081/3/page3_4.html', 0))
        links, items = ex.parse(res)
        self.assertEqual(0, len(links))
        self.assertEqual(1, len(items))


if __name__ == '__main__':
    unittest.main()

