#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#    Copyright (c) 2015 zhaoxiaohui.net, Inc. All Rights Reserved
# 
#**************************************************************************

"""
This modoule is to initialize all needed and 
start the controller

Authors: downtownguy(downtownguy.hui@gmail.com)
Date: 2015-09-15
"""
import logging
import argparse
import ConfigParser

import log
import controller


def parse_args():
    """generate args"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', help='specify the conf file')
    parser.add_argument('urls', help='an url file, one on a line')
    return parser.parse_args()


class MiniSpider(object):
    """main entry"""
    __DEFAULT_CONF = {
        'spider_thread_num': '5',
        'extractor_thread_num': '5',
        'item_thread_num': '5',
        'link_thread_num': '5',
        'spider_interval': '0.05',
        'depth': '2',
        'req_timeout': '5',
        'output': './output',
        'target_url': '<img[^>]*\ssrc=(.*?)[/ ]?>',
        'log_path': './log/pycraw'
    }

    def __init__(self, args):
        self.urls = args.urls
        self.conf = {}
        self._read_conf(args.conf)

    def _read_conf(self, conf_file):
        """initialize the conf"""
        cf = ConfigParser.SafeConfigParser(MiniSpider.__DEFAULT_CONF)
        cf.read(conf_file)
        self.conf['spider_thread_num'] = cf.getint('spider', 'spider_thread_num')
        self.conf['extractor_thread_num'] = cf.getint('spider', 'extractor_thread_num')
        self.conf['item_thread_num'] = cf.getint('spider', 'item_thread_num')
        self.conf['link_thread_num'] = cf.getint('spider', 'link_thread_num')
        self.conf['spider_interval'] = cf.getfloat('spider', 'spider_interval')
        self.conf['depth'] = cf.getint('spider', 'depth')
        self.conf['req_timeout'] = cf.getint('spider', 'req_timeout')
        self.conf['output'] = cf.get('spider', 'output')
        self.conf['target_url'] = cf.get('spider', 'target_url')
        self.conf['log_path'] = cf.get('spider', 'log_path')

    def run(self):
        """go to war"""
        print "Spider start"

        log.init_log(self.conf['log_path'])
        contr = controller.Controller(self.conf)
        
        start_urls = []
        with open(self.urls, 'r') as url_handler:
            start_urls = url_handler.readlines()

        print start_urls
        contr.run(start_urls)
        
        print "Spider done..."


if __name__ == '__main__':
    """entry"""
    minis = MiniSpider(parse_args())
    minis.run()




