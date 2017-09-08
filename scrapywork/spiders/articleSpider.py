# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapywork.items import articleItem
from scrapy.http import Request
from scrapywork.utils import parse_item
from scrapywork.utils import getarticlerules

class ArticleSpider(CrawlSpider):
    name = 'articleSpider'

    def __init__(self,rule):
        self.rule=rule
        self.start_urls=rule.start_urls.split(',')
        self.allowed_domains=rule.allow_domains.split(',')
        rule_list=[]
        # 添加`下一页`的规则
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths=rule.next_page,unique=True),follow=True))
        #添加 '列表'的规则
        if rule.list_page:
            rule_list.append(Rule(LinkExtractor(allow=rule.list_page,unique=True),callback='parse_url',follow=True))
        #添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=rule.allow_url,unique=True),
            callback='parse_item',follow=True)
        )
        self.rules=tuple(rule_list)
        super(ArticleSpider,self).__init__()


    def parse_url(self,response):
        yield response
        self.log('this is a list page %s'% response.url)
        pages=response.xpath(self.rule.list_page_total).extract_first()
        totalpage=re.findall(r'\d+',pages)
        if not totalpage:totalpage='1'
        self.log('this is a pagetoal %s' % totalpage)
        for i in range(2,int(totalpage[0])+1):
           url=response.url.split('.html')[0]+'_{}.html'.format(i)
           self.log('this ia list page %s' % url)
           yield Request(url)

    def parse_item(self, response):
        self.log('this is article page %s' % response.url)

        articleInfo=articleItem()
        parse_item(self.rule,response,articleInfo)
        yield articleInfo


