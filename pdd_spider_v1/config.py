# -*- coding:utf-8 -*-

# @Time    : 2018/8/1 8:09 PM
# @Author  : jerry


import configparser

FILE = "config.ini"

config = configparser.ConfigParser()
config.read(FILE)
config.sections()

DB_HOST = config['CONFIG']['DB_HOST']
DB_PORT = config['CONFIG']['DB_PORT']
DB_NAME = config['CONFIG']['DB_NAME']
DB_USERNAME = config['CONFIG']['DB_USERNAME']
DB_PASSWORD = config['CONFIG']['DB_PASSWORD']



