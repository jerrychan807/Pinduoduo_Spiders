# -*- coding:utf-8 -*-

# @Time    : 2018/8/2 2:03 PM
# @Author  : jerry

import pymongo
from pymongo import MongoClient


db_host = "127.0.0.1"
db_port = 27017
db_name = "pdd_test"
#db_username = str(config.DB_USERNAME)
#db_password = str(config.DB_PASSWORD)
START_OFFSET_NUM = 0
END_OFFSET_NUM = 1000
OPT_ID_LIST = [14,1281,4,15,1,1282,743,18,13,1917,818,1543,16,1451,2048,2478]


def insertCategory(info_dict):
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    coll = db.second_category
    try:
        rs = coll.insert_one(info_dict)
    except pymongo.errors.DuplicateKeyError, e:
        print(e)
    return True



def insert_goods_dict(goods_dict):
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    coll = db.goods
    try:
        rs = coll.insert_one(goods_dict)
    except pymongo.errors.DuplicateKeyError, e:
        print(e)
        pass
    return True

def get_optid_list():
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    COLLECTION = "category"
    db_coll = db[COLLECTION]
    # queryArgs = {'optID':2478}
    queryArgs = {}
    projectionFields = {'_id': False,'optID':True}  # 用字典指定
    searchRes = db_coll.find(queryArgs, projection = projectionFields)
    optid_list = [record['optID'] for record in searchRes]
    return optid_list


def check_offset_num_exists(offset_num_dict):
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    db_coll = db.offsetnum
    rs = db_coll.find_one(offset_num_dict)
    if rs:
        return True
    else:
        return False


def insert_offset_num_dict(offset_num_dict):
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    coll = db.offsetnum
    try:
        rs = coll.insert_one(offset_num_dict)
    except pymongo.errors.DuplicateKeyError, e:
        print(e)
        #pass
    return True


def get_new_opt_id():
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    COLLECTION = "offsetnum"
    db_coll = db[COLLECTION]
    for opt_id in OPT_ID_LIST:
        offset_num_len = db_coll.count({"optID":opt_id})
        if offset_num_len >= 1000:
            continue
        else:
            return opt_id
    return None


def get_category_infos(opt_id):
    client = MongoClient(db_host, db_port)
    db = client[db_name]
    COLLECTION = "category"
    db_coll = db[COLLECTION]
    query_dict = {"optID":opt_id}
    result = db_coll.find_one(query_dict)
    return result


if __name__ == '__main__':
    # client = MongoClient(db_host, db_port)
    # db = client.pdd
    # coll = db.category
    # rs = coll.insert_one({'a': 1, 'b': 2})
    # print(rs)
    opt_id = 14
    result = get_category_infos(opt_id)

    for second_cats in result['cat']:
        print second_cats