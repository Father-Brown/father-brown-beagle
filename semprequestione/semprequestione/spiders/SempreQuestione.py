# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from semprequestione.items import SemprequestioneItem


class SemprequestioneSpider(scrapy.Spider):
    name = 'SempreQuestione'
    allowed_domains = ['www.semprequestione.com']
    start_urls = ['http://www.semprequestione.com/']

    def parse(self, response):
        items = response.xpath(
            '//h2[contains(@class,"post-title entry-title")]'
        )
        for item in items:
            url = item.xpath(
                # ".//a[contains(@href, 'carro')]/@href"
                ".//a/@href"
            ).extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)


        next_page = response.xpath(
         #   '//a[contains(@class, "blog-pager-older-link")]/@href'
         '//*[@id="Blog1_blog-pager-older-link"]/@href'
        ).extract()
        next_page=response.urljoin(url)
        print("--------------------------------------------------------------------")
        print(next_page)
        print("--------------------------------------------------------------------")
        
        if next_page:
           self.log('Next Page: {0}'.format(next_page))
           yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        loader = ItemLoader(item=SemprequestioneItem(), response=response)        
        loader.add_value('url', response.url)
        loader.add_xpath('title', 'normalize-space(//h1[contains(@class, "post-title entry-title")])')
        loader.add_xpath('content', '//div[contains(@class, "post-body entry-content")]//div//span',)
        return loader.load_item()