# -*- coding: utf-8 -*-

import scrapy
from scrapy.exceptions import CloseSpider
import json,Queue
import sys,random
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from pdd_spider_v2.items import PddSpiderGoodsItem,PddSpiderOffsetItem
from pdd_spider_v2 import mongo_db

start_offset_num = mongo_db.START_OFFSET_NUM
end_offset_num = mongo_db.END_OFFSET_NUM

class FirstCategorySpider(scrapy.Spider):
    name = 'first_category'
    allowed_domains = ['yangkeduo.com']
    # start_urls = ['http://apiv3.yangkeduo.com/operation/1451/groups?opt_type=1&size=100&offset=1&flip=&pdduid=0']


    def start_requests(self):
        self.reset_opt_id()
        self.offset_num_queue = Queue.Queue()
        self.create_offset_num_queue()
        self.offset_num = self.offset_num_queue.get()
        self.set_crawl_url()
        yield scrapy.Request(url=self.url, callback=self.parse,dont_filter=True)


    def parse(self, response):
        try:
            goods_list_json = json.loads(response.body.decode('utf-8'))
            for each_good in goods_list_json['goods_list']:
                goods_item = PddSpiderGoodsItem()

                goods_item['_id'] = each_good['goods_id']  # 商品id
                goods_item['optID'] = self.opt_id
                goods_item['goods_name'] = each_good['goods_name']  # 商品名称
                goods_item['normal_price'] = each_good['normal_price']
                goods_item['market_price'] = each_good['market_price']
                goods_item['price'] = each_good['group']['price']  # 商品价格
                goods_item['cnt'] = each_good['cnt']  # 已拼件数

                yield goods_item


            offset_item = PddSpiderOffsetItem()
            offset_item['optID'] = self.opt_id
            offset_item['offset_num'] = self.offset_num
            yield offset_item
        except ValueError,e:
            print e

        if self.offset_num_queue.empty():
            print '[***] offset num queue is empty'
            self.create_offset_num_queue()

        self.offset_num = self.offset_num_queue.get()
        self.set_crawl_url()
        yield scrapy.Request(url=self.url, callback=self.parse,dont_filter=True)


    def set_crawl_url(self):
        # api_num:2,3,4
        api_num = random.randint(2,4)
        self.url = "http://apiv{api_num}.yangkeduo.com/operation/{opt_id}/groups?opt_type=1&size=100&offset={offset_num}&flip=&pdduid=0".format(opt_id = self.opt_id,api_num=api_num,offset_num = self.offset_num)


    def create_offset_num_queue(self):
        global start_offset_num, end_offset_num
        for offset_num in range(start_offset_num, end_offset_num):
            offset_num_dict = {"optID": self.opt_id, "offset_num": offset_num}
            if not mongo_db.check_offset_num_exists(offset_num_dict):
                self.offset_num_queue.put(offset_num)
        print "[*] create opt_id : {0} offset_num_queue , len is {1}".format( self.opt_id,self.offset_num_queue.qsize())
        if self.offset_num_queue.empty():
            self.reset_opt_id()
            self.create_offset_num_queue()


    def reset_opt_id(self):
        new_opt_id = mongo_db.get_new_opt_id()
        if new_opt_id is None: # 没有新的opt_id
            print '[***] all opt id is done !!!'
            raise CloseSpider() # 结束
        self.opt_id = new_opt_id
        print '********************************'
        print "[++] new opt_id is {0}".format(new_opt_id)
        print '********************************'
