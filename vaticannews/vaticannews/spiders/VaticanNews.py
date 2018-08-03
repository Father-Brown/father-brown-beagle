# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.loader import ItemLoader
from vaticannews.items import VaticannewsItem
import js2xml
from math import ceil
import re


class VaticannewsSpider(scrapy.Spider):
    name = 'VaticanNews'
    allowed_domains = ['www.vaticannews.va']
    start = 0
    base_url ="https://www.vaticannews.va/bin/servlet/fusion/search?queryroute=vaticannews-search-main&q=papa&fq=lang_s:pt&sort=editorial_date_dt%%20desc,id%%20asc&rows=18&start=%d&qId=09144a4b-7979-49e5-8efc-8b08805adf0a"
    start_urls = [base_url % start]
    

    def parse(self, response):
        data = json.loads(response.body)
        for item in data.get('response', [])['docs']:
            if item['preview_type_s'] == 'article[Artigo]':
                url = response.urljoin(item['url_descendent_path'])
                yield scrapy.Request(url=url, callback=self.parse_detail)

        total_itens = int(data.get('response', [])['numFound'])
        total_noticias = len(data.get('response', [])['docs'])
        paginas = ceil(total_itens/total_noticias)
        for page in range(1,paginas):
            next_page = self.base_url % (page*total_noticias)
            # self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)
     
    def parse_detail(self, response):
        self.log("")
        self.log("")

        autor = response.xpath(
            '//div[contains(@class, "article__text")]//p//b/text()'
        ).extract_first()
        autor = re.sub("[–|-][A-Za-z ]*", "", autor)

        
        loader = ItemLoader(item=VaticannewsItem(), response=response)
        loader.add_value('site', 'vaticannews')
        loader.add_value('subTitle', '')
        loader.add_value('url', response.url)
        loader.add_value('autor', autor)
        loader.add_xpath('datePublished', '//div[contains(@class, "article__extra")]//span/text()')        
        loader.add_xpath(
            'title', 'normalize-space(//h1[contains(@class, "article__title")])')
        loader.add_xpath(
            'content', '//div[contains(@class, "article__text")]//p',)
            
        return loader.load_item()
    
