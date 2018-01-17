# -*- coding: utf-8 -*-
import scrapy
import re
from scrapywork.items import articleItem


class AutoSpider(scrapy.Spider):
    name = 'autoSpider'


    def __init__(self,rule):
        self.rule=rule
        self.allowed_domains = rule.allow_domains.split(',')
        self.urllist=[]
        super(AutoSpider,self).__init__()

    def start_requests(self):
        try:
            for i in range(1,int(self.rule.pages),int(self.rule.pagestep)):
                url=self.rule.next_page_url.format(str(i))
                yield scrapy.Request(url,callback=self.parse_url)
        except:
            print('autospider request failed')

    def parse_url(self,response):
        try:
            print(response.text)
            host_url=self.rule.host_url
            urls=re.findall(self.rule.url_regex,response.text)
            for url in urls:
                self.urllist.append(host_url+url)
        except:
            print('auto spider urllist error.')
        finally:
            for url in self.urllist:
                try:
                    url=url.replace('\\','')
                    yield scrapy.Request(url,callback=self.parse_item)
                except:
                    continue

    def parse_item(self,response):
        self.log('this is iaaf article page %s' % response.url)
        articleInfo = articleItem()
        parse_item(self.rule,response,articleInfo)
        yield articleInfo