# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import csv
import logging
from urllib import request
from urllib import parse
import ssl
import re
import os
from collections import OrderedDict
import math
import execjs
import json
import datetime
import pymysql
import sys

ssl._create_default_https_context = ssl._create_unverified_context
__path__ = '/var/www/html/fangcms/Uploads/datas/images/property/'
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

__root_path__ = '/var/www/html/python/fang/'

f = open(r'/var/www/html/python/fang/house.txt', 'r')  # 打开所保存的cookies内容文件
cookies = {}  # 初始化cookies字典变量
for line in f.read().split(';'):  # 按照字符：进行划分读取
    # 其设置为1就会把字符串拆分成2份
    name, value = line.strip().split('=', 1)
    cookies[name] = value


def copyInfo(url):
    r = requests.get(url, headers=headers)  # 最基本的GET请求

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html5lib')
        price = soup.find('p', class_="content__aside--title")

        price = price.get_text()

        imgs = soup.find('div', class_="content__thumb--box")
        listimg = imgs.find_all('img')
        lenth = len(listimg)
        img = []
        for i in range(lenth):
            img.append(listimg[i].attrs['src'])
        img = ",".join(img)

        asides = soup.find('p', class_="content__aside--tags")
        listasides = asides.select('i[class^="content__item__tag"]')
        arr = []
        for aside in listasides:
            arr.append(aside.get_text())
        aside = ",".join(arr)

        houses = soup.find('p', class_="content__article__table")
        housesides = houses.select('span')
        housearr = []
        for i, h in housesides:
            housearr.append(h)

        infos = soup.find('div', class_="content__article__info")
        listinfos = infos.select('li[class^="fl oneline"]')
        info = []
        for value in listinfos:
            info.append(value.get_text())
        info = ",".join(info)

        data = []
        data.append(img)
        data.append(price)
        data.append(aside)
        data.append(housearr[0])
        data.append(housearr[1])
        data.append(housearr[2])
        data.append(housearr[3])
        data.append(info)
        return data

    else:
        print(1)
        exit()


def saveData(data):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )

    cur = conn2db.cursor()
    sql = "INSERT INTO `house` ( `imgs`, `price`,`types`,`houser`, `tpe`, `area`,`north`,`info`) VALUES (\
            '%s','%s','%s','%s','%s','%s','%s','%s')" % (
        data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])

    cur.execute(sql)
    conn2db.commit()
    cur.close()
    conn2db.close()

    return 'true'


def saveHouseing(data, ids):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )

    cur = conn2db.cursor()

    for value in data:
        if ids.get(value) == None:
            type = 1
        else:
            type = ids.get(value)

        sql = "INSERT INTO `housing_information` ( `id`,`type`, `imgs`,`own_imgs`,`property`,`location`, `traffic`, `sell_price`,`surface`,`annual_income`,`building`,`rank`,`construction`,`building_area`,`interception`,`total`,`parking`,`land_area`,`land_rights`,`area_burden`,`ground`,`city_plan`,`application_area`,`building_coverage`,`volumetric`,`national_law`,`contact_situation`,`present_situation`,`delivery`,`schedulel_date`,`renewal_date`,`building_number`,`management_number`,`notes`,`transaction`) VALUES (\'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            value, type, data[value][1], disposeImg(data[value][1], value), data[value][2], data[value][3],
            data[value][4], data[value][5], data[value][6], data[value][7], data[value][8], data[value][9],
            data[value][10], data[value][11], data[value][12], data[value][13], data[value][14], data[value][15],
            data[value][16], data[value][17], data[value][18], data[value][19], data[value][20], data[value][21],
            data[value][22], data[value][23], data[value][24], data[value][25], data[value][26],
            int(time.mktime(time.strptime(data[value][27], "%Y/%m/%d"))),
            int(time.mktime(time.strptime(data[value][28], "%Y/%m/%d"))), data[value][29], data[value][30],
            data[value][31], data[value][32])
        cur.execute(sql)

    conn2db.commit()
    cur.close()
    conn2db.close()

    return 'true'


def saveHouseingZh(data, ids, money1, money2, address):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )

    cur = conn2db.cursor()

    for value in data:
        if ids.get(value) == None:
            type = 1
        else:
            type = ids.get(value)
        money_jp = money1.get(value)
        money_zh = money2.get(value)
        addr = address.get(value)

        sql = "INSERT INTO `housing_information_zh` ( `id`,`type`, `imgs`,`own_imgs`,`property`,`location`, `traffic`,`price_jp`,`price_zh`,`sell_price`,`surface`,`annual_income`,`building`,`rank`,`construction`,`building_area`,`interception`,`total`,`parking`,`land_area`,`land_rights`,`area_burden`,`ground`,`city_plan`,`application_area`,`building_coverage`,`volumetric`,`national_law`,`contact_situation`,`present_situation`,`delivery`,`schedulel_date`,`renewal_date`,`building_number`,`management_number`,`notes`,`transaction`) VALUES (\'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            value, type, data[value][1], disposeImg(data[value][1], value), data[value][2], addr, data[value][4],
            money_jp, money_zh, data[value][5], data[value][6], data[value][7], data[value][8], data[value][9],
            data[value][10], data[value][11], data[value][12], data[value][13], data[value][14], data[value][15],
            data[value][16], data[value][17], data[value][18], data[value][19], data[value][20], data[value][21],
            data[value][22], data[value][23], data[value][24], data[value][25], data[value][26],
            int(time.mktime(time.strptime(data[value][27], "%Y/%m/%d"))),
            int(time.mktime(time.strptime(data[value][28], "%Y/%m/%d"))), data[value][29], data[value][30],
            data[value][31], data[value][32])
        cur.execute(sql)

    conn2db.commit()
    cur.close()
    conn2db.close()

    return 'true'




def saveCsv(type, data):
    # 添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/rakumachi.csv", "w", newline="") as datacsv:
    # 追加
    file_name = __root_path__ + "rakumachigenres.csv"
    with open(file_name, "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp = []

        for value in data:
            for i in data:
                row = []
                row.append(value)
                row.append(type)
                row.append(data[value])
            tmp.append(row)

        csvwriter.writerows(tmp)
    return 'true'


def saveSourceCsv(type, data):
    # 添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/rakumachigenres.csv", "a", newline="") as datacsv:
    # 追加
    with open("/Applications/MAMP/htdocs/htdocs/python/rakumachigenre.csv", "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp = []

        for value in data:
            for i in data:
                row = []
                row.append(value)
                row.append(type)
                row.append(data[value])
            tmp.append(row)

        csvwriter.writerows(tmp)
    return 'true'


def reqPage(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理

                req = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
                # req = requests.get(url, headers=headers,cookies = cookies)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1


def reqPages(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理

                req = requests.get(url, headers=headers)
                # req = requests.get(url, headers=headers,cookies = cookies)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1


def RecordLog(msg):
    callfile = '/Applications/MAMP/htdocs/htdocs/python/house.log'
    logging.basicConfig(filename=callfile, filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    logging.info(msg)

    return True


def HandleHtml(soup, data, next_url=''):
    listurls = soup.select('div[class^="propertyBlock__mainArea"]')

    if len(listurls) == 0:
        # RecordLog(next_url)
        return data
    else:
        for list in listurls:
            data[list.get('onclick').split('\'')[1].split('/')[5]] = url_index + list.get('onclick').split('\'')[1]
        return data


def HandleHtmlSupply(soup, data, next_url='', own_id=''):
    listurls = soup.select('div[class^="propertyBlock__mainArea"]')

    if len(listurls) == 0:
        # RecordLog(next_url)
        return data
    else:
        for lists in listurls:
            if int(lists.get('onclick').split('\'')[1].split('/')[5]) > int(own_id):
                data[lists.get('onclick').split('\'')[1].split('/')[5]] = url_index + lists.get('onclick').split('\'')[
                    1]
                # print(lists.get('onclick').split('\'')[1].split('/')[5])
            else:
                break
        return data


def NextPage(soup):
    page = 0
    links = soup.select('li[class^="next"]')
    if len(links) != 0:
        for value in links:
            page = url_area + value.find('a').get('href')

    return page


def SaveCsv(data, id):
    # with open("/Applications/MAMP/htdocs/htdocs/python/ids.csv", "w", newline="") as datacsv:
    with open("/Applications/MAMP/htdocs/htdocs/python/ids.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # csvwriter.writerow(["house_id", "图片","物件名","所在地","沿線交通","販売価格","表面利回り表面利回り","想定年間収入想定年間収入","建物構造建物構造","階数階数","築年月","建物面積","間取り","総戸数総戸数","駐車場駐車場","土地面積","土地権利土地権利","私道負担面積","地目地目","都市計画区域都市計画区域","用途地域用途地域","建ぺい率建ぺい率","容積率容積率","国土法届出国土法届出","接道状況接道状況","現況現況","引渡し引渡し","次回更新予定日","更新日","建築確認番号","管理番号","注意事項","取引態様"])
        datas = []

        for value in data:
            for i in data:
                tmp = []
                tmp.append(value)
                tmp.append(id)
            datas.append(tmp)
        csvwriter.writerows(datas)
    return 'true'


def SaveNext(data):
    file_name = __root_path__ + 'next.csv'
    with open(file_name, "w", newline="") as datacsv:
        # with open("/Applications/MAMP/htdocs/htdocs/python/ids.csv", "a", newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerows(data)
    return 'true'


def SaveMoneyCsv(datas):
    with open("/Applications/MAMP/htdocs/htdocs/python/moneys.csv", "w", newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerows(datas)
    return 'true'


def SaveAddressCsv(datas):
    with open("/Applications/MAMP/htdocs/htdocs/python/address.csv", "w", newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerows(datas)
    return 'true'


def getArea(soup, data):
    listurls = soup.select('input[class^="listCheckbox"]')

    for value in listurls:
        data.append(value.get('value'))

    return data


def handleids(url, value):
    tmp = []
    soup = reqPage(url)
    data = getArea(soup, tmp)
    own_url = NextPage(soup)

    if own_url == 0:
        pass
    else:
        next_url = own_url
        while (next_url):
            time.sleep(3)
            getArea(reqPage(next_url), data)
            next_url = NextPage(reqPage(next_url))

    SaveCsv(data, value)
    return True


def ReadCsv(min, max, filename=None, type=1):
    if filename == None:
        f = '/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv'
    else:
        f = filename
    csvFile = open(f, "r")
    reader = csv.reader(csvFile)
    min = int(min) + 1
    # 建立空字典
    result = {}

    for item in reader:
        # 忽略第一行
        if reader.line_num < min:
            continue
        elif reader.line_num > max:
            continue
        else:
            if type == 1:
                result[item[0]] = item
            elif type == 2:
                result[item[0]] = item[5]
            elif type == 3:
                result[item[0]] = item[2]
            elif type == 4:
                result[item[0]] = item[1]
            else:
                result[item[0]] = item[1]
    csvFile.close()

    return result


def handleAddress(string):
    own_string = string.replace('地図を見る', '')
    return own_string


def UpdateFang():
    ids = [26101, 26102, 26103, 26104, 26105, 26106, 26107, 26108, 26109, 26110, 26111, 27102, 27103, 27104, 27106,
           27107, 27108, 27109, 27111, 27113, 27114, 27115, 27116, 27117, 27118, 27119, 27120, 27121, 27122, 27123,
           27124, 27125, 27126, 27127, 27128, 28101, 28105, 28106, 28107, 28108, 28109, 28110, 28111]
    file_name = __root_path__ + 'next.csv'

    result = ReadCsv(0, 50, file_name, 5)
    nexts = []
    rakumach = []
    for value in ids:
        time.sleep(2)
        test_url = 'https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?limit=60&area[]=%s&newly=&price_from=&price_to=&gross_from=&gross_to=&dim[]=1001&dim[]=1002&dim[]=1003&dim[]=1004&dim[]=1005&year=&b_area_from=&b_area_to=&houses_ge=&houses_le=&min=&l_area_from=&l_area_to=&keyword=&ex_real_search=&sort=property_created_at&sort_type=desc' % (
            value)
        data = {}
        soup = reqPage(test_url)
        data = HandleHtmlSupply(soup, data, test_url, result.get(str(value)))
        # data = HandleHtmlSupply(soup,data,test_url,1575453)
        tmp = []
        if len(data) < 20:
            tmp.append(value)
            if len(data) == 0:
                tmp.append(result.get(str(value)))
            else:

                tmp.append(next(iter(OrderedDict(data))))
            nexts.append(tmp)
            next_url = False
        else:
            next_url = NextPage(soup)

        saveCsv(value, data)
    SaveNext(nexts)

    return True


def updateSource():
    dims = [1001, 1002, 1003, 1004, 1005]
    file_name = 'source.csv'

    source = ReadCsv(0, 50, file_name, 5)

    for value in dims:
        test_url = 'https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?limit=60&area[]=26104&area[]=26105&area[]=26106&area[]=26107&area[]=26108&area[]=26109&area[]=26110&area[]=26111&area[]=27102&area[]=27103&area[]=27104&area[]=27106&area[]=27107&area[]=27108&area[]=27109&area[]=27111&area[]=27113&area[]=27114&area[]=27115&area[]=27116&area[]=27117&area[]=27118&area[]=27119&area[]=27120&area[]=27121&area[]=27122&area[]=27123&area[]=27124&area[]=27125&area[]=27126&area[]=27127&area[]=27128&area[]=28101&area[]=28105&area[]=28106&area[]=28107&area[]=28108&area[]=28109&area[]=28110&area[]=28111&newly=&price_from=&price_to=&gross_from=&gross_to=&dim[]=%s&year=&b_area_from=&b_area_to=&houses_ge=&houses_le=&min=&l_area_from=&l_area_to=&keyword=&ex_real_search=&sort=property_created_at&sort_type=desc' % (
        value)
        data = {}
        soup = reqPage(test_url)
        data = HandleHtml(soup, data, test_url)

        own_url = NextPage(soup)

        time.sleep(30)
        saveCsv(value, data)
    return True


def ReadchunkCsv(min, max, filename=None):
    if filename == None:
        f = 'rakumachi.csv'
    else:
        f = filename
    csvFile = open(f, "r")
    reader = csv.reader(csvFile)
    min = int(min) + 1
    # 建立空字典
    result = {}
    for item in reader:
        # 忽略第一行
        if reader.line_num < min:
            continue
        elif reader.line_num > max:
            continue
        else:
            result[item[0]] = item
    csvFile.close()

    return result


def Own_HandleHtml(soup, id, type_id, source):
    tmp = []

    if soup == None:
        return tmp
    else:
        tmp.append(id)
        tmp.append(type_id)
        tmp.append(source)
        tmp = HandleImg(soup, tmp, id)
        info = soup.find('table', class_="Effect03")
        listinfo = info.select('td')

        for value in range(len(listinfo)):
            # tmp.append(value.get_text())
            tmp.append("".join(listinfo[value].get_text().replace('\n', '').split()))
        return tmp


def ClearFang():
    filename = __root_path__ + 'fangyuanInfoUpdate.csv'
    csvFile = open(filename, "w")
    csvFile.truncate()
    return True


def GetInfo():
    filename = __root_path__ + 'rakumachigenres.csv'
    result = ReadchunkCsv(0, 500, filename)
    if len(result) == 0:
        ClearFang()
        return True
    else:
        tmp = []
        for value in result:
            time.sleep(2)

            data = Own_HandleHtml(reqPage(result[value][2]), result[value][0], result[value][1],
                                  handleSource(result[value][2]))

            if len(data) != 0:
                tmp.append(data)

            SaveCsvFangInfo(tmp)
        return True


def HandleImg(soup, tmps, id):
    imgs = ''
    img = soup.find('div', class_='photoRight')
    if img == None or len(img) == 0:
        tmps.append(imgs)
        return tmps
    listimg = img.select('img')
    tmp = []
    for value in range(len(listimg)):
        ir = requests.get(url_index + listimg[value].get('src'))
        if ir.status_code == 200:
            if os.path.isdir(__path__ + id + '/') == False:
                os.mkdir(__path__ + id + '/')
            file_path = __path__ + id + '/'
            open(file_path + listimg[value].get('src')[listimg[value].get('src').rindex("/") + 1:], 'wb').write(
                ir.content)
        tmp.append(url_index + listimg[value].get('src'))

    imgs = ";".join(tmp)
    tmps.append(imgs)

    return tmps


def handleSource(string):
    own_source = string.split('/')
    sources = {'dim1001': 1, 'dim1002': 2, 'dim1003': 3, 'dim1004': 4, 'dim1005': 5}

    if sources.get(own_source[6]) == None:
        source = 1
    else:
        source = sources.get(own_source[6])

    return source


def SaveCsvFangInfo(data):
    # with open("/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv", "w", newline="") as datacsv:
    file_name = __root_path__ + "fangyuanInfoUpdate.csv"
    with open(file_name, "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # csvwriter.writerow(["id", "图片","物件名","所在地","沿線交通","販売価格","表面利回り表面利回り","想定年間収入想定年間収入","建物構造建物構造","階数階数","築年月","建物面積","間取り","総戸数総戸数","駐車場駐車場","土地面積","土地権利土地権利","私道負担面積","地目地目","都市計画区域都市計画区域","用途地域用途地域","建ぺい率建ぺい率","容積率容積率","国土法届出国土法届出","接道状況接道状況","現況現況","引渡し引渡し","次回更新予定日","更新日","建築確認番号","管理番号","注意事項","取引態様"])
        tmp = []

        # for value in data:
        #     for i in data:
        #         row = []
        #         print(data)
        #         print(value)
        #         exit()
        #         row.append(value)
        #         row.append(data[value])
        #     tmp.append(row)

        # csvwriter.writerow(data)
        csvwriter.writerows(data)
    return 'true'

###################翻译部分
class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


# 处理 多图片
def disposeImg(imgs, id):
    if imgs:
        array = imgs.split(';')

        file_path = '/Uploads/datas/images/property/'
        tmp = []

        for value in array:
            test = {}
            test["img"] = file_path + id + '/' + value[value.rindex("/") + 1:]
            test["alt"] = value[value.rindex("/") + 1:]
            tmp.append(test)

        own_tmp = str(tmp)
        own_img = own_tmp.replace('\'', '\"')
    else:
        own_img = ''
        msg = id + '暂无图片'

    return own_img


# 处理 图片页面
def disImg(imgs, id):
    if imgs:
        array = imgs.split(';')

        file_path = '/Uploads/datas/images/property/'

        tmp = file_path + id + '/' + array[0][array[0].rindex("/") + 1:]

        own_img = str(tmp)
    else:
        own_img = ''
        msg = id + '暂无图片'

    return own_img


# 处理 价钱
def handleMoney(string):
    string = string.replace('億円', '0000')
    own_string = re.findall(r"\d+\.?\d*", string)

    need = ''
    for value in own_string:
        need += value

    return int(need)


# 处理 房间平方
def handleArea(string):
    own_string = re.findall(r"\d+\.?\d*", string)
    if len(own_string) == 0:
        return 0
    else:
        return int(float(own_string[0]))


# 处理 总平方
def handlebuild(string):
    default_build = 191
    types = {'SRC建设': 186, 'RC建设': 187, '钢架': 188, '轻质钢架': 189, '木': 190, '其他': 191}

    result = types.get(string)
    if result == None:
        return default_build
    else:
        return result


# 处理 年限
def handleyear(string):
    a = "192,本年,193,5,194,10,195,15,196,20,197,25,198,30,199,35"
    own_string = re.findall(r"\d+\.?\d*", string)
    now_year = datetime.datetime.now().year

    cha = now_year - int(own_string[0])

    if cha == 1:
        return 192
    elif cha > 1 and cha <= 5:
        return 193
    elif cha > 5 and cha <= 10:
        return 194
    elif cha > 10 and cha <= 15:
        return 195
    elif cha > 15 and cha <= 20:
        return 196
    elif cha > 20 and cha <= 25:
        return 197
    elif cha > 25 and cha <= 30:
        return 198
    elif cha > 30:
        return 199
    else:
        return 192


# 处理 层数
def handlefloors(string):
    a = '212,1-2,213,2-4,214,4-6,215,6-8,216,8'
    own_string = re.findall(r"\d+\.?\d*", string)
    if len(own_string) == 0:
        return 212
    else:
        floor = int(own_string[0])
        if floor > 0 and floor <= 2:
            return 212
        elif floor > 2 and floor <= 4:
            return 213
        elif floor > 4 and floor <= 6:
            return 214
        elif floor > 6 and floor <= 8:
            return 215
        elif floor > 8:
            return 216


# 处理 户数
def handlefamily(string):
    a = '217,1-2,218,2-4,219,4-6,220,6-8,221,8'
    own_string = re.findall(r"\d+\.?\d*", string)

    if len(own_string) == 0:
        return 217
    else:
        family = int(own_string[0])
        if family > 0 and family <= 2:
            return 217
        elif family > 2 and family <= 4:
            return 218
        elif family > 4 and family <= 6:
            return 219
        elif family > 6 and family <= 8:
            return 220
        elif family > 8:
            return 221


# 处理 年
def handleconstruction(string):
    tmp = string.split('（')
    return tmp[0]


# 处理 利率
def handleNianHua(string):
    own_string = re.findall(r"\d+\.?\d*", string)

    if len(own_string) == 0:
        return 0
    else:
        return math.ceil(float(own_string[0]) * 100)


# 处理 均价
def handleAverage(price, area):
    if area == 0:
        return 0
    else:
        average_price = int(price) / int(area)
        return int(round(average_price, 1) * 10000)


# 处理 翻译问题
def googleTranslate(url):
    time.sleep(1)
    # proxy = 'http://178.79.46.5:59073'

    proxy_support = request.ProxyHandler({'http': proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    req = request.Request(url, headers=headers)
    data = request.urlopen(req)
    html = data.read().decode("utf-8")
    needs = html.split(',')[0].split('"')
    need = needs[1]
    return need


# 批量 处理翻译
def googleTranslateTwo(url, datas, tmp2):
    time.sleep(1)
    # proxy = 'http://178.79.46.5:59073'
    proxy = "http://87.228.103.111:8080"
    proxy_support = request.ProxyHandler({'http': proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    req = request.Request(url, headers=headers)
    data = request.urlopen(req)
    html = data.read().decode("utf-8")

    needs = json.loads(html)
    # for value in needs[0]


    for value in range(len(needs[0])):

        if tmp2.get(value) == None:
            pass
        else:
            datas[tmp2[value]] = needs[0][value][0].replace("\n", "")

    return datas


# 请求获取 批量翻译文字
def HandleUrltwo(data):
    tmp = []
    need = {0: 1, 1: 1, 2: 1, 3: 1, 5: 1, 8: 1, 11: 1, 12: 1, 13: 1, 15: 1, 18: 1, 23: 1, 24: 1, 29: 1, 30: 1, 31: 1}
    # need = [0,1,6,9,11,14,17,21,22,27,28,30]
    # 添加  价格日币  价格人民币  利率  土地面积  全部面积 户数id  层数id  建造材料  建筑年限 均价 利率
    for value in range(len(data)):
        if need.get(value):
            pass
        else:
            if data[value] == '':
                pass
            else:
                tmp.append(value)

    tmp2 = {}
    for value in range(len(tmp)):
        tmp2[value] = tmp[value]

    content = ''
    for value in range(len(tmp)):
        if value == len(tmp) - 1:
            content += data[tmp[value]]
        else:
            content += data[tmp[value]].replace('〓', '').replace('！', '').replace('！', '').replace('【', '').replace('】',
                                                                                                                    '').replace(
                '。', '') + "\n"

    area = handleArea(data[13])
    price_jp = handleMoney(data[7])
    price_zh = math.ceil(handleMoney(data[7]) / 16.27)
    data.append(price_jp)
    data.append(price_zh)
    data.append(area)
    data.append(handleArea(data[17]))
    data.append(handleArea(data[15]))
    data.append(disposeImg(data[3], data[0]))
    data.append(disImg(data[3], data[0]))
    data.append(handlebuild(data[10]))
    data.append(handleyear(data[12]))
    data.append(handlefloors(data[11]))
    data.append(handlefamily(data[15]))
    data.append(handleconstruction(data[12]))
    data.append(handleNianHua(data[8]))

    data.append(handleAverage(price_zh, area))
    data[5] = data[5].replace('地図を見る', '')

    js = Py4Js()
    tk = js.getTk(content)
    if len(content) > 4891:
        # print("翻译的长度超过限制！！！")
        return ''

    content = parse.quote(content)

    url = "https://translate.google.cn/translate_a/single?client=webapp&sl=ja&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (
    tk, content)

    return googleTranslateTwo(url, data, tmp2)

# 存储到数据库
def SaveFangData(data):
    conn2db = pymysql.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='instagram@web.',  # 密码
        db='fangcms',  # DB name
    )
    cur = conn2db.cursor()

    error_log = __root_path__ + 'fang_error.log'
    logging.basicConfig(filename=error_log, level=logging.INFO)

    for value in data:

        sql = 'INSERT INTO `yk_used` ( `id`,`area_id`,`title`, `address`,`map`,`area`,`build_area`,`total_floor`,`file`,`img`,`status`,`source`,`build`,`year`,`floors`,`family`,`traffic`,`location`,`price_jp`,`price_zh`,`average_price`,`surface`,`surface_s`,`annual_income`,`building`,`rank`,`construction`,`interception`,`parking`,`land_rights`,`area_burden`,`ground`,`city_plan`,`application_area`,`building_coverage`,`volumetric`,`national_law`,`contact_situation`,`present_situation`,`delivery`,`schedulel_date`,`building_number`,`management_number`,`notes`,`transaction`) VALUES (\"%s","%s","%s","%s","%s","%s","%s","%s",\'%s\',"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            value[0], value[1], value[4], value[5], '', value[37], value[38],
            value[37], value[40], value[41], 1, value[2], value[42], value[43],
            value[44], value[45], value[4], value[6], value[35], value[36],
            value[48], value[8], value[47], value[9],
            value[10], value[11], value[46], value[14], value[16], value[17],
            value[19], value[20], value[21], value[22], value[23], value[24],
            value[25], value[26], value[27], value[28],
            int(time.mktime(time.strptime(value[30], "%Y/%m/%d"))), value[31], value[32],
            value[33], value[34])
        try:
            cur.execute(sql)
        except pymysql.Error:
            logging.info(sys.exc_info())

    conn2db.commit()
    cur.close()
    conn2db.close()

    return True

if __name__ == '__main__':
    UpdateFang()
    time.sleep(10)
    GetInfo()
    time.sleep(10)

    file_name = __root_path__ + 'fangyuanInfoUpdate.csv'

    data = ReadCsv(0, 150, file_name)

    if len(data) == 0:
        print('nothing success')
        exit()

    tmp = []
    for value in data:
        time.sleep(3)
        tmp.append(HandleUrltwo(data[value]))

    SaveFangData(tmp)
    print('success')
    exit()
