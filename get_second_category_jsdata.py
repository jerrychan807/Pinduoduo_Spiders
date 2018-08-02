# -*- coding:utf-8 -*-

# @Time    : 2018/8/2 3:48 PM
# @Author  : jerry



import os,re,time,random
import json,jsonpath
import requests
import linecache
from lxml import etree

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


'''
first_category_dicts = {
    "":"",
    
}
'''


class GetJsData():
    def __int__(self):
        self.second_category_url = "http://apiv3.yangkeduo.com/operation/14/groups?opt_type=1&size=100&offset=0&flip=&pdduid=0"


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

    # 开始爬取
    def startCrawl(self):
        self.change_useragent()



        res = requests.get(url, headers=self.headers)
        if res.status_code == 200:
            print res.content
            second_html_data = etree.HTML(res.content)
            # all_li_data = second_html_data.xpath('''//*[@id="catname-slide-up"]/div[2]//span/text()''')




            time.sleep(1)




if __name__ == '__main__':
    tester = GetJsData()
    tester.startCrawl()