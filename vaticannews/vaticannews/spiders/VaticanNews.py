# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.loader import ItemLoader
from vaticannews.items import VaticannewsItem
import js2xml


class VaticannewsSpider(scrapy.Spider):
    name = 'VaticanNews'
    allowed_domains = ['www.vaticannews.va']
    start_urls = ['https://www.vaticannews.va/bin/servlet/fusion/search?queryroute=vaticannews-search-main&q=papa&fq=lang_s:pt&sort=editorial_date_dt%20desc,id%20asc&rows=18&qId=09144a4b-7979-49e5-8efc-8b08805adf0a']    

    def parse(self, response):
        data = json.loads(response.body)
        for item in data.get('response', [])['docs']:
            if item['preview_type_s'] == 'article[Artigo]':
                url = response.urljoin(item['url_descendent_path'])
                # yield scrapy.Request(url=url, callback=self.parse_detail)

        total_itens = int(data.get('response', [])['numFound'])
        #len(data.get('response', [])['docs'])
        self.log(total_itens)
     
    def parse_detail(self, response):
        loader = ItemLoader(item=VaticannewsItem(), response=response)
        loader.add_value('site', 'vaticannews')
        loader.add_value('subTitle', '')
        loader.add_value('url', response.url)
        loader.add_xpath(
            'title', 'normalize-space(//h1[contains(@class, "article__title")])')
        loader.add_xpath(
            'content', '//div[contains(@class, "article__text")]//p',)
        return loader.load_item()
    
