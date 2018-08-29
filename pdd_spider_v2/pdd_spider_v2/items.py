# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


'''商品信息'''
class PddSpiderGoodsItem(scrapy.Item):
    _id = scrapy.Field() # 商品id
    first_opt_id = scrapy.Field()  # 商品一级分类Id
    second_opt_id = scrapy.Field()  # 商品二级分类Id
    third_opt_id = scrapy.Field()  # 商品三级分类Id
    goods_name = scrapy.Field()  # 商品名称
    normal_price = scrapy.Field()
    market_price = scrapy.Field()
    img_url =  scrapy.Field() # 图片链接
    price = scrapy.Field()  # 单独购买价格
    cnt = scrapy.Field()  # 已拼件数


'''offset_num记录'''
class PddSpiderOffsetItem(scrapy.Item):
    third_opt_id = scrapy.Field()
    offset_num = scrapy.Field()


'''二级分类信息'''
class PddSpiderSecCategoryItem(scrapy.Item):
    _id = scrapy.Field()
    opt_name = scrapy.Field()
    father_opt_id = scrapy.Field()
    cats = scrapy.Field()