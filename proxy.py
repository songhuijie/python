import requests
import time
import redis
from bs4 import BeautifulSoup


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
                req = requests.get(url, headers=headers)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def HandleUrl(page):

    own_url = 'http://www.ip3366.net/free/?stype=3&page=%s' % (page)

    return own_url

def setProxys(data):

    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

    for i in data:
        r.lpush('proxy',i)

def getProxys():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

    proxy = r.lrange('proxy', 0, 0)

    if len(proxy) < 1:
        return False
    else:
        return True


if __name__ == '__main__':



    proxy = getProxys()
    if proxy == True:
        exit()

    url = 'http://www.ip3366.net/free/?stype=3&page=3'

    req = reqPage(url)
    soup = BeautifulSoup(req, 'html5lib')

    data_list = []  # 结构: [dict1, dict2, ...], dict结构{'船名': ship_name, '航次': voyage, '提单号': bill_num, '作业码头': wharf}
    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            if tds[3].contents[0] == 'HTTPS':
                data_list.append(tds[0].contents[0] + ':' + tds[1].contents[0])

    data_page = [4, 5, 6, 7]

    for i in data_page:
        time.sleep(3)
        this_url = HandleUrl(i)
        req = reqPage(this_url)
        soup = BeautifulSoup(req, 'html5lib')
        for idx, tr in enumerate(soup.find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                if tds[3].contents[0] == 'HTTPS':
                    data_list.append(tds[0].contents[0] + ':' + tds[1].contents[0])

    setProxys(data_list)
    print('success')
    exit()