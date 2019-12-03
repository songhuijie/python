# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import csv
import json as js
import json

proxies = {
    # "http": "http://178.79.46.5:59073"
    "http": "http://111.13.134.22:80"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',

}


singer_url = 'https://www.youtube.com/playlist?list=PLeS5BJRLpXLZdaNTAWDscN5fTaszromTV'

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

def GetListOfSingers(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理


                req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                # req = requests.get(url, headers=headers, proxies=proxies)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                # if req.status_code == 200:
                    # 返回BeautifulSoup对象
                return req.text
        except:
            pass
        time.sleep(3)
        num += 1

def saveData(data):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )

    cur = conn2db.cursor()
    sql = "INSERT INTO `singer_list` ( `sing_name`) VALUES "

    for value in data:
        sql += ' ("' + value + '"),'
    sql += " ('success');"

    # print(sql)
    # exit()
    cur.execute(sql)
    conn2db.commit()
    cur.close()
    conn2db.close()
    return 'true'


def MakeData(data):
    text = json.loads(data)
    singer_insert_data = []
    if (text['code'] == 'SUCCESS'):
        singer_data = text['result']['data']['artists']
        for value in singer_data:
            singer_insert_data.append(value['artistName'])

    else:
        print(2)
    return singer_insert_data

if __name__ == '__main__':


    data = GetListOfSingers(singer_url)
    handle_data = MakeData(data)

    if handle_data:
        saveData(handle_data)
    else:
        print('continue')
        exit()
    print('success')
    exit()