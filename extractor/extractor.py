#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#**************************************************************************
"""
This module specify the link extractor engines

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
import sys
import urllib2
import urlparse
import logging
import re

import chardet

sys.path.append('../common')
import common.item
import common.link

def clean_link(link_text):
    """Remove leading and trailing whitespace and punctuation"""
    return link_text.strip("\t\r\n '\"")


def clean_url(url, base_url):
    """join and clean the url"""
    clean_url = ''
    try:
        clean_url = urlparse.urljoin(base_url, clean_link(url))
    except ValueError:
        pass
    return clean_url


class BaseExtractor(object):
    """
    extractor base class, every extractor should inherit
    this class and implement the parse method
    """
    def parse(self, response):
        """
        parse the page, get the links and items

        Returns:
            a tuple (links, items)
        """
        return ([], [])

    def _process_links(self, links):
        """ 
        Normalize and filter extracted links
        The subclass should override it if necessary
        """
        links = unique_list(links, key=lambda link: link.get_url())
        return links


class Extractor(BaseExtractor):
    """regex extractor"""
    def __init__(self, targetre="<img[^>]*\ssrc=(.*?)[/ ]?>"):
        BaseExtractor.__init__(self)
        linkre="<a\s.*?href=(\"[.#]+?\"|\'[.#]+?\'|[^\s]+?)(>|\s.*?>)(.*?)<[/ ]?a>"
        self.__linkre = re.compile(linkre, re.DOTALL | re.IGNORECASE)
        self.__itemre = re.compile(targetre, re.DOTALL | re.IGNORECASE)
    
    def parse(self, response):
        if response is None:
            logging.error("None object")
            return ([], [])
        if response.get_response() is None:
            logging.error("%s get a None page" % (response.get_origin_url()))
            return ([], [])
        res = response.get_response()
        logging.debug("%s response code:%s" % (res.geturl(), res.getcode()))
        body = self.__decode(res.read(), response.get_origin_url())
        if body is not None:
            links, items = self.__get_hyperlinks(body, response)
            return (links, items)
        return ([], [])
    
    def __get_hyperlinks(self, body, response):
        """get page hypelinks and classify them to links and items"""
        links_text = self.__linkre.findall(body)
        base_url = response.get_origin_url()
        next_ind = response.get_index() + 1
        links = [common.link.Link(clean_url(url, base_url), next_ind) for url, _, _ in links_text]

        items_text = self.__itemre.findall(body)
        items = [common.item.Item(clean_url(url, base_url)) for url in items_text]
        return (links, items)
     
    def __decode(self, body, url):
        """decode the response body"""
        detect_dict = chardet.detect(body)
        if isinstance(body, unicode):
            return body
        else:
            if detect_dict['encoding'] == 'GB2312':
                try:
                    res = body.decode('gbk')
                    return res
                except UnicodeError as e:
                    logging.error("decode %s failed, msg=%s" % (url, str(e)))
                    return None
            else:
                try:
                    res = body.decode(detect_dict['encoding'])
                    return res
                except UnicodeError as e:
                    loggind.error("decode %s failed, msg=%s" % (url, str(e)))
                    return None


