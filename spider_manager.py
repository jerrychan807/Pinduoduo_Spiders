# -*- coding:utf-8 -*-

# @Time    : 2018/8/4 4:41 PM
# @Author  : jerry

from multiprocessing import Pool
# import subprocess
from firstcat_spider import FirstCategoryGoodsSpider
import mongo_db


def start_first_cat_spider(opt_id):
    first_cat_spider = FirstCategoryGoodsSpider(opt_id)
    first_cat_spider.start_crawl()

'''
class SpiderManager():
    def __init__(self):
        self.opt_id_list = mongo_db.get_optid_list()


    def distribute_task(self):
        task_pool = Pool(5)

        for opt_id in self.opt_id_list[0:2]:
            opt_id = str(opt_id)
            print opt_id
            # task_pool.apply_async(start_first_cat_spider, args=(opt_id,))
            task_pool.apply(start_first_cat_spider, opt_id)
        print('Waiting for all subprocesses done...')
        task_pool.close()  # 关闭进程池，表示不能在往进程池中添加进程
        task_pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
        print('All subprocesses done.')
'''



        # opt_id = self.opt_id_list[0]
        # #for opt_id in self.opt_id_list[0]:
        # subprocess.Popen(
        # ["python", "/Users/chanjerry/Desktop/oksec/9.development/pdd_spider/firstcat_spider.py", str(opt_id)])




if __name__ == '__main__':
    opt_id_list = mongo_db.get_optid_list()
    task_pool = Pool(5)
    for opt_id in opt_id_list[0:2]:
        opt_id = str(opt_id)
        print opt_id
        # task_pool.apply_async(start_first_cat_spider, args=(opt_id,))
        task_pool.apply(start_first_cat_spider, args=(opt_id,))
    print('Waiting for all subprocesses done...')
    task_pool.close()  # 关闭进程池，表示不能在往进程池中添加进程
    task_pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
    print('All subprocesses done.')