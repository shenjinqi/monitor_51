# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
class Monitor51JsonPipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    def process_item(self, item, spider):
        print "========process_item"
        line = json.dumps(dict(item), ensure_ascii = False) + "\n"
        self.file.write(line)
        print line
        return item
    def spider_opened(self, spider):
        print "========spider_opened"
        self.file = codecs.open('./monitor_51.json', 'w+', encoding = 'utf-8')
    def spider_closed(self, spider):
        print "========spider_closed"
        self.file.close() 
