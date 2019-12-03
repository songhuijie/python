# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time

proxies = {
    # "http": "http://178.79.46.5:59073"
    "http": "http://177.39.187.70:37315"
}
url_index = 'https://www.rakumachi.jp'
url_area = 'https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Origin': 'https://cd.lianjia.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
}
f = open(r'house.txt', 'r')  # 打开所保存的cookies内容文件
cookies = {}  # 初始化cookies字典变量
for line in f.read().split(';'):  # 按照字符：进行划分读取
    # 其设置为1就会把字符串拆分成2份
    name, value = line.strip().split('=', 1)
    cookies[name] = value


def reqPages(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                # req = requests.get(url, headers=headers)
                req = requests.get(url, headers=headers,cookies = cookies)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def Is_login(url):

    soup = reqPages(url)

    # login_status = soup.select('p[class^="R163__message"]')
    login_not_status = soup.select('p[class^="R163__kaiintouroku"]')
    if len(login_not_status) == 0:
        print('登录')
    else:
        print('未登录')

    exit()

    return True


if __name__ == '__main__':

    result = Is_login(url_index)

    print(result)
    exit()