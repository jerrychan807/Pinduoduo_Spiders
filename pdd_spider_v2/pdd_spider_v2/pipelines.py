# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from pdd_spider_v2.items import PddSpiderGoodsItem,PddSpiderOffsetItem,PddSpiderSecCategoryItem
from pdd_spider_v2 import mongo_db

class PddSpiderV2Pipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PddSpiderGoodsItem):
            # print 'yes'
            mongo_db.insert_goods_dict(dict(item))
            #self.client.insert(dict(item))

        if isinstance(item,PddSpiderOffsetItem):
            mongo_db.insert_offset_num_dict(dict(item))

        if isinstance(item,PddSpiderSecCategoryItem):
            print '--------------'
            mongo_db.insertCategory(dict(item))
            print '--------------'
        return item