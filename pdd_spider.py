# -*- coding:utf-8 -*-

# @Time    : 2018/8/1 8:10 PM
# @Author  : jerry

import os
import re
import time
import json
import random
import jsonpath
import requests
import linecache
from lxml import etree

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import config

class PddSpider():
    def __init__(self):
        self.start_url = "https://mobile.yangkeduo.com/index.html" # 起始url


    # 开始爬取
    def startCrawl(self):
        self.change_useragent()
        self.get_json_data()
        self.get_category_info_dicts()


    # 获取一级分类名列表
    def get_first_category_name(self):
        res = requests.get(self.start_url, headers=self.headers)
        self.resp_code = res.status_code
        self.first_category_name_list = []
        if self.resp_code == 200:
            self.index_html_data = etree.HTML(res.content)

            for index_num in range(1,18): # range(2,18),就可以不要一级分类:热门
                all_li_data = self.index_html_data.xpath('''//*[@id="navbar-ul"]/li[{0}]/span/text()'''.format(
                    index_num))
                # print index_num,'.',all_li_data[0].encode('utf-8')
                self.first_category_name_list.append(all_li_data[0])
        print len(self.first_category_name_list)


    # 获取分类信息
    def get_category_info_dicts(self):
        category_info_list = self.json_data['props']['data']['data']['portalCommon']['operations']
        # print len(category_info_list) 17个分类
        category_info_dicts = {'first_category':[]}
        for first_category_info in category_info_list:
            first_category_dict = {}
            first_category_dict['tabname'] = first_category_info['tabName']

            category_info_dicts['first_category'].append(first_category_dict)
            # if first_category_info.has_key('cat'): # 含有二级分类列表
        print category_info_dicts
        print len( category_info_dicts['first_category'])


    # 获取含有分类信息的json数据
    def get_json_data(self):
        res = requests.get(self.start_url, headers=self.headers)
        self.resp_code = res.status_code
        self.first_category_name_list = []
        if self.resp_code == 200:
            self.index_html_data = etree.HTML(res.content)
            js_data = self.index_html_data.xpath("/html/body/script[1]/text()")
            pattern = "_NEXT_DATA__ = ({.*?})\n                        module={}"
            # json_data = js_data[0][25:-6]
            json_data1 = re.findall(pattern,js_data[0],re.S)[0]
            self.json_data = json.loads(json_data1)


    def get_second_category_name(self):
        pass


    # 随机更改user_agent
    def change_useragent(self):
        tunnel = random.randint(1, 1036)
        user_agent = linecache.getline('1000ua-pc.log', tunnel)
        user_agent = user_agent.strip().replace('\n', '').replace('\r', '')
        # 请求头携带Host会导致无法访问数据
        self.headers = {
            "Connection": "keep-alive",
            "Cookie": "goods=goods_abY0pR; api_uid=rBQh3Vqd/BEEgl0IBpdgAg==; ua=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F63.0.3239.132%20Safari%2F537.36; webp=1; msec=86400000; rec_list=rec_list_OW96ZF",
            # "Upgrade-Insecure-Requests": "1",
            # 'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'user-agent': user_agent,
        }
        print(self.headers)




if __name__ == '__main__':
    pdd_spider = PddSpider()
    pdd_spider.startCrawl()
