#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 zhaoxiaohui.net, Inc. All Rights Reserved
# 
#**************************************************************************
"""
This moudle manages the link extractor egines
Using thread pool

Authors: downtownguy(downtownguy.hui@gmail.com)
Date:    2015-09-12
"""
import Queue
import threading
import logging

import extractor.extractor
import tools.thread_pool

def extractor_work(extractor, stop_event, res_queue, item_queue, \
                   link_queue, dicts, id):
    """
    The schedule process.
    Get a response from global response queue then call the 
    extractor engine to do the real work holding the links and 
    items which will be put into the corresponding global link queue
    and item queue

    Args:
        extractor               - link extractor engine
        stop_event              - threading.Event instance to check exit
        res_queue               - global response queue(blocking queue)
        item_queue              - global item queue(blocking queue) using to
                                  hold the resources(e.g. png/gif/jpg...)
        link_queue              - global link queue(blocking queue) using to
                                  hold the hypelink
        dicts                   - global url cache contains urls of items and links
                                  already being crawled
        id                      - which thread handle this work 
    """
    while not stop_event.isSet():
        try:
            response = res_queue.get(True, 1)
            links, items = extractor.parse(response)
            logging.debug("from[%s] get [%d]links and [%d]items" % \
                          (response.get_origin_url(), len(links), len(items)))
            for item in items:
                if not dicts.check_item_in(item.get_url()):
                    item_queue.put(item)
            for link in links:
                if not dicts.check_link_in(link.get_url()):
                    link_queue.put(link)
        except Queue.Empty as e:
            continue
    logging.info("extractor[%d] task done" % (id))


class ExtractorManager(threading.Thread):
    """extractor pool"""
    def __init__(self, stop_event, thread_num, targetre, \
                 res_queue, item_queue, link_queue, dicts):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__extractor = extractor.extractor.Extractor(targetre)
        self.__stop_event = stop_event
        self.__thread_num = thread_num
        self.__res_queue = res_queue
        self.__item_queue = item_queue
        self.__link_queue = link_queue
        self.__dicts = dicts
    
    def run(self):
        self.__run()
    
    def __run(self):
        extractor_pool = tools.thread_pool.ThreadPool(self.__thread_num)
        for i in range(0, self.__thread_num):
            extractor_pool.add_task(extractor_work, self.__extractor, \
                                    self.__stop_event, self.__res_queue, \
                                    self.__item_queue, self.__link_queue, \
                                    self.__dicts, i)
        logging.info("extractor initalize done, begining to explore.")
        extractor_pool.wait_completion()




