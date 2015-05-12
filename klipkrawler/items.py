# -*- coding: utf-8 -*-

import scrapy

class KlipkrawlerItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    scraped_date = scrapy.Field()
    published_date = scrapy.Field()
    images = scrapy.Field()
    videos = scrapy.Field()
    source = scrapy.Field()
    language = scrapy.Field()
