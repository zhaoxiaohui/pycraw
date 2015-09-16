#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
#**************************************************************************
"""
This module manages the processor engines.
Using thread pool

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
import Queue
import threading
import logging

import processor.processor
import tools.thread_pool

def item_work(processor, stop_event, item_queue, id):
    """
    The schedule process
    Getting an item from global item_queue then
    call the processor engine to deal

    Args:
        processor           - the engine for process
        stop_event          - threading.Event instance to check exit
        item_queue          - the global item queue(blocking queue)
        id                  - which thread handle this work
    """
    while not stop_event.isSet():
        try:
            item = item_queue.get(True, 1)
            processor.process_item(item)
        except Queue.Empty as e:
            continue
    logging.info("processor:item[%d] task done" % (id))


def link_work(processor, stop_event, link_queue, req_queue, depth, id):
    """
    The schedule process
    Get a link form global link queue then call the processor
    engine to deal giving back the request which will be
    put into the global request queue if the link depth is under
    the given depth

    Args:
        processor           - the engine for process
        stop_event          - threading.Event instance to check exit
        link_queue          - the global link queue(blocking queue)
        req_queue           - the global request queue(blocking queue)
        depth               - the upper limit of the depth of crawling
        id                  - which thread handle this work
    """
    while not stop_event.isSet():
        try:
            link = link_queue.get(True, 1)
            if link.get_index() < depth:
                request = processor.process_link(link)
                req_queue.put(request)
        except Queue.Empty as e:
            #todo
            continue
    logging.info("processor:link[%d] task done" % (id))


class LinkManager(threading.Thread):
    """link pool"""
    def __init__(self, processor, stop_event, link_thread_num, \
                 link_queue, req_queue, depth):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__processor = processor
        self.__stop_event = stop_event
        self.__link_thread_num = link_thread_num
        self.__link_queue = link_queue
        self.__req_queue = req_queue
        self.__depth = depth

    def run(self):
        self.__run()

    def __run(self):
        link_pool = tools.thread_pool.ThreadPool(self.__link_thread_num)
        for i in range(0, self.__link_thread_num):
            link_pool.add_task(link_work, self.__processor, self.__stop_event, \
                               self.__link_queue, self.__req_queue, \
                               self.__depth, i)
        logging.info("processor:link initialize done, begining to explre.")
        link_pool.wait_completion()


class ItemManager(threading.Thread):
    """item pool"""
    def __init__(self, processor, stop_event, item_thread_num, item_queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__processor = processor
        self.__stop_event = stop_event
        self.__item_thread_num = item_thread_num
        self.__item_queue = item_queue
    
    def run(self):
        self.__run()
    
    def __run(self):
        item_pool = tools.thread_pool.ThreadPool(self.__item_thread_num)
        for i in range(0, self.__item_thread_num):
            item_pool.add_task(item_work, self.__processor, \
                               self.__stop_event, self.__item_queue, i)
        logging.info("processor:item initialize done, begining to explre.")
        item_pool.wait_completion()
    

class ProcessorManager(object):
    """manipulate LinkManager and ItemManager"""
    def __init__(self, stop_event, item_thread_num, link_thread_num, \
                 item_queue, link_queue, req_queue, depth, output='./output/'):
        self.__processor = processor.processor.Processor(output)
        self.__link_manager = LinkManager(self.__processor, \
                                          stop_event, \
                                          link_thread_num, \
                                          link_queue, \
                                          req_queue, \
                                          depth)
        self.__item_manager = ItemManager(self.__processor, \
                                          stop_event, \
                                          item_thread_num, \
                                          item_queue)
    
    def start(self):
        """start processor manger(start link and item manager)"""
        self.__link_manager.start()
        self.__item_manager.start()

    def join(self):
        """wait for link and item manager to finish"""
        self.__link_manager.join()
        self.__item_manager.join()
    
   
