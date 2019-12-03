import requests
import MySQLdb
from bs4 import BeautifulSoup
import time
import redis
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',

}

redis_key = 'xvideo_key'

def getNeedProxy():
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

    proxy = r.lrange('redis_proxy', 0, 0)
    print(r.llen('redis_proxy'))
    if len(proxy) < 1:
        response_str = getProxydata()
        print(response_str)
        list = json.loads(response_str)
        # data = getProxydata()
        print(list)
        for value in list:
            print(value)
            r.lpush('redis_proxy', str(value['Ip']) + ':' + str(value['Port']))

        proxy = r.lrange('redis_proxy', 0, 0)

        r.ltrim('redis_proxy', 1, -1)
        return proxy[0]
    else:
        r.ltrim('redis_proxy', 1, -1)

        return proxy[0]

def getProxydata():
    url = 'http://www.ip3366.net/action/'
    post_data = 'key=20190829153652708&getnum=30&isp=0&anonymoustype=0&start=&port=&notport=&ipaddress=&unaddress=&area=2&order=1&formats=2&splits=&proxytype=1'
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.post(url, data = post_data,headers=headers,timeout=5)
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

    print(1)