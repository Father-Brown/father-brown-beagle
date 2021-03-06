# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from diariodocentrodomundo.items import DiariodocentrodomundoItem

class DcSpider(scrapy.Spider):
    name = 'dcm'
    allowed_domains = ['www.diariodocentrodomundo.com.br']
    start_urls = ['https://www.diariodocentrodomundo.com.br/?s=papa']

    def parse(self, response):
        match = "contains(text(), 'papa') or contains(text(), 'Papa') or contains(text(), 'vaticano') or contains(text(), 'Vaticano')"
        items = response.xpath(
            '//h3[contains(@class,"entry-title td-module-title")]'
        )
        for item in items:            
            url = item.xpath(
                ".//a["+match+"]/@href"
            ).extract_first()            
            if url:
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(         
         "//a[./i[contains(@class, 'td-icon-menu-right')]]/@href"
        ).extract_first()
        next_page=response.urljoin(next_page)
        if next_page:
           self.log('Next Page: {0}'.format(next_page))
           yield scrapy.Request(url=next_page, callback=self.parse)
    def parse_detail(self, response):        
        loader = ItemLoader(item=DiariodocentrodomundoItem(), response=response)
        loader.add_value('site', 'diariodocentrodomundo')
        loader.add_value('subTitle', '')
        loader.add_value('url', response.url)
        loader.add_xpath('title', 'normalize-space(//h1[contains(@class, "entry-title")])')
        loader.add_xpath('content', 'normalize-space(//div[contains(@class, "td-post-content td-pb-padding-side")]//p)',)
        loader.add_xpath('autor', 'normalize-space(//div[contains(@class, "td-post-author-name")]/a/text())')
        loader.add_xpath('datePublished', 'normalize-space(//time[contains(@class, "entry-date updated td-module-date")]/@datetime)')
        return loader.load_item()
