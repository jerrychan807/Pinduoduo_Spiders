# -*- coding:utf-8 -*-

# @Time    : 2018/8/2 2:03 PM
# @Author  : jerry

import pymongo
from pymongo import MongoClient
import config

db_host = str(config.DB_HOST)
db_port = int(config.DB_PORT)
#db_name = str(config.DB_NAME)
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


if __name__ == '__main__':
    client = MongoClient(db_host, db_port)
    db = client.pdd
    coll = db.category
    rs = coll.insert_one({'a': 1, 'b': 2})
    print(rs)
    # collection = "pdd"
    # print connectiondb(collection)


