import requests
import MySQLdb
from bs4 import BeautifulSoup
import time
import re
import struct
import logging
import redis
import json


offset=0
limit=10
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
}

proxies = {
    "https": "https://43.242.242.196:8080"
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
                req = requests.get(url, headers=headers,timeout=5)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def reqPageProxy(url,proxy):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers,proxies = proxy,timeout=5)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def getData(db_name):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )
    cur = conn2db.cursor()
    sql = "SELECT `id`,`video_access_address` FROM `xvideo_csv_%s`  where insert_time = 0 order by id desc limit %s,%s"% (db_name,offset,limit)
    # sql = "SELECT `id`,`video_access_address` FROM `xvideo_csv_%s`  where insert_time = 0 order by id asc limit %s,%s" % (
    # db_name, offset, limit)
    # sql = "SELECT `id`,`video_id`,`video_access_address`,`video_title` FROM `xvideo`  where video_duration = 0 order By id desc limit %s,%s" % (
    # offset, limit)
    cur.execute(sql)
    db_result = cur.fetchall()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result


if __name__ == '__main__':


    url = 'https://api.tube8.com/api.php?action=searchVideos&output=json&search=hard&thumbsize=all'

    response = reqPage(url)

    print(response)
    soup = BeautifulSoup(response, 'html5lib')

    'lang-drop-wrap'

    print(url)
    exit()