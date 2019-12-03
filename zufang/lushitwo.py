import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',

}

f = open(r'lushi.txt', 'r')  # 打开所保存的cookies内容文件
cookies = {}  # 初始化cookies字典变量
for line in f.read().split(';'):  # 按照字符：进行划分读取
    # 其设置为1就会把字符串拆分成2份
    name, value = line.strip().split('=', 1)
    cookies[name] = value

proxies = {
    "http": "http://200.5.203.58:52116"
}

def reqPage(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies,timeout = 5)
                # req = requests.get(url, headers=headers,proxies = proxies,timeout = 5)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

if __name__ == '__main__':


    url = 'http://hs.gameyw.netease.com/hs/c/cg_liupai_info?code=b23cfc0dd875e7c215bb0ec707e778f5'

    text = reqPage(url)
    print(text)
    exit()