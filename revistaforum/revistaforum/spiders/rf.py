# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from revistaforum.items import RevistaforumItem
import re

class RfSpider(scrapy.Spider):
    name = 'rf'
    allowed_domains = ['www.revistaforum.com.br']
    start_urls = ['http://www.revistaforum.com.br/?s=papa']

    def parse(self, response):
        match = "contains(text(), 'papa') or contains(text(), 'Papa') or contains(text(), 'vaticano') or contains(text(), 'Vaticano')"
        items = response.xpath(
            '//div[contains(@class,"media")]'
        )
        for item in items:
            url = item.xpath(
                ".//a["+match+"]/@href"                
            ).extract_first()
            if url:
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(         
         "//a[contains(@aria-label, 'Next')]/@href"
        ).extract_first()
        next_page=response.urljoin(next_page)
        
        if next_page:
           self.log('Next Page: {0}'.format(next_page))
           yield scrapy.Request(url=next_page, callback=self.parse)
    def parse_detail(self, response):
        autor = response.xpath(
            'normalize-space(//div[contains(@class, "author")]//div//a/text())'
        ).extract_first()
        autor = re.sub('Por', '', autor)
        
        data = response.xpath(
            'normalize-space(//span[contains(@class, "date")]/text())'
        ).extract_first()
        
        
        loader = ItemLoader(item=RevistaforumItem(), response=response)
        loader.add_value('site', 'revistaforum')
        loader.add_value('subTitle', '')
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1')
        loader.add_xpath('content', 'normalize-space(//div[contains(@class, "text")]//p/text())')
        loader.add_value('autor', autor)
        loader.add_value('datePublished', data)
        return loader.load_item()
                
