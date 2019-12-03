# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import csv
import re

proxies = {
    # "http": "http://178.79.46.5:59073"
    "http": "http://111.13.134.22:80"
}

def GetListOfSingers(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理


                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url,  proxies=proxies)
                # req = requests.get(url, headers=headers)
                # req = requests.get(url)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                # if req.status_code == 200:
                    # 返回BeautifulSoup对象
                return BeautifulSoup(req.text, 'html5lib')
                # return req.text
        except:
            pass
        time.sleep(3)
        num += 1


def handleCover(soup):

    covers_array = soup.select('img[class^="channel-header-profile-image"]')
    # covers_array = soup.find('yt-img-shadow[id^="avatar"]')
    # tag = soup.find('div', attrs={'class': 'pl-header-thumb'})

    covers = len(covers_array)
    if covers >= 1:
        for i in range(covers):
            if i == 0:
                return covers_array[i].get('src')
            else:
                return False
    else:
        return False

def getData():
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )
    cur = conn2db.cursor()
    sql = "SELECT `id`,`song_lists` FROM `singer_list` WHERE `cover_status` = 0 and `song_lists` != '' limit 200"
    cur.execute(sql)
    db_result = cur.fetchall()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result

def updateData(id,cover):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )
    cur = conn2db.cursor()
    sql_update = "UPDATE `singer_list` SET `cover` = '%s',`cover_status` = 1 WHERE `id` = '%s'" % (cover,id)
    try:
        # 执行SQL语句
        cur.execute(sql_update)
        # 提交到数据库执行
        conn2db.commit()
        print(1)
    except:
        # 发生错误时回滚
        conn2db.rollback()
        print(conn2db.error)
    # 关闭数据库连接
    conn2db.close()

    return True

if __name__ == '__main__':

    result = getData()

    for value in result:
        time.sleep(60)
        soup = GetListOfSingers(value[1])
        covers_result = handleCover(soup)
        if covers_result == False:
            print('end')
            continue
        else:
            print(value[0],covers_result)
            updateData(value[0],covers_result)

    print('success')
    exit()

