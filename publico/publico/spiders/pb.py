# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from publico.items import PublicoItem
import json

class PbSpider(scrapy.Spider):
    name = 'pb'
    allowed_domains = ['www.publico.pt']
    base_url = 'https://www.publico.pt/api/list/search/?query=papa&start=&end=&page=%d'
    index = 1
    start_urls = [base_url % index]
    

    def parse(self, response):
        json_data = json.loads(response.text)
        for data in json_data:
            url = data['url']                 
            if url: 
                yield scrapy.Request(url=url, callback=self.parse_detail, dont_filter=True)
        if json_data:
            self.index += 1
            next_page = self.base_url % self.index
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)
        
        

    def parse_detail(self, response):
        loader = ItemLoader(item=PublicoItem(), response=response)
        loader.add_value('site', 'publico')
        loader.add_xpath('subTitle', 'normalize-space(//div[contains(@class, "story__blurb lead")]//p)')
        loader.add_value('url', response.url)
        loader.add_xpath('title', 'normalize-space(//h1[contains(@class, "headline story__headline")])')
        loader.add_xpath('content', '//div[contains(@class, "story__body")]//p',)
        loader.add_xpath('autor', 'normalize-space(//span[contains(@class, "byline__name")]/text())')
        loader.add_xpath('datePublished', 'normalize-space(//time[contains(@class, "dateline")]/@datetime)')
        return loader.load_item()
        
