# -*- coding:utf-8 -*-

# @Time    : 2018/8/1 8:09 PM
# @Author  : jerry


import configparser

FILE = "config.ini"

config = configparser.ConfigParser()
config.read(FILE)
config.sections()

API_KEY = config['CONFIG']['API_KEY']
NUMBER = config['CONFIG']['NUMBER']
SENDER = config['CONFIG']['SENDER']
TEAM = config['CONFIG']['TEAM']