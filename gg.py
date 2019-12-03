# -*- coding: utf-8 -*-
import requests
import csv
import time
from bs4 import BeautifulSoup
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
}
proxies = {
    "http": "http://103.198.34.164:32425"
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
                    text = req.text
                    text = text.encode('ISO-8859-1').decode(req.apparent_encoding)
                    return text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def saveText(content):

    fout = open('/Applications/MAMP/htdocs/htdocs/python/a.text', 'w', encoding='utf8')
    # 写入文件内容
    fout.write(content)
    fout.close()

if __name__ == '__main__':
    url = 'https://www.biqugex.com/book_2986/1988263.html'

    result = reqPage(url)
    soup = BeautifulSoup(result, 'html5lib')
    text = soup.find('div', {'class': 'content'})


    title = text.find('h1').get_text()
    content = text.find(id='content').get_text()

    contents = title + "\n" + content
    saveText(contents)

    print('success')
    exit()
