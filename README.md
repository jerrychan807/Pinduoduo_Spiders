# 拼多多爬虫


## description:

version1:

- base on `requests`
- 爬取拼多多某一级分类下的所有商品信息

version2:

- base on framework `scrapy`
- 爬取拼多多所有的商品信息:



---

##Requirements

- python2
- 多代理



---

## Usage:

1. 在`proxy.py`里填入自己的代理ip的api地址
2. 在`mongo_db.py`配置一下本地MongoDB数据库的信息

### Version1 usage:

3. `python firstcat_spider.py {opt_id}`

 - ![](https://ws2.sinaimg.cn/large/006tKfTcgy1ftxu5yfvbpj30zm0k61fj.jpg)
 - opt_id : 一级分类商品的id

4. start to crawl all goods info with this opt_id

### Version2 usage:



---

## To-do-list:


* [x] 爬取分类信息(一级-二级)
* [x] MongoDB入库
    * [x] 入分类信息
* [x] 爬取某一级分类下的所有商品信息
    * [x] 入库-入商品信息
    * [x] 入库-入offset_num信息
* [x] 修改成scrapy逛街
* [x] 优化代码


---



---


## screenshots

![](https://ws2.sinaimg.cn/large/006tKfTcgy1ftxuhpq3zoj315o0e07nz.jpg)

---

## log:

- 2018.8.4 18:16:
 - goods num : 4312
- 2018.8.10 18:16:
 - goods num : 20414

---

## contact:

you can send email to me : `NTI5ODgzNDA5QHFxLmNvbQ==`


