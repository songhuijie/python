import requests
import MySQLdb
from bs4 import BeautifulSoup
import time
import re
import struct
import logging
import redis
import json

redis_key = 'request_video'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
}

proxies = {
    "https": "https://80.83.137.102:8888"
}

def reqPage(url,proxies):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers,proxies = proxies,timeout=5)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def getNeedProxy():
    #return proxy_ip_own
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

    proxy = r.get(redis_key)
    if proxy:
        return proxy
    else:
        proxy = getProxys()
        r.set(redis_key, proxy)
        return proxy

def getProxys():

    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

    proxy = r.lrange('rvideo',0,0)
    print(r.llen('rvideo'))
    if len(proxy) < 1:
        response_str = getProxydata()
        print(response_str)
        list = json.loads(response_str)
        # data = getProxydata()
        print(list)
        for value in list:
            print(value)
            r.lpush('rvideo', str(value['Ip']) + ':' + str(value['Port']))

        proxy = r.lrange('rvideo', 0, 0)

        r.ltrim('rvideo', 1, -1)
        return proxy[0]
    else:
        r.ltrim('rvideo', 1, -1)

        return  proxy[0]

def getProxydata():
    url = 'http://ged.ip3366.net/api/?key=20190829153652708&getnum=30&anonymoustype=3&filter=1&area=2&order=2&formats=2&proxytype=1'
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers,timeout=5)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def changeProxy():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    proxy = getProxys()
    r.set(redis_key, proxy)
    return proxy

if __name__ == '__main__':


    #
    urls = 'http://www.pornhub.com?utm_source=domain&utm_medium=banner-paid&utm_campaign=hubtraffic_jiedage'


    a = 1
    while a < 1002:
        time.sleep(5)
        proxy_ip = getNeedProxy()
        print(proxy_ip)
        proxy = {'https': ''}
        proxy['https'] = proxy_ip

        reqPage(urls, proxy)
        print(a)
        a += 1
        changeProxy()

    exit()
