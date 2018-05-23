# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import json
import urllib3

class SemprequestionePipeline(object):
    def __init__(self):
        self.http = urllib3.PoolManager()
        # connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]


    def process_item(self, item, spider):
        # response = self.http.request(
        #     'GET', 
        #     'http://localhost:5000/site/'+settings['BOT_NAME'])
        # print(json.loads(response.data.decode('utf-8')))
        # if not site:
            # site ={"name": settings['BOT_NAME'], "url": "www.semprequestione.com"}
        #     self.http .request(
        #     'POST',
        #     'http://localhost:5000/save/site',
        #     body=json.dumps(site),
        #     headers={'Content-Type': 'application/json'})
        site ={"name": settings['BOT_NAME'], "url": "www.semprequestione.com"}
        print("------------------------------------------------------")
        print()
        print()
        if site:
            print("site ", site)
        print()
        print()
        print("------------------------------------------------------")
        # data ={'site':item['site'], 'url':item['url'], 'title':item['title'], 'subTitle':item['subTitle'],
        #                              'item':item['item'], 'tipo':tipo}
        # response= requests.put("http://localhost:5000/save/news", data=data)
        # print(response)
        # valid = True
        # for data in item:
        #     if not data:
        #         valid = False
        #         raise DropItem("Missing {0}!".format(data))
        # if valid:
        #     self.collection.insert(dict(item))
        #     log.msg("News added to MongoDB database!",
        #             level=log.DEBUG, spider=spider)        
        return item
