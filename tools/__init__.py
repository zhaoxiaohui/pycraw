#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#**************************************************************************
"""
Useful tools

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
import base64

def url_hash(url):
    """base64 url hash"""
    return base64.urlsafe_b64encode(url)
