# -*- coding:utf-8 -*-

# @Time    : 2018/8/1 8:10 PM
# @Author  : jerry

import os,re,time,random
import json,jsonpath
import requests
import linecache
from lxml import etree

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import config
from mongo_db import insertCategory

class PddSpider():
    def __init__(self):
        self.start_url = "https://mobile.yangkeduo.com/index.html" # 起始url



    # 开始爬取
    def startCrawl(self):
        self.change_useragent()
        self.get_json_data()
        self.get_first_category_dicts()
        self.get_second_category_dicts()
        #self.insert_category_infos()


    # 获取一级分类名列表
    def get_first_category_name(self):
        res = requests.get(self.start_url, headers=self.headers)
        self.first_category_name_list = []
        if res.status_code == 200:
            self.index_html_data = etree.HTML(res.content)

            for index_num in range(1,18): # range(2,18),就可以不要一级分类:热门
                all_li_data = self.index_html_data.xpath('''//*[@id="navbar-ul"]/li[{0}]/span/text()'''.format(index_num))
                # print index_num,'.',all_li_data[0].encode('utf-8')
                self.first_category_name_list.append(all_li_data[0])
        print len(self.first_category_name_list)


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


    # 获取分类信息
    def get_first_category_dicts(self):
        category_json_info = self.json_data['props']['data']['data']['portalCommon']['operations']
        # print len(category_info_list) 17个分类
        self.category_info_list = []
        for first_category in category_json_info:
            first_category_dict = {}
            first_category_dict['tabName'] = first_category['tabName']
            first_category_dict['optID'] = first_category['optID']
            self.category_info_list.append(first_category_dict)
            '''
            # 此处获取的二级分类不够全，均只有9个二级分类
            if first_category.has_key('cat'): # 含有二级分类列表
                first_category_dict['cat'] = []
                
                for each in first_category['cat']:
                    second_category_dict = {}
                    second_category_dict['optName'] = each['optName']
                    second_category_dict['optID'] = each['optID']
                    first_category_dict['cat'].append(second_category_dict)
            '''
        print self.category_info_list


    # 获取二级分类标签名
    def get_second_category_dicts(self):
        second_category_url = "https://mobile.yangkeduo.com/catgoods.html?opt_id={opt_id}" \
                              "&opt_name={opt_name}&opt_type=1&refer_page_name=index&refer_page_id=10002_15331"
        for each in self.category_info_list:
            url = second_category_url.format(opt_id= each['optID'],opt_name= each['tabName'])
            print(url)
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                print res.content
                second_html_data = etree.HTML(res.content)
                all_li_data = second_html_data.xpath('''//*[@id="catname-slide-up"]/div[2]//span/text()''')
                print(all_li_data)
                print type(all_li_data)
                print len(all_li_data)
                time.sleep(1)
            break



    # 入库分类信息
    def insert_category_infos(self):
        for category_info in self.category_info_list:
            insertCategory(category_info)


    def update_category_infos(self):
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
        # print(self.headers)




if __name__ == '__main__':
    pdd_spider = PddSpider()
    pdd_spider.startCrawl()
