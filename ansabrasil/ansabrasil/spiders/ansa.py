# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ansabrasil.items import AnsabrasilItem


class AnsaSpider(scrapy.Spider):
    name = 'ansa'
    allowed_domains = ['ansabrasil.com.br']
    start_urls = ['http://ansabrasil.com.br/brasil/noticias/vaticano/noticias/vaticano.shtml']

    def parse(self, response):
        items = response.xpath(
            '//div[contains(@class,"news-content")]'
        )
        for item in items:            
            url = item.xpath(
                ".//h2//a/@href"                
            ).extract_first()            
            if url:
                url = response.urljoin(url)                
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
           '//li[contains(@class, "next")]//a/@href'       
        ).extract_first()        
        next_page=response.urljoin(next_page)        
        if next_page:
        #    self.log('Next Page: {0}'.format(next_page))
           yield scrapy.Request(url=next_page, callback=self.parse)
    
    def parse_detail(self, response):      
        loader = ItemLoader(item=AnsabrasilItem(), response=response)
        loader.add_value('site', 'ansabrasil')
        loader.add_xpath('subTitle', 'normalize-space(.//h2)')
        loader.add_value('url', response.url)
        loader.add_xpath('title', 'normalize-space(.//h1)')
        loader.add_xpath('content', '//div[contains(@class, "news-txt")]//p',)
        return loader.load_item()