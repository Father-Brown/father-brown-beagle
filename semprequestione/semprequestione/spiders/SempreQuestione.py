# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from semprequestione.items import SemprequestioneItem


class SemprequestioneSpider(scrapy.Spider):
    name = 'SempreQuestione'
    allowed_domains = ['www.semprequestione.com']
    start_urls = ['http://www.semprequestione.com/']

    def parse(self, response):
        match = "contains(text(), 'papa') or contains(text(), 'Papa') or contains(text(), 'vaticano') or contains(text(), 'Vaticano')"
        items = response.xpath(
            '//h2[contains(@class,"post-title entry-title")]'
        )
        for item in items:
            url = item.xpath(
                ".//a["+match+"]/@href"                
            ).extract_first()
            if url:
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
         #   '//a[contains(@class, "blog-pager-older-link")]/@href'
         'normalize-space(//*[@id="Blog1_blog-pager-older-link"]/@href)'
        ).extract_first()
        next_page=response.urljoin(next_page)
        
        
        if next_page:
        #    self.log('Next Page: {0}'.format(next_page))
           yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        loader = ItemLoader(item=SemprequestioneItem(), response=response)
        loader.add_value('site', 'semprequestione')
        loader.add_value('subTitle', '')
        loader.add_value('url', response.url)
        loader.add_xpath('title', 'normalize-space(//h1[contains(@class, "post-title entry-title")])')
        loader.add_xpath('content', '//div[contains(@class, "post-body entry-content")]//div//span',)
        loader.add_xpath('autor', 'normalize-space(//span[contains(@itemprop, "name")])')
        return loader.load_item()