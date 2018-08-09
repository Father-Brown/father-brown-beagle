# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

class PublicoItem(scrapy.Item):
    site = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    url = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    subTitle = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )    
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    abstract = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    content = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    autor = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    datePublished = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
