# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from bson.objectid import ObjectId
from actor_scrape.settings import MONGODB_COLLECTION, MONGODB_DB, MONGODB_HOST, MONGODB_PORT


class ActorScrapePipeline(object):
    def __init__(self):
        connection = MongoClient(
            MONGODB_HOST,
            MONGODB_PORT)
        self.db = connection[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        self.collection.insert({"_id": ObjectId().__str__(),
                                "info": item['info'][0],
                               "img_url": item['img_url'][0]})
        return item
