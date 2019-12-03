# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import csv

proxies = {
    # "http": "http://178.79.46.5:59073"
    "http": "http://177.39.187.70:37315"
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
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
                # req = requests.get(url, headers=headers)
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def HandleMessage(soup):

    result = soup.select('.topic-title')

    arr = []
    tmp = []
    for value in result:
        arr.append(value.text.strip())


    SaveMessage(arr)
    return True

def SaveMessage(data):
    with open("/Applications/MAMP/htdocs/htdocs/python/message.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        # tmp = []
        # for value in data:
        #     tmp.append(value)
        tmp = []
        for value in data:
            tmp.append(value)

        csvwriter.writerow(tmp)

        # csvwriter.writerows(tmp)
    return 'true'

if __name__ == '__main__':

    url = 'https://learnku.com/laravel'
    result = reqPage(url)
    bool = HandleMessage(result)
    print(bool)