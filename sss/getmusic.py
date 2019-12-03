import requests
import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
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
                # req = requests.get(url, headers=headers,cookies = cookies)
                req = requests.get(url, headers=headers)
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1


if __name__ == '__main__':

    url = 'http://dl.stream.qqmusic.qq.com/C400003mAan70zUy5O.m4a?guid=8718150648&vkey=E38753C163D9562864A730DF2B3862E4014704E1FB08FD364E6447BBC5D267C41349F7B5E71A6B606F899EE7D72865ED4E033964D1204352&uin=5439&fromtag=3&r=5494786824305276'
    print(reqPage(url))
    exit()