# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.loader import ItemLoader
from acidigital.items import AcidigitalItem
import re

class AcidiSpider(scrapy.Spider):
    name = 'acidi'
    allowed_domains = ['acidigital.com']
    start_urls = ['https://www.acidigital.com/noticias.php?cat_id=1']
    data = ''

    def parse(self, response):

        # items = response.xpath(
        #     '//div[contains(@class, "noticia_list_body")]//h3'
        # )
        # self.data=response.xpath(
        #     '//span[contains(@class, "noticia_list_fecha")]/text()'
        # ).extract_first()
        

        # for item in items:
        #     url = item.xpath(
        #         './/a/@href'
        #     ).extract_first()            
        #     url = response.urljoin(url)   
        #     if url: 
        #          yield scrapy.Request(url=url, callback=self.parse_detail, dont_filter=True)

        next_page = response.xpath(         
         "//div[contains(@class, 'pagination')]/a/@href"
        ).extract_first()
        next_page=response.urljoin(next_page)
        if next_page:
        #    self.log('Next Page: {0}'.format(next_page))
           yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):

        autor = response.xpath(
                '//div[contains(@class, "bajada")]/text()'
            ).extract()
        
        if len(autor) == 0:
            autor.append(settings['BOT_NAME'])
        else:
            autor[0] = autor[0].replace('Por ', '')
      
        
        loader = ItemLoader(item=AcidigitalItem(), response=response)
        loader.add_value('site', settings['BOT_NAME'])
        loader.add_value('subTitle', '')
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1')
        loader.add_xpath('content', '//div[contains(@class, "noticia-contenido")]//p/text()')
        loader.add_value('autor', autor)
        loader.add_value('datePublished', self.data)
        return loader.load_item()
