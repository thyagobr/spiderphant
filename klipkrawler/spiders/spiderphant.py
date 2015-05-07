# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from klipkrawler.items import KlipkrawlerItem
import newspaper
from newspaper import Article
import pdb

class SpiderphantSpider(CrawlSpider):
    name = "spiderphant"
    allowed_domains = ['www.tribunadonorte.com.br',
                       'blog.tribunadonorte.com.br', 
                       'www.thaisagalvao.com.br']
    start_urls = [
        'http://www.tribunadonorte.com.br',
        'http://www.thaisagalvao.com.br'
    ]

    rules = [
        Rule(LinkExtractor(allow=['/noticia/', r'/\d{4}\/\d{2}\/\d{2}/']), callback='parse_tribuna'),
   #     Rule(LinkExtractor(deny=['cadastro.tribunadonorte.com.br']))
    ]

    def scrape_published_date(self, response, published_date):
        if "tribunadonorte.com.br" in response.url:
            pubdate = response.css('section[id=r-main] section[id=content] header small').extract()
            return pubdate[0] if pubdate else None
        else:
            return published_date.strftime('%d/%m/%Y')

    def scrape_images(self, response, image_list):
        if "tribunadonorte.com.br" in response.url:
            return filter(lambda image:'arquivos' in image, image_list) 
        else:
            return image_list

    def parse_tribuna(self, response):
        #if response.url == "http://cadastro.tribunadonorte.com.br/leitor/entrar":
        #    return None
        article = Article(response.url)
        article.download()
        article.parse()
        item = KlipkrawlerItem()
        item['title'] = article.title.encode('utf-8')
        item['text'] = article.text.strip()
        item['url'] = response.url
        item['published_date'] = self.scrape_published_date(response, article.publish_date)
        item['images'] = self.scrape_images(response, article.images)
        item['videos'] = article.movies
        with open('output.txt', 'a') as f:
            for key, value in item.iteritems():
                value = ''.join(value) if isinstance(value, list) else value
                if value == None:
                    value = ""
                line = key + ' = ' + value
                #print('%s = %s' % (key, value), file=f)
                f.write(line + '\n')

