# -*- coding: utf-8 -*-
import scrapy

from os import path
import json,Queue
import sys,random
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from pdd_spider_v2.items import PddSpiderGoodsItem, PddSpiderOffsetItem
from pdd_spider_v2 import mongo_db


class GoodsSpider(scrapy.Spider):
    name = 'goods'
    allowed_domains = ['yangkeduo.com']

    def set_crawl_url(self, opt_id, opt_type, offset_num):
        # api_num:2,3,4
        api_num = random.randint(2, 4)
        url = "http://apiv{api_num}.yangkeduo.com/operation/{opt_id}/groups?opt_type={opt_type}&size=100&offset={offset_num}&flip=&pdduid=0".format(
            opt_id = opt_id, api_num = api_num, opt_type = opt_type, offset_num=offset_num)
        return url


    def create_crawl_url_list(self, first_opt_id):
        category_infos_dict_list = mongo_db.get_category_infos(first_opt_id)

        third_category_dict_list = [{"first_opt_id": first_opt_id, "second_opt_id": int(category_infos_dict['_id']),"third_opt_id": int(each['opt_id']), "opt_type":3, "offset_num":offset_num} for category_infos_dict in category_infos_dict_list
                                    for each in category_infos_dict['cats']
                                        for offset_num in range(1, 1000, 100)]
        return third_category_dict_list



    def start_requests(self):
        first_opt_id_list = [14, 1281, 4, 15, 1, 1282, 743, 18, 13, 1917, 818, 1543, 16, 1451, 2048, 2478]
        # first_opt_id_list = [1281]
        for first_opt_id in first_opt_id_list: # [::-1]列表反转
            third_category_dict_list = self.create_crawl_url_list(first_opt_id)
            for third_category_dict in third_category_dict_list:
                if not mongo_db.check_offset_num_exists({"third_opt_id": third_category_dict['third_opt_id'], "offset_num": third_category_dict['offset_num']}): # 没爬过该页面
                    url = self.set_crawl_url(third_category_dict['third_opt_id'], third_category_dict['opt_type'], third_category_dict['offset_num'])
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                         meta={"first_opt_id": third_category_dict['first_opt_id'], "second_opt_id": third_category_dict['second_opt_id'], "third_opt_id": third_category_dict['third_opt_id'], "offset_num": third_category_dict['offset_num']})
                else:
                    pass


    def parse(self, response):

        first_opt_id = response.meta["first_opt_id"]
        second_opt_id = response.meta["second_opt_id"]
        third_opt_id = response.meta["third_opt_id"]
        offset_num = response.meta["offset_num"]
        try:
            goods_list_json = json.loads(response.body.decode('utf-8'))
        except Exception,e:
            print e
        else:
            if goods_list_json['goods_list']:
                for each_good in goods_list_json['goods_list']: # 遍历商品信息
                    goods_item = PddSpiderGoodsItem()

                    goods_item['_id'] = each_good['goods_id']  # 商品id
                    goods_item['first_opt_id'] = first_opt_id  # 商品一级分类Id
                    goods_item['second_opt_id'] = second_opt_id # 商品二级分类Id
                    goods_item['third_opt_id'] = third_opt_id # 商品三级分类Id
                    goods_item['goods_name'] = each_good['goods_name']  # 商品名称
                    goods_item['normal_price'] = each_good['normal_price']
                    goods_item['market_price'] = each_good['market_price']
                    goods_item['img_url'] = each_good['hd_url'] # 图片链接
                    goods_item['price'] = each_good['group']['price']  # 商品价格
                    goods_item['cnt'] = each_good['cnt']  # 已拼件数
                    yield goods_item

                offset_item = PddSpiderOffsetItem()
                offset_item['third_opt_id'] = third_opt_id
                offset_item['offset_num'] = offset_num
                yield offset_item
            else:
                pass



if __name__ == '__main__':
    test_spider = GoodsSpider()
    result = test_spider.create_crawl_url_list(1281)
    print len(result)

    for each in result:
        print each