# -*- coding:utf-8 -*-

# @Time    : 2018/8/2 2:03 PM
# @Author  : jerry

import pymongo
from pymongo import MongoClient

import config

db_host = str(config.DB_HOST)
db_port = int(config.DB_PORT)
db_name = str(config.DB_NAME)
#db_username = str(config.DB_USERNAME)
#db_password = str(config.DB_PASSWORD)



def insertCategory(info_dict):
    client = MongoClient(db_host, db_port)
    db = client.pdd
    coll = db.category
    rs = coll.insert_one(info_dict)
    return True


def insertComputersGoods(info_dict):
    client = MongoClient(db_host, db_port)
    db = client.pdd
    coll = db.computer
    try:
        rs = coll.insert_one(info_dict)
    except pymongo.errors.DuplicateKeyError, e:
        print(e)
        #pass
    return True


def insert_goods_dict(goods_dict):
    client = MongoClient(db_host, db_port)
    db = client.pdd
    coll = db.goods
    try:
        rs = coll.insert_one(goods_dict)
    except pymongo.errors.DuplicateKeyError, e:
        #print(e)
        pass
    return True

def get_optid_list():
    client = MongoClient(db_host, db_port)
    database = db_name
    db = client[database]
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
    database = db_name
    db = client[database]
    db_coll = db.offsetnum
    rs = db_coll.find_one(offset_num_dict)
    if rs:
        return True
    else:
        return False


def insert_offset_num_dict(offset_num_dict):
    client = MongoClient(db_host, db_port)
    database = db_name
    db = client[database]
    coll = db.offsetnum
    try:
        rs = coll.insert_one(offset_num_dict)
    except pymongo.errors.DuplicateKeyError, e:
        print(e)
        #pass
    return True


if __name__ == '__main__':
    # client = MongoClient(db_host, db_port)
    # db = client.pdd
    # coll = db.category
    # rs = coll.insert_one({'a': 1, 'b': 2})
    # print(rs)
    # collection = "pdd"
    # print connectiondb(collection)
    # optid_list = query_optid_list()
    # print optid_list
    offset_num_dict = {"optID":1,"offset_num":2}
    # insert_offset_num_dict(offset_num_dict)
    print check_offset_num_exists(offset_num_dict)