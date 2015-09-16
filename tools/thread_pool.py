#!/usr/bin/env python
# -*- coding: gb18030 -*-
#**************************************************************************
# 
#   Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
#**************************************************************************
"""
This module implements an theadpool using
threading.Thread

Authors: zhaohui11(zhaohui11@baidu.com)
Date:    2015-09-12
"""
import Queue
import threading
import logging

class Worker(threading.Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: 
                func(*args, **kargs)
            except Exception as e: 
                logging.error("thread is failed, msg=%s" % (str(e)))
            self.tasks.task_done()


class ThreadPool(object):
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue.Queue(num_threads)
        for _ in range(num_threads): 
            Worker(self.tasks)
    
    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))
    
    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()
