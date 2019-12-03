# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider,CrawlSpider,XMLFeedSpider,CSVFeedSpider,SitemapSpider


class AmazonSpider(scrapy.Spider):  # 自定义类，继承Spiders提供的基类
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['http://www.amazon.cn/']

    custom_settings = {
        'BOT_NAME': 'Egon_Spider_Amazon',
        'REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        }
    }

    def parse(self, response):
        pass


class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        return [scrapy.FormRequest("http://www.example.com/login",
                                   formdata={'user': 'john', 'pass': 'secret'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass