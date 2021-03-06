# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from scrapywork.models import ItemParser

class BasespiderTemplate(scrapy.Spider):

    def __init__(self,rule):
        self.rule=rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(',')
        self.urllist=[]
        super(BasespiderTemplate,self).__init__()

    def start_requests(self):
        try:
            for i in range(2,int(self.rule.pages),int(self.rule.pagestep)):
                url=self.rule.next_page_url.format(str(i))
                yield scrapy.Request(url,callback=self.parse_url)
        except:
            logging.error('basespider request failed :%s',self.rule.name)

    def parse_url(self,response):
        try:
            host_url=self.rule.host_url
            urls=re.findall(self.rule.url_regex,response.text)
            if self.rule.url_format:
                for url in urls:
                    self.urllist.append(self.rule.url_format.format(url[0],url[-1]))
                    print(self.rule.url_format.format(url[0],url[-1]))
            else:
                for url in urls:
                    self.urllist.append(host_url + url)
        except:
            logging.error('base spider urllist error： %s',self.rule.name)
        finally:
            for url in self.urllist:
                try:
                    url=url.replace('\\','')
                    yield scrapy.Request(url,callback=self.parse_item)
                except Exception as e:
                    logging.error('request error code: ',e)
                    continue

    def parse_item(self,response):
        logging.info('This is article page %s',response.url)
        print(response.url)
        itemparser=ItemParser(rule=self.rule,response=response)
        yield itemparser.parse_item()