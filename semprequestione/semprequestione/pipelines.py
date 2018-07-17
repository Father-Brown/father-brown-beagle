# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import json
import urllib3

class SemprequestionePipeline(object):
    def __init__(self):
        self.http = urllib3.PoolManager()

    def process_item(self, item, spider):
        response = self.getSite()

        if response.status == 404:
            site ={"name": settings['BOT_NAME'], "url": "www.semprequestione.com"}
            self.post('http://localhost:5000/save/site', json.dumps(site))

        data = {
            "site":item['site'],
            "url":item['url'],
            "title":item['title'],
            "subTitle":item['subTitle'],
            "content":item['content'],
            "autor":item['autor'],
            "datePublished":item['datePublished'],
            "tipo":'None'
            }

        data = json.dumps(data)
        response = self.post("http://localhost:5000/save/news", data)
        return item

    def getSite(self):
        response = self.http.request(
            'GET',
            'http://localhost:5000/site/'+settings['BOT_NAME'])
        return response;

    def post(self, url, data):
        return self.http.request('POST',url,
            body=data,
            headers={'Content-Type': 'application/json'})
