# -*- coding: utf-8 -*-
from __future__ import print_function
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from klipkrawler.items import KlipkrawlerItem
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
            allow=['/noticia/']),
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

    def scrape_published_date(self, source, response):
        if source == "tribunadonorte":
            pubdate = response.css('section[id=r-main] section[id=content] header small').extract()
            return pubdate[0] if pubdate else None

    def scrape_images(self, source, image_list):
        if source == "tribunadonorte":
            return filter(lambda image:'arquivos' in image, image_list) 

    def parse_tribuna(self, response):
        article = Article(response.url)
        article.download()
        article.parse()
        item = KlipkrawlerItem()
        item['title'] = article.title.encode('utf-8')
        item['text'] = article.text
        item['url'] = response.url
        item['published_date'] = self.scrape_published_date("tribunadonorte", response)
        item['images'] = self.scrape_images("tribunadonorte", article.images)
        item['videos'] = article.movies
        with open('output.txt', 'w') as f:
            for key, value in item.iteritems():
                print("%s = %s" % (key, value), file=f)

