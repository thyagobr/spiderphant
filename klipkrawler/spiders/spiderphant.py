# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from klipkrawler.items import KlipkrawlerItem
from datetime import datetime
from urlparse import urlparse
import newspaper
from newspaper import Article
import json
import pdb

class SpiderphantSpider(CrawlSpider):
    name = "spiderphant"
    allowed_domains = ['www.tribunadonorte.com.br',
                       'blog.tribunadonorte.com.br', 
                       'www.thaisagalvao.com.br',
                       'nominuto.com/noticias',
                       'robsoncarvalho.com',
                       'www.aluiziodecarnaubais.blogspot.com.br',
                       'www.assessorn.com',
                       'www.caiooliveira.com',
                       'www.nahorah.net',
                       'www.portalmercadoaberto.com.br',
                       'www.rodrigoloureiro.com.br'
                    ]

    start_urls = [
        'http://www.tribunadonorte.com.br',
       # 'http://www.thaisagalvao.com.br',
       # 'http://nominuto.com/noticias',
       # 'http://robsoncarvalho.com',
       # 'http://www.aluiziodecarnaubais.blogspot.com.br',
       # 'http://www.assessorn.com',
       # 'http://www.caiooliveira.com',
       # 'http://www.nahorah.net',
       # 'http://www.portalmercadoaberto.com.br',
       # 'http://www.rodrigoloureiro.com.br'
    ]

    rules = [
        Rule(LinkExtractor(allow=['noticia', '/novo/coluna/', r'/\d{4}\/\d{2}\/'],
                            deny=['cadastro.tribunadonorte.com.br']),
                            callback='parse_news')
    ]

    def scrape_published_date(self, response, published_date):
        pubdate = []
        if isinstance(published_date, datetime):
            published_date = published_date.strftime("%d/%m/%Y")
        if "tribunadonorte.com.br" in response.url:
            pubdate = response.css('section[id=r-main] section[id=content] header small').extract()
            # Some witchery here. Crazy, I know, but, necessary.
            # This is how we get pubdate up here:
            # "<small>Publicação: 2015-05-08 10:49:00 | Comentários: 0</small>"
            # So we gotta hack and slash that to get our datetime
            if len(pubdate) > 0:
                pubdate = pubdate[0].split(" | ")[0].split(": ")[1].strip().replace("-", "/")
            else:
                pubdate = None
        elif "robsoncarvalho.com" in response.url:
            pubdate = response.css("time::attr(datetime)").extract()[0]
        return pubdate if pubdate else published_date

    def scrape_images(self, response, image_list):
        images = []
        if "tribunadonorte.com.br" in response.url:
            image_list = filter(lambda image:'arquivos' in image, image_list) 
        for image_url in image_list:
            image_info = {}
            image_info['url'] = image_url
            image_info['alt'] = ''
            images.append(image_info)
        return images

    def scrape_text(self, response, text):
        scraped_text = None
        if "tribunadonorte" in response.url:
            split_text = text.split("\n")
            split_size = len(split_text)
            scraped_text = split_text[split_size - 1] if split_size > 0 else text
        return scraped_text if scraped_text else text

    def parse_news(self, response):
        article = Article(response.url)
        article.download()
        article.parse()
        item = KlipkrawlerItem()
        item['title'] = article.title.encode('utf-8')
        item['text'] = self.scrape_text(response, article.text)
        item['url'] = response.url
        item['published_date'] = self.scrape_published_date(response, article.publish_date)
        item['scraped_date'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        item['images'] = self.scrape_images(response, article.images)
        item['videos'] = article.movies
        item['source'] = urlparse(response.url).hostname
        item['language'] = article.meta_lang
        pdb.set_trace()
        yield item
        #with open('output.txt', 'a') as f:
        #    for key, value in item.iteritems():
        #        value = ''.join(value) if isinstance(value, list) else value
        #        if value == None:
        #            value = ""
        #        line = key + ' = ' + value
        #        f.write(line + '\n')

