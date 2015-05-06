# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import newspaper
from newspaper import Article
import pdb

class SpiderphantSpider(CrawlSpider):
    name = "spiderphant"
    allowed_domains = ['www.tribunadonorte.com.br', 'blog.tribunadonorte.com.br']
    start_urls = [
        'http://www.tribunadonorte.com.br'
    ]

    rules = [
        Rule(LinkExtractor(
            allow=['/noticia/'],
            deny=['/video/']),
            callback='parse_tribuna'
        )
    ]
    
   # def parse(self, response):
   #     main = newspaper.build(response.url, memoize_articles=False)
   #     for article in main.articles:
   #         current = Article(article.url)
   #         current.download()
   #         current.parse()
   #         pdb.set_trace()

    def parse_tribuna(self, response):
        print(response.url)
        pdb.set_trace()
