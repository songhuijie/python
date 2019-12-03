# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import csv
import logging
from urllib import request
from urllib import parse
import ssl
import re
from collections import OrderedDict
import math
import json
ssl._create_default_https_context = ssl._create_unverified_context

proxies = {
    # "http": "http://178.79.46.5:59073"
    "http": "http://177.39.187.70:37315"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Origin': 'https://cd.lianjia.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
}

def reqPage(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers,proxies = proxies)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def douban(url):
    proxy = "http://87.228.103.111:8080"
    proxy_support = request.ProxyHandler({'http': proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    req = request.Request(url, headers=headers)
    data = request.urlopen(req)
    html = data.read().decode("utf-8")

    needs = json.loads(html)

    data = []
    for value in needs.get('subjects'):
        tmp = []
        tmp.append(value.get('title'))
        tmp.append(value.get('rate'))
        data.append(tmp)

    SaveD(data)
    return True


def SaveD(data):
    with open("/Applications/MAMP/htdocs/htdocs/python/doubanpingfen.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp =[]
        for value in data:
            tmp.append(value)

        csvwriter.writerows(tmp)
    return 'true'

if __name__ == '__main__':


    page = [20,40,60,100]


    for value in page:
        time.sleep(3)
        next = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=%s' % (
        '%E7%83%AD%E9%97%A8', value)
        douban(next)

    print('s')
    exit()


