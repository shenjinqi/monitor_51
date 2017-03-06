# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy

from scrapy.item import Item, Field

class Monitor51Item(Item):
    # define the fields for your item here like:
    title       = Field()   #职位名称
    link        = Field()   #详情链接
    company     = Field()   #公司名称   
    updatetime  = Field()   #更新时间
    
