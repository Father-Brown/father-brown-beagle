# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from publico.items import PublicoItem

class PbSpider(scrapy.Spider):
    name = 'pb'
    allowed_domains = ['www.publico.pt']
    start_urls = ['https://www.publico.pt/pesquisa?query=papa']

    def parse(self, response):

        items = response.xpath(
           '//div[contains(@class, "media-object-section")]'
        )        
        for item in items:
            titulo = item.xpath(                
                ".//h4[contains(text(), 'papa') or contains(text(), 'Papa') or contains(text(), 'vaticano') or contains(text(), 'Vaticano')]"                
            ).extract_first()
            url = item.xpath(##[contains(text(), 'papa') or contains(text(), 'vaticano')]
                ".//a/@href"                
            ).extract_first()
            if url and titulo:                
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
           '//a[contains(@class, "module__button module__button--more append-content")]/@href'         
        ).extract_first()
        next_page=response.urljoin(next_page)
        self.log(next_page)
        
        # if next_page:
        # #    self.log('Next Page: {0}'.format(next_page))
        #    yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        loader = ItemLoader(item=PublicoItem(), response=response)
        loader.add_value('site', 'publico')
        loader.add_value('subTitle', '')
        loader.add_value('url', response.url)
        loader.add_xpath('title', 'normalize-space(//h1[contains(@class, "headline story__headline")])')
        loader.add_xpath('content', '//div[contains(@class, "story__body")]//p',)
        return loader.load_item()
        
