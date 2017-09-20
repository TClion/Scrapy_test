# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class DoubanBookPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]


    def process_item(self, item, spider):
        postItem = dict(item)
        if self.coll.find_one({'link':postItem['link']}) == None:
            self.coll.insert(postItem)
        # print postItem
        return item
