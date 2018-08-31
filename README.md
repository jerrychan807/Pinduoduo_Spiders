# 拼多多爬虫


## screenshots

- 已爬取的商品信息条数(70w+):
 - ![](https://ws4.sinaimg.cn/large/0069RVTdgy1fusovmf76qj30hy03a75h.jpg) 

- 商品信息示例:
 - ![](https://ws2.sinaimg.cn/large/006tKfTcgy1ftxuhpq3zoj315o0e07nz.jpg)

---

## description:

version2:

- base on framework `scrapy`
- 爬取拼多多所有的商品信息



---

## Requirements

- python2
- 多代理
-  `scrapy`


---

## Usage:

1. 在`proxy.py`里填入自己的代理ip的api地址
2. 在`mongo_db.py`配置一下本地MongoDB数据库的信息
3. 根据自己的代理、网络带宽、主机性能等情况修改`settings.py`中的并发请求数`CONCURRENT_REQUESTS`

### Version2 usage:

1. 进入到 `pdd_spider_v2`目录下
2. 先爬取所有二级、三级分类信息 `scrapy crawl category_infos`
3. 爬取所有商品分类信息 `scrapy crawl goods`


---

## To-do-list:


* [x] 爬取分类信息(一级-二级)
* [x] MongoDB入库
    * [x] 入分类信息
* [x] 爬取某一级分类下的所有商品信息
    * [x] 入库-入商品信息
    * [x] 入库-入offset_num信息
* [x] 修改成scrapy框架
    * [x] 优化代码
    * [x] 减少页面的爬取




---

## log:

- 2018.8.4 18:16:
 - goods num : 4312
- 2018.8.10 18:16:
 - goods num : 20414
- 2018.8.31 18:16:
 - goods num : 70w+

---

## contact:

you can send email to me : `NTI5ODgzNDA5QHFxLmNvbQ==`


