# -*- coding:utf-8 -*-

# @Time    : 2018/8/4 2:54 PM
# @Author  : jerry

# optId-collections-map


import random,sys,time
import Queue
import json,jsonpath
import requests
import linecache
import mongo_db

from proxy import get_proxy_queue



start_offset_num = 0
end_offset_num = 1000


# 一级分类商品信息爬虫类
class FirstCategoryGoodsSpider():
    def __init__(self,optid):

        self.opt_id = int(optid)
        self.offset_num_queue = Queue.Queue()
        self.proxy_ip_queue = Queue.Queue()  # 代理ip队列
        print "[+] Create Instance opt_id : {0} spider successfully ".format(self.opt_id)


    def run(self):
        self.start_crawl()


    # 获取代理ip队列
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


    # 随机设置api地址
    def set_crawl_url(self,opt_id,offset_num):
        # api_num:2,3,4
        api_num = random.randint(2,4)
        self.url = "http://apiv{api_num}.yangkeduo.com/operation/{opt_id}/groups?opt_type=1&size=100&offset={offset_num}&flip=&pdduid=0".format(opt_id=opt_id,api_num=api_num,offset_num=offset_num)



    def create_offset_num_queue(self, opt_id):
        global start_offset_num, end_offset_num
        for offset_num in range(start_offset_num, end_offset_num):
            offset_num_dict = {"optID": opt_id, "offset_num": offset_num}
            if not mongo_db.check_offset_num_exists(offset_num_dict):
                self.offset_num_queue.put(offset_num)
        print "[*] create opt_id : {0} offset_num_queue , len is {1}".format( self.opt_id,self.offset_num_queue.qsize())


    def get_html(self, proxy_ip):
        self.change_useragent()
        proxies = {
            "http": "http://{0}".format(proxy_ip)
        }

        print "[*] requesting url : {0}".format(self.url)
        try:
            response = requests.get(self.url, headers=self.headers,proxies=proxies,timeout=5)
        except requests.exceptions.ConnectTimeout,e:
            print e
            raise RuntimeError('error')
        except requests.exceptions.ReadTimeout,e:
            print e
            raise RuntimeError('error')
        except requests.exceptions.ProxyError,e:
            print e
            raise RuntimeError('error')
        except requests.exceptions.ConnectionError,e:
            print e
            raise RuntimeError('error')
        else:
            if response.status_code == 200:
                html_data = response.content
                return html_data
            else: # 尝试过几秒重连
                pass
        return None

    def start_crawl(self):
        self.create_offset_num_queue(self.opt_id)  # 生成偏移量的队列
        while not self.offset_num_queue.empty(): # 要把偏移量队列消耗完
            offset_num = self.offset_num_queue.get()
            self.set_crawl_url(opt_id,offset_num) # 设置爬虫api url
            self.get_goods_data(offset_num) # 爬取商品信息数据


    # reset代理ip池
    def set_proxy_ip_queue(self):
        if self.proxy_ip_queue.empty(): # 代理ip池消耗完
            self.get_proxy_ip_queue()
            self.proxy_ip_using_num = self.proxy_ip_queue.qsize() * 10 # 若每个代理ip可用，则用10次
        if self.proxy_ip_using_num < 1: # 代理ip总初始次数用完
            self.get_proxy_ip_queue()
            self.proxy_ip_using_num = self.proxy_ip_queue.qsize() * 10


        # 获取商品信息,入库
    def get_goods_data(self,offset_num):
        self.set_proxy_ip_queue()
        proxy_ip = self.proxy_ip_queue.get()

        print "[*] using offset_num : {0}".format(offset_num)

        try:
            html_data = self.get_html(proxy_ip)  # 获取json数据
        except RuntimeError: # 该代理ip不可用,从代理ip池中去掉
            self.proxy_ip_using_num -= 10
        else:
            self.proxy_ip_queue.put(proxy_ip) # 该代理ip可用,放回ip代理池
            if html_data:
                jsonobj = json.loads(html_data.decode('utf-8'))
                self.insert_goods_info(jsonobj)
                mongo_db.insert_offset_num_dict({"optID": self.opt_id, "offset_num": offset_num})
                print "[+] successfully get html_data , handle offset_num : {0}".format(offset_num)
            else: # 该offset_num没查到数据,放回偏移量任务队列中去
                print "[-] failed handle offset_num : {0}".format(offset_num)
                self.offset_num_queue.put(offset_num)
        print '------------------------------------------------'

    # 入库商品信息
    def insert_goods_info(self, jsonobj):
        for each_good in jsonobj['goods_list']:
            good_dict = {}
            good_dict['_id'] = each_good['goods_id']  # 商品id
            good_dict['goods_name'] = each_good['goods_name']  # 商品名称
            good_dict['normal_price'] = each_good['normal_price']
            good_dict['market_price'] = each_good['market_price']
            good_dict['price'] = each_good['group']['price']  # 商品价格
            good_dict['cnt'] = each_good['cnt']  # 已拼件数
            mongo_db.insert_goods_dict(good_dict)


if __name__ == '__main__':
    #optid_list = [2478]
    # optid_list = mongo_db.query_optid_list()

    opt_id = int(sys.argv[1])
    # opt_id = 2478
    first_cat_spider = FirstCategoryGoodsSpider(opt_id)
    first_cat_spider.start_crawl()
