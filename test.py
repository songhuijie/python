# -*- coding: utf-8 -*

import requests
import MySQLdb
from bs4 import BeautifulSoup
import time
import re
import logging
import redis
import json
import math
from googletrans import Translator
import time
import get_one_proxy

wei_bo_key = 'wei_bo_key'
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
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1


def getData():
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='hubtraffic',  # DB name
        charset="utf8"
    )
    cur = conn2db.cursor()
    sql = "SELECT `id`,`cate_name`,`cate_id` FROM `cate`  where is_handle = 0 order by id desc limit 100,1"
    cur.execute(sql)
    db_result = cur.fetchone()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result

def getCount(cate_id):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='hubtraffic',  # DB name
        charset="utf8"
    )
    cur = conn2db.cursor()
    sql = "SELECT count(`id`) FROM `xvideo`  where cate_id = %s limit 1" % (cate_id)
    cur.execute(sql)
    db_result = cur.fetchone()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result

def updateData(id):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='hubtraffic',  # DB name
        charset="utf8"
    )
    cur = conn2db.cursor()
    sql = "update cate set is_handle = 1 Where id = %s" % (id)

    try:

        cur.execute(sql)  # 执行sql语句
        conn2db.commit()  # 提交到数据库执行
        print(sql)
        print('更新成功')
    except:
        print('更新失败')
        print(id)
        print(sql)
        conn2db.rollback()  # 发生错误后回滚

    cur.close()
    conn2db.close()
    return 'true'

def insertXvideo(data):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='hubtraffic',  # DB name
        charset="utf8"
    )

    cur = conn2db.cursor()
    sql = "INSERT INTO `xvideo` ( `video_id`,`video_access_address`,`video_title`,`video_title_ja`,`video_duration`,`video_cover`,`video_tag`,`views`,`cate_id`,`insert_time`) VALUES "


    for value in range(len(data)):

        sql += ' ("' + str(data[value][0]) + '","' + str(data[value][1]) + '","' + str(data[value][2]) + '","' + str(data[value][3]) + '", "' + str(data[value][4]) + '","' + str(data[value][5]) + '","' + str(data[value][6]) + '","' + str(data[value][7]) + '", "' + str(data[value][8]) + '", "' + str(data[value][9]) + '")'

        if value == int(len(data)) - 1:
            sql += ';'
        else:
            sql += ','

    try:
        cur.execute(sql)
        conn2db.commit()
    except Exception as e:
        print(e)
        print(sql)
        print('插入错误')

    cur.close()
    conn2db.close()
    return 'true'


def RecordLog(msg):
    callfile = '/var/own_project/python/log/hubtraffic.log'
    logging.basicConfig(filename=callfile, filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    logging.info(msg)

    return True

def HandlePage(count):
    page = math.ceil(count / 20) + 1
    return page

def HandleDuration(duration):
    data = duration.split(':', 1)
    return int(data[0]) * 60 + int(data[1])

def returnTranslator():
    proxy_ip = get_one_proxy.getNeedProxy()
    # proxy_ip = get_one_proxy.changeProxy()
    proxy = {'https': ''}
    print(proxy_ip)
    proxy['https'] = proxy_ip
    translator = Translator(proxies=proxy, timeout=5)
    # translator = Translator(timeout=5)
    try:
        text = translator.translate('Big black', dest='ja').text
        print(text)
        return translator
    except Exception as e:
        return False

def returnTranslatorIp(proxy_ip):
    proxy = {'https': ''}
    proxy['https'] = proxy_ip
    translator = Translator(proxies=proxy, timeout=5)
    try:
        text = translator.translate('Big black', dest='ja').text
        print(text)
        return translator
    except Exception as e:
        return False

if __name__ == '__main__':

    cate = getData()
    id = cate[0]
    cate_name = cate[1]
    cate_id = cate[2]
    count = getCount(cate_id)
    translator = returnTranslator()
    if translator == False:
        proxy_ip = get_one_proxy.changeProxy()
        translator = returnTranslatorIp(proxy_ip)
        if translator == False:
            exit()

    count = HandlePage(count[0])
    url = "https://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search=%s&tags[]=Teen&thumbsize=medium&page=%s" % (cate_name,count)
    result = reqPage(url)


    try:
        list = json.loads(result)

        finally_data = []
        if list['videos']:
            for value in list['videos']:
                own_data = []
                own_value = value['video']
                own_data.append(own_value['video_id'])
                own_data.append(own_value['url'])

                own_data.append(own_value['title'].replace("[\\x{10000}-\\x{10FFFF}]",'').replace('"','').replace('💋', ''))
                try:
                    own_data.append(translator.translate(own_value['title'].replace('&', '').replace('#', '').replace('/', '').replace('💋', '').replace('"','').replace("[\\x{10000}-\\x{10FFFF}]",''), dest='ja').text)
                except Exception as e:
                    RecordLog('google 翻译失败')
                    exit()

                own_data.append(HandleDuration(own_value['duration']))
                own_data.append(own_value['default_thumb'])
                own_d = []
                for val in own_value['tags']:
                    own_d.append(val['tag_name'])

                own_data.append(','.join(own_d))
                own_data.append(own_value['views'])
                own_data.append(cate_id)
                own_data.append(int(time.time()))
                finally_data.append(own_data)


            insertXvideo(finally_data)
            print('完成')
            RecordLog('插入成功')
        else:
            print('没有数据 更新')
            RecordLog('没有数据 更新')
            updateData(id)


    except Exception as e:
        print(e)
        RecordLog(e)
        print('错误')
        exit()