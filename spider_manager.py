#!/usr/bin/env python
# -*- coding: gb18030 -*-
#***************************************************************************
# 
#   Copyright (c) 2015 zhaoxiaohui.net, Inc. All Rights Reserved
# 
#***************************************************************************
"""
This module manages the spider engines.
Using thread pool

Authros: downtownguy(downtownguy.hui@gmail.com)
Date:    2015-09-12
"""
import Queue
import threading
import logging
import time

import spider.spider
import tools.thread_pool

def spider_work(spider, stop_event, interval, req_queue, res_queue, id):
    """
    The schedule process
    Getting a reqest from global request queue then
    call the spider engine to deal giving back
    the response which will be put into the global response
    queue
    If geting request beyound the given time, 
    the task is assumed done

    Args:
        spider              - the engine for crawl
        stop_event          - threading.Event instance to check exit
        interval            - thread interval
        req_queue           - the global request queue(blocking queue)
        res_queue           - the global response queue(blocking queue)
        id                  - which thread handle this work
    """
    while not stop_event.isSet():
        try:
            request = req_queue.get(True, 1)
            response = spider.crawl(request)
            res_queue.put(response)
            time.sleep(interval)
        except Queue.Empty as e:
            continue
    logging.info("spider[%d] task done" % (id))


class SpiderManager(threading.Thread):
    """Spider pool"""
    def __init__(self, stop_event, thread_num, interval, req_queue, res_queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__spider = spider.spider.Spider()
        self.__stop_event = stop_event
        self.__thread_num = thread_num
        self.__interval = interval
        self.__req_queue = req_queue
        self.__res_queue = res_queue

    def run(self):
        self.__run()

    def __run(self):
        spider_pool = tools.thread_pool.ThreadPool(self.__thread_num)
        for i in range(0, self.__thread_num):
            spider_pool.add_task(spider_work, self.__spider, self.__stop_event, \
                                 self.__interval, self.__req_queue, \
                                 self.__res_queue, i)
        logging.info("spider initalize done, begining to explore.")
        spider_pool.wait_completion()



