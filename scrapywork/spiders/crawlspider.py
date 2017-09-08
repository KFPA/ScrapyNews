# -*- coding: utf-8 -*-
import re
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapywork.models import ItemParser

class CrawlspiderTemplate(CrawlSpider):

    def __init__(self,rule):
        self.rule=rule
        self.name=rule.name
        self.start_urls=rule.start_urls.split(',')
        self.allowed_domains=rule.allow_domains.split(',')
        rule_list=[]
        # 添加`下一页`的规则
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page,unique=True),follow=True))
        #添加 '列表'的规则
        if rule.list_url:
            rule_list.append(Rule(LinkExtractor(allow=rule.list_url,unique=True),callback='parse_url',follow=True))
        #添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=rule.allow_url,unique=True),
            callback='parse_item',follow=True)
        )
        self.rules=tuple(rule_list)
        super(CrawlspiderTemplate,self).__init__()


    def parse_url(self,response):
        yield response
        logging.info('this is a list page %s'% response.url)
        pages=response.xpath(self.rule.list_page_total).extract_first()
        totalpage=re.findall(r'\d+',pages)
        if not totalpage:totalpage='1'
        logging.info('this is a pagetoal %s' % totalpage)
        for i in range(2,int(totalpage[0])+1):
           url=response.url.split('.html')[0]+'_{}.html'.format(i)
           logging.info('this ia list page %s' % url)
           yield Request(url)

    def parse_item(self, response):
        logging.info('this is article page %s' % response.url)

        itemparser=ItemParser(rule=self.rule,response=response)
        yield itemparser.parse_item()


