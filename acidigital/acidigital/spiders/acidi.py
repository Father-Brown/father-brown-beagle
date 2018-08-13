# -*- coding: utf-8 -*-
import scrapy


class AcidiSpider(scrapy.Spider):
    name = 'acidi'
    allowed_domains = ['acidigital.com']
    start_urls = ['https://www.acidigital.com/noticias_tags.php?tag_id=2996&page=1']

    def parse(self, response):

        items = response.xpath(
            '//div[contains(@class, "noticia_list_body")]//h3'
        )

        for item in items:
            url = item.xpath(
                './/a/@href'
            ).extract_first()
            self.log(url)
            url = response.urljoin(url)   
            if url: 
                 yield scrapy.Request(url=url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):

        data = response.xpath(
                '//div[contains(@class, "noticia-contenido")]//p//text()'
            )
        for s in data:
            self.log(
                s
            )
        
         # loader = ItemLoader(item=RevistaforumItem(), response=response)
        # loader.add_value('site', 'revistaforum')
        # loader.add_value('subTitle', '')
        # loader.add_value('url', response.url)
        # loader.add_xpath('title', '//h1')
        # loader.add_xpath('content', 'normalize-space(//div[contains(@id, "content")]//div//p)')
        # loader.add_value('autor', autor)
        # loader.add_value('datePublished', data)
        # return loader.load_item()
