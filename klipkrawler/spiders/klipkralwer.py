# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
import newspaper

class KlipkralwerSpider(scrapy.Spider):
    name = "klipkralwer"
    start_urls = (
        'http://thaisagalvao.com.br',
        'http://portalmercadoaberto.com.br',
        'http://g1.globo.com/rn/rio-grande-do-norte/index.html',
        'http://aluiziodecarnaubais.blogspot.com.br',
        'http://visorpolitico.com.br',
        'http://caiooliveira.com',
        'http://novojornal.jor.br',
        'http://robsoncarvalho.com',
        'http://tribunadonorte.com.br'
    )

   # self.hcf_settings = {'HS_ENDPOINT': 'http://storage.scrapinghub.com/',
   #                      'HS_AUTH': 'c4009b5382834967aedec18952411ffc',
   #                      'HS_PROJECTID': '12516',
   #                      'HS_FRONTIER': 'test',
   #                      'HS_CONSUME_FROM_SLOT': '0',
   #                      'HS_NUMBER_OF_SLOTS': 1}

    def parse(self, response):
        article = newspaper.build(response.url, language='pt')
        article.download()
        article.parse()
        print(article.title)

