# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose

class ScrapyworkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class articleItem(scrapy.Item):
    #文章的链接
    url = scrapy.Field()
    #站点
    site=scrapy.Field()
    #文章标题
    title=scrapy.Field()
    #文章发布时间
    time=scrapy.Field()
    #文章类型
    type=scrapy.Field()
    #文章发布方
    publish=scrapy.Field()
    html =scrapy.Field()
    text=scrapy.Field()
    xml=scrapy.Field()

    #文件下载
    file_urls=scrapy.Field()
    files=scrapy.Field()
    #图片下载
    image_urls=scrapy.Field()
    images=scrapy.Field()



