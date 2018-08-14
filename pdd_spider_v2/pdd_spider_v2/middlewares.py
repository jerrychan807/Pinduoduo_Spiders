# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
from scrapy import signals
import random
import linecache
import Queue
import codecs
from proxy import get_proxy_queue


class PddSpiderV2SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PddSpiderV2DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleWare(object):
    def __init__(self):
        self.proxy_ip_queue = Queue.Queue()  # 代理ip队列


    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        self.set_proxy_ip_queue()
        self.proxy = "http://{0}".format(self.proxy_ip_queue.get())
        print "[*] now , proxy_ip length is : {0}".format(       self.proxy_ip_queue.qsize())
        print("[+] this is request ip : " + self.proxy)
        request.meta['proxy'] = self.proxy


    def process_response(self, request, response, spider):
        '''对返回的response处理'''

        if response.status == 200:
            self.proxy_ip_queue.put(self.proxy.replace('http://',''))  # 该代理ip可用,放回ip代理池
            print("[**] this proxy ip is useful:" + self.proxy)
            print "[**] now , proxy_ip length is : {0}".format(self.proxy_ip_queue.qsize())
            return response
        else: # 如果返回的response状态不是200，重新生成当前request对象
            self.proxy_ip_using_num -= 10 # 该代理ip不可用,从代理ip池中去掉
            self.process_request(request, spider)
            return request

    def process_exception(self, request, exception, spider):
        import time
        time.sleep(2)
        self._faillog(request, u'EXCEPTION', exception, spider)
        self.proxy_ip_using_num -= 10  # 该代理ip不可用,从代理ip池中去掉
        self.process_request(request, spider)
        return request

    def _faillog(self, request, errorType, reason, spider):
        with codecs.open('faillog.log', 'a', encoding='utf-8') as file:
            file.write("%(now)s [%(error)s] %(url)s reason: %(reason)s \r\n" %
                       {'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'error': errorType,
                        'url': request.url,
                        'reason': reason})

    # reset代理ip池
    def set_proxy_ip_queue(self):
        print "[+] try to reset proxy ip queue"
        if self.proxy_ip_queue.empty(): # 代理ip池消耗完
            self.get_proxy_ip_queue()
            self.proxy_ip_using_num = self.proxy_ip_queue.qsize() * 10 # 若每个代理ip可用，则用10次
        if self.proxy_ip_using_num < 1: # 代理ip总初始次数用完
            self.get_proxy_ip_queue()
            self.proxy_ip_using_num = self.proxy_ip_queue.qsize() * 10


    def get_proxy_ip_queue(self):
        self.proxy_ip_queue = get_proxy_queue()




class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""


    def process_request(self, request, spider):
        tunnel = random.randint(1, 1036)
        user_agent = linecache.getline('1000ua-pc.log', tunnel)
        self.user_agent = user_agent.strip().replace('\n', '').replace('\r', '')
        # print "**************************"
        print "[*] ua is {0}".format(self.user_agent)
        # print "**************************"
        request.headers.setdefault('User-Agent', self.user_agent)
