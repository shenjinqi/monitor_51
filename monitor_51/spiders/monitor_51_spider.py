# -*- coding: utf-8 -*-

import logging
import scrapy
import urllib
import codecs

from scrapy.selector import Selector

from monitor_51.items import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

keyword = "FP&A"
#把字符串编码成符合url规范的编码
keywordcode = urllib.quote(keyword)

is_start_page = True
keyword_idx = 0
keyowrds_list = ["FP&A", "python", "C++11", "volte", "LTE"]

class TestfollowSpider(scrapy.Spider):
    global keyword_idx, keyowrds_list
    keywordcode = urllib.quote(keyowrds_list[keyword_idx])
   
    name = "monitor_51"
    allowed_domains = ["51job.com"]
    start_urls = [
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000%2C00&funtype=0000&industrytype=00&keyword=" + keywordcode,
    ]

    def parse(self, response):
        global is_start_page

        url = ""
        #从开始页面开始解析数据，开始页面start_urls
        if is_start_page:
            url = self.start_urls[0]
            is_start_page = False
        else:
            href = response.xpath('//table[@class="searchPageNav"]/tr/td[last()]/a/@href')
            url = response.urljoin(href.extract())

        yield scrapy.Request(url, callback=self.parse_dir_contents)
        

    def parse_dir_contents(self, response):
        global keyword_idx, keyowrds_list
        #print "---------------"
        # print response.xpath('//div[@id="resultList"]')
        for sel in response.xpath('//div[@id="resultList"]/div[@class="el"]'):
            #print "===============" 
            #print sel.xpath('string(.)').extract()[0].replace(' ', '')			
            #print sel.xpath('string(.)').extract()[0].replace(' ', '').strip() # get all info
            link = sel.xpath('.//p/span/a/@href').extract()[0].strip()
            title = sel.xpath('.//p/span/a/text()').extract()[0].strip()
            company = sel.xpath('./span/a/text()').extract()[0].strip() 
            len_more = len(sel.xpath('./span/text()').extract())
            salary = ''
            if len_more == 3:
				location = sel.xpath('./span/text()').extract()[0].strip()
				salary = sel.xpath('./span/text()').extract()[1].strip()
				date = sel.xpath('./span/text()').extract()[2].strip()
            else:
				location = sel.xpath('./span/text()').extract()[0].strip()
				# salary = sel.xpath('./span/text()').extract()[1].strip()
				date = sel.xpath('./span/text()').extract()[1].strip()

            
            item = Monitor51Item()
            item['title'] = title
            item['link'] = link
            item['company'] = company
            item['updatetime'] = date
            item['salary'] = salary
            yield item
            #break

        pre_next_page = response.xpath('//li[@class="bk"]')
        next_page = pre_next_page[1].xpath('.//a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, self.parse_dir_contents)
        else:
            keyword_idx += 1
            if keyword_idx < len(keyowrds_list):
                keywordcode = urllib.quote(keyowrds_list[keyword_idx])
                start_urls_of_next_keyword = [
            "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000%2C00&funtype=0000&industrytype=00&keyword=" + keywordcode,
                ]
                url = start_urls_of_next_keyword[0]
                yield scrapy.Request(url, callback=self.parse_dir_contents)