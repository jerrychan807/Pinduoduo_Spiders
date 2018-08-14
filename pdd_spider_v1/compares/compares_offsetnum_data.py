# -*- coding:utf-8 -*-

# @Time    : 2018/8/13 9:19 AM
# @Author  : jerry

import json



def get_goodsid_list(html_data):
    jsonobj = json.loads(html_data.decode('utf-8'))
    goods_id_list = []
    for each_good in jsonobj['goods_list']:
        goods_id_list.append(each_good['goods_id'])  # 商品id

    return goods_id_list



def diff(list1,list2):
    return list(set(list1).difference(set(list2)))

def same(list1,list2):
    return list(set(list1).intersection(set(list2)))



if __name__ == '__main__':

    with open('201.html','r') as f:
        goods_id_list1 = get_goodsid_list(f.read())

    with open('201_1.html', 'r') as f:
        goods_id_list2 = get_goodsid_list(f.read())

    # with open('3.html', 'r') as f:
    #     goods_id_list3 = get_goodsid_list(f.read())




    print "[*] diff length is {0}" .format(len(diff(goods_id_list1, goods_id_list2)))

    print "[*] same length is {0}".format(len(same(goods_id_list1, goods_id_list2)))

    print '**********************************'
    #
    # print diff(goods_id_list2, goods_id_list3)
    # print same(goods_id_list2, goods_id_list3)
    #
    # print '**********************************'
    # print diff(goods_id_list1, goods_id_list3)
