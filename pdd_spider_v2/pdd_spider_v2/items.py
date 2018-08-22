# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PddSpiderGoodsItem(scrapy.Item):
    _id = scrapy.Field() # 商品id
    opt_id = scrapy.Field()  # 商品一级分类Id
    goods_name = scrapy.Field()  # 商品名称
    normal_price = scrapy.Field()
    market_price = scrapy.Field()
    price = scrapy.Field()  # 单独购买价格
    cnt = scrapy.Field()  # 已拼件数



class PddSpiderOffsetItem(scrapy.Item):
    opt_id = scrapy.Field()
    offset_num = scrapy.Field()


'''二级分类信息'''
class PddSpiderSecCategoryItem(scrapy.Item):
    _id = scrapy.Field()
    opt_name = scrapy.Field()
    father_opt_id = scrapy.Field()
    cats = scrapy.Field()