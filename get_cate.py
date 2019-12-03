import requests
import MySQLdb
from bs4 import BeautifulSoup
import time
import redis
import json
import random
from googletrans import Translator
import get_one_proxy

offset=5000
limit=1000

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',

}

proxies = {
    "https": "https://117.239.38.81:50376"
}
redis_key = 'xvideo_key'

url = 'https://www.xvideos.com'

def reqPage(url,cookie,proxy):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers,proxies = proxy,timeout=5,cookies = cookie)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def reqPostPage(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    cookies = req.cookies.get_dict()
                    return cookies
        except:
            pass
        time.sleep(3)
        num += 1


def handleCate(soup):
    # list = soup.select('li[class^="sub-list"]')
    lists = soup.find_all('li',{'class':'dyn'})
    covers = len(lists)

    data_array = []
    if covers >= 1:

        for i in range(covers):
            array = []
            # print(lists[i].get_text())
            array.append(url + lists[i].find('a').get('href'))
            array.append(lists[i].get_text().strip())
            array.append(i+1)
            data_array.append(array)
    else:
        return False

    return data_array


def saveData(data,uid):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )

    cur = conn2db.cursor()
    sql = "INSERT INTO `cate_zh` ( `cate_url`,`cate_name`,`cate_id`,`is_recommend`) VALUES "


    for value in range(len(data)):
        sql += " ('" + data[value][0] + "','" + data[value][1] +"', "+ str(data[value][2]) +"," + str(uid) +")"
        if value == int(len(data)) - 1 :
            sql+= ';'
        else:
            sql+= ','


    # print(sql)
    # exit()
    cur.execute(sql)
    conn2db.commit()
    cur.close()
    conn2db.close()
    return 'true'

def getData():
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )
    cur = conn2db.cursor()
    sql = "SELECT `id`,`video_title` FROM `xvideo`  where insert_time > 1 and video_title_en is null order By id desc limit %s,%s" % (
        offset, limit)
    cur.execute(sql)
    db_result = cur.fetchall()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result


def updateData(data):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"

    )

    cur = conn2db.cursor()
    sql = 'UPDATE  `xvideo`  set `video_title_en` = "%s"  where id = "%s"'% (data[0],data[1])

    # exit()

    try:
        cur.execute(sql)  # 执行sql语句
        conn2db.commit()  # 提交到数据库执行
        print('更新成功')
    except Exception as e:
        print('更新失败')
        conn2db.rollback()  # 发生错误后回滚

    cur.close()
    conn2db.close()
    return 'true'



def HandleLanguageJA():
    print('s')


def isAllJa(s):
    '包含汉字的返回TRUE'
    for c in s:
        if '\u0800' <= c <= '\u4e00':
            print(c)
            return 1
    return 0




def returnTranslator():
    proxy_ip = get_one_proxy.getNeedProxy()
    proxy = {'https': ''}
    print(proxy_ip)
    proxy['https'] = proxy_ip
    # translator = Translator(proxies=proxy, timeout=5)
    translator = Translator(timeout=5)

    return translator


def baiduTranslator(content):

    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'
    q = content
    fromLang = 'zh'  # 源语言
    toLang = 'jp'  # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey

if __name__ == '__main__':

    # 谷歌翻译 库





    # translator = Translator()

    # str = '☆無料動画☆【超鮮明】☆巨乳の優樹菜ﾁｬﾝ・・エッチだけでは物足りず？？☆'
    # print(translator.translate(str,dest='ja').text)
    # exit()

    # url2 = 'https://www.xvideos.com/change-language/ja?no_redirect=1'
    # url2 = 'https://www.xvideos.com/change-language/en?no_redirect=1'
    # cookie = reqPostPage(url2)
    # print(cookie)


    translator = returnTranslator()

    data = getData()
    count = 0
    for k in data:
        time.sleep(5)
        own_data = []
        try:
            own_str = translator.translate(k[1].replace('&','').replace('#',''),dest='en').text
            own_data.append(own_str)
            own_data.append(k[0])
            updateData(own_data)
            count += 1
            print("成功%s次"%(count))
        except Exception as e:
            print(k[1])
            get_one_proxy.changeProxy()
            # own_data.append(k[1])
            # own_data.append(k[0])
            # updateData(own_data)
            print('失败 切换代理 执行下次')
            print(k[0])
            continue


    print('success')
    exit()


    # for k in data:
    #     own_data = []
    #
    #     proxy_ip = getNeedProxy()
    #     proxy = {'https': ''}
    #     print(proxy_ip)
    #     proxy['https'] = proxy_ip
    #
    #     time.sleep(3)
    #     print(k[0])
    #     soup = reqPage(k[1], cookie ,proxy)
    #     print(soup)
    #     if soup == None:
    #         changeProxy()
    #         continue
    #     title = soup.find('h2', {'class': 'page-title'})
    #     language_content = ''
    #     for i, child in enumerate(title.contents):
    #         if i == 0:
    #             language_content = child
    #
    #     bool = isAllJa(language_content.replace('一','').replace('"',''))
    #
    #     own_data.append(language_content.replace('"',''))
    #     own_data.append(bool)
    #     own_data.append(k[0])
    #     print(own_data)
    #     updateData(own_data)

    print('success')
    exit()



