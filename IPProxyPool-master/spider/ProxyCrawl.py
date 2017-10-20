# coding:utf-8
from gevent import monkey
monkey.patch_all()

import sys
import time
import gevent

from gevent.pool import Pool
from multiprocessing import Queue, Process, Value

from api.apiServer import start_api_server
from config import THREADNUM, parserList, UPDATE_TIME, MINNUM, MAX_CHECK_CONCURRENT_PER_PROCESS, MAX_DOWNLOAD_CONCURRENT
from db.DataStore import store_data, sqlhelper
from spider.HtmlDownloader import Html_Downloader
from spider.HtmlPraser import Html_Parser
from validator.Validator import validator, getMyIP, detect_from_db

'''
这个类的作用是描述爬虫的逻辑
'''


def startProxyCrawl(queue, db_proxy_num,myip):
    crawl = ProxyCrawl(queue, db_proxy_num,myip)
    crawl.run()


class ProxyCrawl(object):
    proxies = set()

    def __init__(self, queue, db_proxy_num,myip):
        self.crawl_pool = Pool(THREADNUM)
        self.queue = queue
        self.db_proxy_num = db_proxy_num
        self.myip = myip


    def run(self):
        while True:
            self.proxies.clear()
            str = 'IPProxyPool----->>>>>>>>beginning'
            sys.stdout.write(str + "\r\n")
            sys.stdout.flush()
            proxylist = sqlhelper.select()

            spawns = []
            for proxy in proxylist:
                spawns.append(gevent.spawn(detect_from_db, self.myip, proxy, self.proxies))
                if len(spawns) >= MAX_CHECK_CONCURRENT_PER_PROCESS:
                    gevent.joinall(spawns)
                    spawns= []
            gevent.joinall(spawns)
            self.db_proxy_num.value = len(self.proxies)
            str = 'IPProxyPool----->>>>>>>>db exists ip:%d' % len(self.proxies)

            if len(self.proxies) < MINNUM:
                str += '\r\nIPProxyPool----->>>>>>>>now ip num < MINNUM,start crawling...'
                sys.stdout.write(str + "\r\n")
                sys.stdout.flush()
                spawns = []
                for p in parserList:
                    spawns.append(gevent.spawn(self.crawl, p))
                    if len(spawns) >= MAX_DOWNLOAD_CONCURRENT:
                        gevent.joinall(spawns)
                        spawns= []
                gevent.joinall(spawns)
            else:
                str += '\r\nIPProxyPool----->>>>>>>>now ip num meet the requirement,wait UPDATE_TIME...'
                sys.stdout.write(str + "\r\n")
                sys.stdout.flush()

            time.sleep(UPDATE_TIME)

    def crawl(self, parser):
        html_parser = Html_Parser()
        for url in parser['urls']:
            response = Html_Downloader.download(url)
            if response is not None:
                proxylist = html_parser.parse(response, parser)
                if proxylist is not None:
                    for proxy in proxylist:
                        proxy_str = '%s:%s' % (proxy['ip'], proxy['port'])
                        if proxy_str not in self.proxies:
                            self.proxies.add(proxy_str)
                            while True:
                                if self.queue.full():
                                    time.sleep(0.1)
                                else:
                                    self.queue.put(proxy)
                                    break


if __name__ == "__main__":
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue()
    q2 = Queue()
    p0 = Process(target=start_api_server)
    p1 = Process(target=startProxyCrawl, args=(q1, DB_PROXY_NUM))
    p2 = Process(target=validator, args=(q1, q2))
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM))

    p0.start()
    p1.start()
    p2.start()
    p3.start()

    # spider = ProxyCrawl()
    # spider.run()
