#!/usr/bin/python 
# -*- coding:utf-8 -*-
# Author: nullne
# Email:  co.nullne@gmail.com
# DO:
# TODO:
#

import os
import sys
import time
import logging
import Queue
import threading
import requests
from bs4 import BeautifulSoup


URL_QUEUE = Queue.Queue()
DATA_QUEUE = Queue.Queue()
#STATUS_QUEUE = Queue.Queue()

class UrlThread(threading.Thread):
    """
    """
    def __init__(self, url_queue, data_queue, depth):
        threading.Thread.__init__(self)
        # why copy to here
        self.url_queue = url_queue
        self.data_queue = data_queue
        self.depth = depth

    def run(self):
        while True:
            #grabs host from queue
            host = self.url_queue.get()
            print host[0]

            if host[0] > self.depth:
                print 'not here'
            else:
                r = requests.get(host[1])
                if r.status_code == 200:
                    # encoding issues

                    #place the text into data queue
                    self.data_queue.put([host[0] + 1, r.text])
                    pass
                else:
                    #log the information
                    pass

            #signals to queue job is done
            self.url_queue.task_done()

class DatamineThread(threading.Thread):
    """
    """
    def __init__(self, url_queue, data_queue, key):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.data_queue = data_queue
        self.key = key

    def run(self):
        while True:
            #grabs chunk from the data queue

            chunk = self.data_queue.get()

            #parse the chunk
            soup = BeautifulSoup(chunk[1])

            #find the key


            #save to the page
            prefix = 'http://'
            for link in soup.find_all('a', href=True):
                if link['href'][:len(prefix)].lower() == prefix.lower():
                    #print link['href']
                    self.url_queue.put([chunk[0], link['href']])

            self.data_queue.task_done()

def check_end():
    while True:
        if DATA_QUEUE.empty() and URL_QUEUE.empty():
            STATUS_QUEUE.get()
            print "Done"
            STATUS_QUEUE.task_done()


def run(options):
    URL_QUEUE.put([0, options.url])
    #STATUS_QUEUE.put(1)
    #status_thread = threading.Thread(target=check_end)
    #status_thread.setDaemon(True)
    #status_thread.start()

    for i in range(options.thread):
        t = UrlThread(URL_QUEUE, DATA_QUEUE, options.depth)
        t.setDaemon(True)
        t.start()
    for i in range(options.thread):
        t = DatamineThread(URL_QUEUE, DATA_QUEUE, options.key)
        t.setDaemon(True)
        t.start()

    #STATUS_QUEUE.join
    URL_QUEUE.join()
    DATA_QUEUE.join()

def main():
    import argparse

    project_path = os.path.abspath(os.path.join(__file__, os.path.pardir))

    logger = logging.getLogger('spider')
    logging.basicConfig(filename=os.path.join(project_path, 'runtime', 'spider.log'), 
            format="[%(asctime)s] %(levelname)s: %(message)s", 
            filemode='w', 
            datefmt='%m/%d/%Y %H:%M:%S')

    parser = argparse.ArgumentParser(prog="nullne's spider", description="Amazing spider")
    #positional arguments
    parser.add_argument('-u', '--url', required=True, 
            help='URL to be crawled')
    parser.add_argument("-d", dest="depth", type=int, required=True,
            help="the crawler depth")
    parser.add_argument("-D", "--dbfile", required=True,
            help="sqlite database file to store the results")

    #optional arguments
    parser.add_argument("-k", "--key",  
            help="key word")
    parser.add_argument("-l", type=int, dest="location", 
            help="log file location, default is ./runtime/spider.log")
    parser.add_argument("-t", "--thread", type=int, default=10, 
            help="numbers of thead, default is 10")
    parser.add_argument("-T", "--testself", action="store_true",
            help="self test")
    parser.add_argument("-v", "--verbosity", action="count",
            help="increase logging verbosity")

    args = parser.parse_args()
    if args.verbosity >=2:
        logger.setLevel(logging.DEBUG)
    elif args.verbosity >=1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    try:
        run(args)
    except KeyboardInterrupt:
        print "Err, your order..."
        sys.exit(1)
if __name__ == "__main__":
    main()
