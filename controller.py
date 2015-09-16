#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#    Copyright (c) 2015 zhaoxiaohui.net, Inc. All Rights Reserved
# 
#**************************************************************************
"""
This moudle is the central controller.
Initializing the three managers and start the crawling
work.

Authors: downtownguy(downtownguy.hui@gmail.com)
Date:    2012-09-13
"""
import Queue
import logging
import threading
import time

import safe_dict
import spider_manager
import extractor_manager
import processor_manager
import common.request

class Monitor(threading.Thread):
    """monitor status"""
    def __init__(self, stop_event, \
                 req_queue, res_queue, link_queue, item_queue):
        threading.Thread.__init__(self)
        self.__stop_event = stop_event
        self.__req_queue = req_queue
        self.__res_queue = res_queue
        self.__link_queue = link_queue
        self.__item_queue = item_queue

    def __check_empty(self):
        if self.__req_queue.empty() and \
           self.__res_queue.empty() and \
           self.__item_queue.empty() and \
           self.__link_queue.empty():
            return True

    def __status(self):
        logging.info("four queue size[res, req, link, item] => [%d, %d, %d, %d]" % \
                     (self.__req_queue.qsize(), self.__res_queue.qsize(), \
                      self.__link_queue.qsize(), self.__item_queue.qsize()))
    
    def run(self):
        empty_max_time = 5
        empty_time = 0
        while True:
            if self.__check_empty():
                empty_time += 1
                if empty_time >= empty_max_time:
                    self.__stop_event.set()
                    break
            self.__status()
            time.sleep(2)


class Controller(object):
    """CPU"""
    def __init__(self, conf):
        self.__conf = conf
        self.__stop_event = threading.Event()
        self.__init_queues()
    
    def __init_queues(self):
        self.__req_queue = Queue.Queue()
        self.__res_queue = Queue.Queue()
        self.__item_queue = Queue.Queue()
        self.__link_queue = Queue.Queue()
        
    def run(self, start_urls):
        """
        start to crawler
        """
        dicts = safe_dict.SafeDict()
        for url in start_urls:
            req = common.request.Request(url, 0, self.__conf['req_timeout'])
            if not dicts.check_link_in(url):
                self.__req_queue.put(req)
        sm = spider_manager.SpiderManager(self.__stop_event, \
                                          self.__conf['spider_thread_num'], \
                                          self.__conf['spider_interval'], \
                                          self.__req_queue, \
                                          self.__res_queue)
        em = extractor_manager.ExtractorManager(self.__stop_event, \
                                                self.__conf['extractor_thread_num'], \
                                                self.__conf['target_url'], \
                                                self.__res_queue, \
                                                self.__item_queue, \
                                                self.__link_queue, dicts)
        pm = processor_manager.ProcessorManager(self.__stop_event, \
                                                self.__conf['item_thread_num'], \
                                                self.__conf['link_thread_num'], \
                                                self.__item_queue, \
                                                self.__link_queue, \
                                                self.__req_queue, \
                                                self.__conf['depth'], \
                                                self.__conf['output'])
        sm.start()
        em.start()
        pm.start()
        monitor = Monitor(self.__stop_event, self.__req_queue, self.__res_queue, \
                          self.__link_queue, self.__item_queue)
        monitor.start()
        sm.join()
        em.join()
        pm.join()
        monitor.join()
        logging.info("All works are done, going to exit")


if __name__ == '__main__':
    Controller({}).run(['http://www.sina.com/'])
