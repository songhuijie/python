#! -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import time
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authority': 'ip.ihuan.me',
}

cookies = '__cfduid=d4b6a1d0135e5f7e81e512b46b3eec1661565571832; Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829=1565571860; statistics=c62bcec6dba699768a10a7a258543b88; cf_clearance=1741a5efc57e882755912f1256314a1563df1d16-1565935485-1800-250; Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829=1565935501'
def GetListOfSingers(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理


                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                # req = requests.get(url, headers=headers, proxies=proxies)
                req = requests.get(url, headers=headers,cookies = cookies)
                # req = requests.get(url)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                # if req.status_code == 200:
                    # 返回BeautifulSoup对象
                print(req.text)
                return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def handleImg(soup):
    img_html = soup.find('div', {'class': 'article-con'})
    try:
        img = img_html.find('center').find('img').get('src')
    except:
        img = ''

    return  img

def remen(soup):
    card = soup.find_all('div',{'class':'cardsgroup-item'})

    cards = []
    for value in card:
        cards.append([value.find('span').get_text(),value.find('a').get('href')])

    return cards

def main(str):
    # singer_url  = 'https://ip.ihuan.me'
    # data = GetListOfSingers(singer_url)

    soup = BeautifulSoup(str,'lxml')

    result = soup.find_all('tr')
    for i in range(len(result)):

        if i == 0 :
            continue
        else:
            if "中国" in result[i].find_all('td')[2].get_text():
                continue
            elif result[i].find_all('td')[4].get_text() == '不支持':
                continue
            else:
                print(result[i].find_all('td')[0].get_text() + ':' + result[i].find_all('td')[1].get_text())


    exit()




if __name__ == '__main__':
    #$('table').html()
    str = '<thead><tr><th>IP地址</th><th>端口</th><th>地理位置</th><th>运营商</th><th>HTTPS</th><th>POST</th><th>匿名度</th><th>访问速度</th><th>入库时间</th><th>最后检测</th></tr></thead><tbody><tr><td><a href="/check.html?proxy=MTE3LjIzOS4zOC44MTo1MDM3Ng==" target="_blank"><img src="/flag/IN.svg">117.239.38.81</a></td><td>50376</td><td><a href="/address/5Y2w5bqm.html">印度</a>&nbsp;<a href="/address/5Y2w5bqm.html">印度</a>&nbsp;</td><td><a href="/isp/YnNubC5jby5pbg==.html">bsnl.co.in</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>4.83秒</td><td>3小时前</td><td>16秒前</td></tr><tr><td><a href="/check.html?proxy=MTkxLjcuMjAwLjE3NDo1MzIzMA==" target="_blank"><img src="/flag/BR.svg">191.7.200.174</a></td><td>53230</td><td><a href="/address/5be06KW/.html">巴西</a>&nbsp;<a href="/address/5be06KW/.html">巴西</a>&nbsp;</td><td><a href="/isp/b25saW5lLm5ldC5icg==.html">online.net.br</a></td><td>不支持</td><td>不支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>15.02秒</td><td>2小时前</td><td>16秒前</td></tr><tr><td><a href="/check.html?proxy=NDMuMjQyLjI0Mi4xOTY6ODA4MA==" target="_blank"><img src="/flag/MN.svg">43.242.242.196</a></td><td>8080</td><td><a href="/address/6JKZ5Y+k.html">蒙古</a>&nbsp;<a href="/address/6JKZ5Y+k.html">蒙古</a>&nbsp;</td><td><a href="/isp/.html"></a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>6.99秒</td><td>3天前</td><td>16秒前</td></tr><tr><td><a href="/check.html?proxy=MTE4LjE3NC4yMzIuMTI4OjQ1MDE5" target="_blank"><img src="/flag/TH.svg">118.174.232.128</a></td><td>45019</td><td><a href="/address/5rOw5Zu9.html">泰国</a>&nbsp;<a href="/address/5YyX6YOo5aSn5Yy6.html">北部大区</a>&nbsp;</td><td><a href="/isp/dG90LmNvLnRo.html">tot.co.th</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>6.91秒</td><td>3小时前</td><td>16秒前</td></tr><tr><td><a href="/check.html?proxy=MTExLjI5LjMuMTg0OjgwODA=" target="_blank"><img src="/flag/CN.svg">111.29.3.184</a></td><td>8080</td><td><a href="/address/5Lit5Zu9.html">中国</a>&nbsp;<a href="/address/5rW35Y2X.html">海南</a>&nbsp;<a href="/address/5rW35Y+j.html">海口</a>&nbsp;</td><td><a href="/isp/56e75Yqo.html">移动</a></td><td>不支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>0.28秒</td><td>2天前</td><td>16秒前</td></tr><tr><td><a href="/check.html?proxy=MzYuNjcuNDIuMzk6NDk0OTM=" target="_blank"><img src="/flag/ID.svg">36.67.42.39</a></td><td>49493</td><td><a href="/address/5Y2w5bqm5bC86KW/5Lqa.html">印度尼西亚</a>&nbsp;<a href="/address/5Lic54iq5ZOH55yB.html">东爪哇省</a>&nbsp;</td><td><a href="/isp/dGVsa29tLmNvLmlk.html">telkom.co.id</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>7.63秒</td><td>1小时前</td><td>16秒前</td></tr><tr><td><a href="/check.html?proxy=MTgyLjkzLjgwLjM3OjgwODA=" target="_blank"><img src="/flag/NP.svg">182.93.80.37</a></td><td>8080</td><td><a href="/address/5bC85rOK5bCU.html">尼泊尔</a>&nbsp;<a href="/address/5bC85rOK5bCU.html">尼泊尔</a>&nbsp;</td><td><a href="/isp/c3ViaXN1Lm5ldC5ucA==.html">subisu.net.np</a></td><td>不支持</td><td>支持</td><td><a href="/anonymity/1.html">普匿</a></td><td>29.24秒</td><td>2小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MjEyLjIwNS4xMTIuMTYyOjU3MjA1" target="_blank"><img src="/flag/GR.svg">212.205.112.162</a></td><td>57205</td><td><a href="/address/5biM6IWK.html">希腊</a>&nbsp;<a href="/address/6Zi/5o+Q5Y2h5aSn5Yy6.html">阿提卡大区</a>&nbsp;<a href="/address/6ZuF5YW4.html">雅典</a>&nbsp;</td><td><a href="/isp/Y29zbW90ZS5ncg==.html">cosmote.gr</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>3.2秒</td><td>3天前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MTg1Ljc1LjUuMTU4OjYwODE5" target="_blank"><img src="/flag/RU.svg">185.75.5.158</a></td><td>60819</td><td><a href="/address/5L+E572X5pav.html">俄罗斯</a>&nbsp;<a href="/address/5pav5aGU5aSr572X5rOi5bCU6L6555aG5Yy6.html">斯塔夫罗波尔边疆区</a>&nbsp;<a href="/address/55qu5Lqa5a2j5oiI5bCU5pav5YWL.html">皮亚季戈尔斯克</a>&nbsp;</td><td><a href="/isp/MXRlbGVjb20ucnU=.html">1telecom.ru</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>52.68秒</td><td>11小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MTg2LjIxMS4xNzYuMTkwOjM4OTM0" target="_blank"><img src="/flag/BR.svg">186.211.176.190</a></td><td>38934</td><td><a href="/address/5be06KW/.html">巴西</a>&nbsp;<a href="/address/5be06KW/.html">巴西</a>&nbsp;</td><td><a href="/isp/Y29tbWNvcnAuY29tLmJy.html">commcorp.com.br</a></td><td>不支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>3.98秒</td><td>4小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MzYuOTAuMjA5LjQwOjgwODA=" target="_blank"><img src="/flag/ID.svg">36.90.209.40</a></td><td>8080</td><td><a href="/address/5Y2w5bqm5bC86KW/5Lqa.html">印度尼西亚</a>&nbsp;<a href="/address/5Lic54iq5ZOH55yB.html">东爪哇省</a>&nbsp;</td><td><a href="/isp/dGVsa29tLmNvLmlk.html">telkom.co.id</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>1.63秒</td><td>1小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MTEyLjEyLjM3LjE5Njo1MzI4MQ==" target="_blank"><img src="/flag/CN.svg">112.12.37.196</a></td><td>53281</td><td><a href="/address/5Lit5Zu9.html">中国</a>&nbsp;<a href="/address/5rWZ5rGf.html">浙江</a>&nbsp;<a href="/address/6YeR5Y2O.html">金华</a>&nbsp;</td><td><a href="/isp/56e75Yqo.html">移动</a></td><td>不支持</td><td>支持</td><td><a href="/anonymity/1.html">普匿</a></td><td>10.47秒</td><td>14小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MTY3Ljg2Ljc3LjM5OjgwMDA=" target="_blank"><img src="/flag/DE.svg">167.86.77.39</a></td><td>8000</td><td><a href="/address/5b635Zu9.html">德国</a>&nbsp;<a href="/address/5be05LyQ5Yip5Lqa5bee.html">巴伐利亚州</a>&nbsp;<a href="/address/57q95Lym5aCh.html">纽伦堡</a>&nbsp;</td><td><a href="/isp/Y29udGFiby5kZQ==.html">contabo.de</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>19.33秒</td><td>6小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=OTEuMjAwLjEyNC4xOTc6MzA4NDU=" target="_blank"><img src="/flag/UA.svg">91.200.124.197</a></td><td>30845</td><td><a href="/address/5LmM5YWL5YWw.html">乌克兰</a>&nbsp;<a href="/address/5Z+66L6F5bee.html">基辅州</a>&nbsp;<a href="/address/5LyK5bCU5bmz.html">伊尔平</a>&nbsp;</td><td><a href="/isp/aWxhbi5jb20udWE=.html">ilan.com.ua</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>5.3秒</td><td>2小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MjAxLjIxNy40LjEwMTo1MzI4MQ==" target="_blank"><img src="/flag/PY.svg">201.217.4.101</a></td><td>53281</td><td><a href="/address/5be05ouJ5Zyt.html">巴拉圭</a>&nbsp;<a href="/address/5be05ouJ5Zyt.html">巴拉圭</a>&nbsp;</td><td><a href="/isp/Y29wYWNvLmNvbS5weQ==.html">copaco.com.py</a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>38.13秒</td><td>4小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MTU3LjI0NS45MC4zNzo4MDgw" target="_blank"><img src="/flag/US.svg">157.245.90.37</a></td><td>8080</td><td><a href="/address/576O5Zu9.html">美国</a>&nbsp;<a href="/address/5L+E5YuS5YaI5bee.html">俄勒冈州</a>&nbsp;<a href="/address/5bCk6YeR.html">尤金</a>&nbsp;</td><td><a href="/isp/.html"></a></td><td>支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>0.75秒</td><td>3天前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MTE2LjIwNC4xNTIuMTEwOjgwODA=" target="_blank"><img src="/flag/BD.svg">116.204.152.110</a></td><td>8080</td><td><a href="/address/5a2f5Yqg5ouJ.html">孟加拉</a>&nbsp;<a href="/address/5a2f5Yqg5ouJ.html">孟加拉</a>&nbsp;</td><td><a href="/isp/.html"></a></td><td>不支持</td><td>不支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>2.29秒</td><td>1小时前</td><td>17秒前</td></tr><tr><td><a href="/check.html?proxy=MzkuMTM3LjY5Ljc6ODA=" target="_blank"><img src="/flag/CN.svg">39.137.69.7</a></td><td>80</td><td><a href="/address/5Lit5Zu9.html">中国</a>&nbsp;<a href="/address/5aSp5rSl.html">天津</a>&nbsp;<a href="/address/5aSp5rSl.html">天津</a>&nbsp;</td><td><a href="/isp/56e75Yqo.html">移动</a></td><td>不支持</td><td>支持</td><td><a href="/anonymity/2.html">高匿</a></td><td>0.09秒</td><td>24小时前</td><td>17秒前</td></tr></tbody>'
    main(str)

