# -*- coding: utf-8 -*-

import scrapy
from os import path
import json,Queue
import sys,random
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from pdd_spider_v2.items import PddSpiderCategoryItem
from pdd_spider_v2 import mongo_db


class CategoryInfosSpider(scrapy.Spider):
    name = 'category_infos'
    allowed_domains = ['yangkeduo.com']

    def set_crawl_url(self, opt_id, opt_type):
        # api_num:2,3,4
        api_num = random.randint(2, 4)
        self.url = "http://apiv{api_num}.yangkeduo.com/operation/{opt_id}/groups?opt_type={opt_type}&size=1&offset=2&flip=&pdduid=0".format(
            opt_id = opt_id, api_num = api_num, opt_type = opt_type)


    def start_requests(self):
        #first_opt_id_list = [14,1281,4,15,1,1282,743,18,13,1917,818,1543,16,1451,2048,2478]
        first_opt_id_list = [14]
        for first_opt_id in first_opt_id_list:
            self.opt_id = first_opt_id
            self.first_info_dict = {"opt_id":self.opt_id,"cats":[]}
            self.second_info_dict = {"opt_id":"","cats": []}
            self.set_crawl_url(first_opt_id,opt_type=1)
            print "[*] url is {0}".format(self.url)
            yield scrapy.Request(url=self.url, callback=self.parse, dont_filter=True)


    def parse(self, response): # 处理一次一级opt_id的请求,获取二级分类信息
        html_json_data = json.loads(response.body.decode('utf-8'))
        # first_cat_item = PddSpiderCategoryItem()
        # self.first_info_dict['cats'] = [{"opt_id":opt_info['id'],"opt_name":opt_info['name']} for opt_info in html_json_data['opt_infos']] # 二级分类信息列表
        for opt_info in html_json_data['opt_infos']:
            self.second_info_dict = {"opt_id":opt_info['id'],"opt_name":opt_info['name']}
            self.first_info_dict['cats'].append(self.second_info_dict)
            self.set_crawl_url(opt_info['id'],opt_type=2)
            print "[*] url is {0}".format(self.url)
            yield scrapy.Request(url=self.url,callback=self.get_third_cats_info)


    def get_third_cats_info(self, response):  # 处理一次二级opt_id的请求,获取三级分类信息
        html_json_data = json.loads(response.body.decode('utf-8'))
        for opt_info in html_json_data['opt_infos']:
            self.second_info_dict['cats'].append({"opt_id":opt_info['id'],"opt_name":opt_info['name']})
        print self.first_info_dict

