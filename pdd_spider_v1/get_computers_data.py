# -*- coding:utf-8 -*-

# @Time    : 2018/8/2 10:58 PM
# @Author  : jerry



import os,re,time,random
import json,jsonpath
import requests
import linecache
from lxml import etree

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 电脑的opt_id为2478

from mongo_db import insertComputersGoods
from proxy import get_proxy_queue

import Queue


start_offset_num = 0
end_offset_num = 1000

class ComputersGoodsSpider():
    def __init__(self):
        self.second_category_url = "http://apiv2.yangkeduo.com/operation/2478/groups?opt_type=1&size=100&offset={0}&flip=&pdduid=0"
        #"http://apiv3.yangkeduo.com/operation/2478/groups?opt_type=1&size=100&offset={0}&flip=&pdduid=0"
        self.offset_num_queue = Queue.Queue()
        self.proxy_ip_queue = Queue.Queue() # 代理ip队列


    def get_proxy_ip_queue(self):
        self.proxy_ip_queue = get_proxy_queue()


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

    def get_html(self,offset_num, proxy_ip):
        # self.change_useragent()
        proxies = {
            "http": "http://{0}".format(proxy_ip)
        }
        url = self.second_category_url.format(offset_num)
        print "[*] requesting url : {0}".format(url)
        try:
            response = requests.get(url, headers=self.headers,proxies=proxies,timeout=5)
        except requests.exceptions.ConnectTimeout,e:
            print e
        except requests.exceptions.ReadTimeout,e:
            print e
        except requests.exceptions.ProxyError,e:
            print e
        except requests.exceptions.ConnectionError,e:
            print e
        else:
            if response.status_code == 200:
                html_data = response.content
                return html_data
            else: # 尝试过几秒重连
                pass
        return None

    def create_offset_num_queue(self):
        global start_offset_num, end_offset_num

        for offset_num in range(start_offset_num, end_offset_num):
            self.offset_num_queue.put(offset_num)

    def random_sleep(self):
        for i in range(1, 11):
            time.sleep(0.5)
            # print '请求失败，第%s次重复请求' % i
            if i == 5:
                print "[*] sleeping 3s..."
                time.sleep(3)
            elif i == 7:
                print "[*] sleeping 5s..."
                time.sleep(5)
            elif i == 9:
                print "[*] sleeping 2s..."
                time.sleep(2)
            else:
                time.sleep(3)
                print "[*] sleeping 3s..."
            break


    def get_goods_data(self):
        while not self.offset_num_queue.empty():
            #self.random_sleep()
            self.change_useragent()
            if self.proxy_ip_queue.empty():
                self.get_proxy_ip_queue()
            proxy_ip = self.proxy_ip_queue.get()


            offset_num =  self.offset_num_queue.get()
            print "[*] using offset_num : {0}".format(offset_num)
            html_data = self.get_html(offset_num,proxy_ip) # 获取json数据
            if html_data:
                jsonobj = json.loads(html_data.decode('utf-8'))

                for each_good in jsonobj['goods_list']:
                    good_dict = {}
                    good_dict['_id'] = each_good['goods_id']  # 商品id
                    good_dict['goods_name'] = each_good['goods_name']  # 商品名称
                    good_dict['normal_price'] = each_good['normal_price']
                    good_dict['market_price'] = each_good['market_price']
                    good_dict['price'] = each_good['group']['price'] # 商品价格
                    good_dict['cnt'] = each_good['cnt']  # 已拼件数

                    insertComputersGoods(good_dict)
                print "[+] successfully get html_data , handle offset_num : {0}".format(offset_num)
            else:
                print "[-] failed handle offset_num : {0}".format(offset_num)
                self.offset_num_queue.put(offset_num)

                '''
                # 全部二级分类
                # opt_name_list = jsonpath.jsonpath(jsonobj, '$..opt_name')
                # 商品名称
                goods_name_list = jsonpath.jsonpath(jsonobj, '$..goods_name')
                # 商品名称 - 商品简略名称
                short_name_list = jsonpath.jsonpath(jsonobj, '$..short_name')
                # print(short_name_list)
                # 商品id(goods_id)
                goods_id_list = jsonpath.jsonpath(jsonobj, '$..goods_id')
                # print(goods_id_list)
                # 商品价格
                price_list = jsonpath.jsonpath(jsonobj, '$..price')
                # print(price_list)
                #print len(price_list)
                # 已拼件数
                cnt_list = jsonpath.jsonpath(jsonobj, '$..cnt')
                # print(cnt_list)
                #print len(cnt_list)
                for i in range(len(cnt_list)):
                    print  i
                '''



    # 开始爬取
    def start_crawl(self):
        self.create_offset_num_queue() # 生成偏移量的队列
        self.get_goods_data()


if __name__ == '__main__':
    computers_spiders = ComputersGoodsSpider()
    computers_spiders.start_crawl()