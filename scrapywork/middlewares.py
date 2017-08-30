# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from scrapywork.settings import IPPOOL
from scrapywork.spiders.ipSpider import initIPPOOL

from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapywork.settings import UAPOOL

from scrapy.http import Request
from scrapy.utils.url import canonicalize_url


class ScrapyworkSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class IpPoolsMiddleware(HttpProxyMiddleware):
    def __init__(self,ip=''):
        self.ip=ip
        initIPPOOL()
    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL)
        print('the current ip is:'+ thisip['ipaddr'])
        request.meta['proxy']='http://'+thisip['ipaddr']


class UaPoolsMiddleware(UserAgentMiddleware):
    def __init__(self,user_agent=''):
        self.user_agent=user_agent
    def process_request(self, request, spider):
        thisua=random.choice(UAPOOL)
        print('the current user-agent is:'+ thisua)
        request.headers.setdefault('User-Agent',thisua)

class UrlCanonicalizerMiddleware(object):
    def process_spider_output(self,response,result,spider):
        for r in result:
            if isinstance(r,Request):
                curl=canonicalize_url(r.url)
                if curl != r.url:
                    r=r.replace(url=curl)
            yield r

from scrapywork.models import mysqldb
from pybloom import ScalableBloomFilter
from scrapy.dupefilter import RFPDupeFilter
import hashlib
class UrlFilter(RFPDupeFilter):
    def __init__(self,path=None,debug=False):
        self.urls_sbf=ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        RFPDupeFilter.__init__(self,path,debug)
    def request_seen(self, request):

        fp=hashlib.sha1()
        fp.update(canonicalize_url(request.url).encode('utf-8'))
        url_sha1=fp.hexdigest()
        if url_sha1 not in self.urls_sbf and not mysqldb.queryItem(request.url):
            self.urls_sbf.add(url_sha1)
        else:
            return True




