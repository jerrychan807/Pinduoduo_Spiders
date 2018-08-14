# -*- coding:utf-8 -*-

# @Time    : 2018/8/3 1:54 PM
# @Author  : jerry



import urllib,urllib2
import json
import StringIO
import time
import Queue

# 填入自己的代理ip api地址
API_URL = ''

def remove_repeat(list):
    newlist = []
    for rep in list:  # rep:<type 'str'>
        if rep > 0:
            rep = rep.strip('\r\n')
            newlist.append(rep)
    return newlist


# 向api获取代理ip列表 list
def get_proxy_queue():
    proxy_ip_queue = Queue.Queue()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    }
    url = API_URL  # APi的URL
    req = urllib2.Request(url, headers=headers)
    time.sleep(2)  # 避免API请求过于频繁
    try:
        html = urllib2.urlopen(req).read()  # print type(html) #type为str
        buf = StringIO.StringIO(html)  # <type 'instance'>
        proxylist = remove_repeat(buf)
        if len(proxylist):  # 如果代理数量不为0
            print '[++] Got Proxy Num: %s' % len(proxylist)
            for proxy_ip in proxylist:
                proxy_ip_queue.put(proxy_ip)
            return proxy_ip_queue
        else:  # 如果代理数量为0
            print '[*] Got Proxy Num: %s' % len(proxylist)
            print '[-] The API website may be Error ! Try to Get The Proxy Again'
            return None

    except Exception, e:  # 出错情况下需要重新获取代理，设置最大的尝试次数为5
        print '[-] Can Not Get The Proxy'
        print '[-] Error: {e}'.format(e=e)

