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
from collections import OrderedDict
import math

ssl._create_default_https_context = ssl._create_unverified_context

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

f = open(r'/Applications/MAMP/htdocs/htdocs/python/house.txt', 'r')  # 打开所保存的cookies内容文件
cookies = {}  # 初始化cookies字典变量
for line in f.read().split(';'):  # 按照字符：进行划分读取
    # 其设置为1就会把字符串拆分成2份
    name, value = line.strip().split('=', 1)
    cookies[name] = value


def copyInfo(url):
    r = requests.get(url,headers = headers)  # 最基本的GET请求


    if r.status_code == 200:
        soup = BeautifulSoup(r.text,'html5lib')
        price = soup.find('p', class_="content__aside--title")

        price =price.get_text()

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
        for i,h in housesides:
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



def saveHouseing(data,ids):
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
            value,type,data[value][1], disposeImg(data[value][1],value), data[value][2],data[value][3],data[value][4],data[value][5],data[value][6],data[value][7],data[value][8],data[value][9],data[value][10],data[value][11],data[value][12],data[value][13],data[value][14],data[value][15],data[value][16],data[value][17],data[value][18],data[value][19],data[value][20],data[value][21],data[value][22],data[value][23],data[value][24],data[value][25],data[value][26],int(time.mktime(time.strptime(data[value][27], "%Y/%m/%d"))),int(time.mktime(time.strptime(data[value][28], "%Y/%m/%d"))),data[value][29],data[value][30],data[value][31],data[value][32])
        cur.execute(sql)

    conn2db.commit()
    cur.close()
    conn2db.close()

    return 'true'

def saveHouseingZh(data,ids,money1,money2,address):
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
            value,type,data[value][1], disposeImg(data[value][1],value), data[value][2],addr,data[value][4],money_jp,money_zh,data[value][5],data[value][6],data[value][7],data[value][8],data[value][9],data[value][10],data[value][11],data[value][12],data[value][13],data[value][14],data[value][15],data[value][16],data[value][17],data[value][18],data[value][19],data[value][20],data[value][21],data[value][22],data[value][23],data[value][24],data[value][25],data[value][26],int(time.mktime(time.strptime(data[value][27], "%Y/%m/%d"))),int(time.mktime(time.strptime(data[value][28], "%Y/%m/%d"))),data[value][29],data[value][30],data[value][31],data[value][32])
        cur.execute(sql)

    conn2db.commit()
    cur.close()
    conn2db.close()

    return 'true'

def disposeImg(imgs,id):

    if imgs:
        array = imgs.split(';')

        file_path = '/data/images/property/'
        tmp = []
        for value in array:
            tmp.append(file_path + id + '/' + value[value.rindex("/") + 1:])

        own_img = ';'.join(tmp)
    else:
        own_img = ''
        msg = id + '暂无图片'
        # RecordLog(msg)

    return own_img


def saveCsv(type,data):
    #添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/rakumachi.csv", "w", newline="") as datacsv:
    #追加
    with open("rakumachigenres.csv", "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp =[]

        for value in data:
            for i in data:
                row = []
                row.append(value)
                row.append(type)
                row.append(data[value])
            tmp.append(row)

        csvwriter.writerows(tmp)
    return 'true'

def saveSourceCsv(type,data):
    #添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/rakumachigenres.csv", "a", newline="") as datacsv:
    #追加
    with open("/Applications/MAMP/htdocs/htdocs/python/rakumachigenre.csv", "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp =[]

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
                #加上代理

                req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                # req = requests.get(url, headers=headers,cookies = cookies)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
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
                #加上代理

                req = requests.get(url, headers=headers)
                # req = requests.get(url, headers=headers,cookies = cookies)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
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

def HandleHtml(soup,data,next_url=''):

    listurls = soup.select('div[class^="propertyBlock__mainArea"]')



    if len(listurls) == 0:
        # RecordLog(next_url)
        return data
    else:
        for list in listurls:
            data[list.get('onclick').split('\'')[1].split('/')[5]] = url_index + list.get('onclick').split('\'')[1]
        return data

def HandleHtmlSupply(soup,data,next_url='',own_id=''):
    listurls = soup.select('div[class^="propertyBlock__mainArea"]')

    if len(listurls) == 0:
        # RecordLog(next_url)
        return data
    else:
        for lists in listurls:
            if int(lists.get('onclick').split('\'')[1].split('/')[5]) > int(own_id):
                data[lists.get('onclick').split('\'')[1].split('/')[5]] = url_index + lists.get('onclick').split('\'')[1]
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

def SaveCsv(data,id):
    # with open("/Applications/MAMP/htdocs/htdocs/python/ids.csv", "w", newline="") as datacsv:
    with open("/Applications/MAMP/htdocs/htdocs/python/ids.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # csvwriter.writerow(["house_id", "图片","物件名","所在地","沿線交通","販売価格","表面利回り表面利回り","想定年間収入想定年間収入","建物構造建物構造","階数階数","築年月","建物面積","間取り","総戸数総戸数","駐車場駐車場","土地面積","土地権利土地権利","私道負担面積","地目地目","都市計画区域都市計画区域","用途地域用途地域","建ぺい率建ぺい率","容積率容積率","国土法届出国土法届出","接道状況接道状況","現況現況","引渡し引渡し","次回更新予定日","更新日","建築確認番号","管理番号","注意事項","取引態様"])
        datas = []

        for value in data:
            for i in data:
                tmp=[]
                tmp.append(value)
                tmp.append(id)
            datas.append(tmp)
        csvwriter.writerows(datas)
    return 'true'

def SaveNext(data):
    with open("next.csv", "w", newline="") as datacsv:
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
def getArea(soup,data):


    listurls = soup.select('input[class^="listCheckbox"]')

    for value in listurls:
        data.append(value.get('value'))

    return data

def handleids(url,value):

    tmp = []
    soup = reqPage(url)
    data = getArea(soup,tmp)
    own_url = NextPage(soup)

    if own_url == 0:
        pass
    else:
        next_url = own_url
        while(next_url):
            time.sleep(3)
            getArea(reqPage(next_url),data)
            next_url = NextPage(reqPage(next_url))

    SaveCsv(data,value)
    return True


def ReadCsv(min,max,filename=None,type=1):
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

def handleMoney(string):
    own_string = re.findall(r"\d+\.?\d*",string)

    need = ''
    for value in own_string:
        need += value

    return int(need)

def googleTranslate(string):
    if string == '':
        need = ''
    else:
        url = "https://translate.google.cn/translate_a/single?client=webapp&sl=ja&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&otf=1&pc=1&ssel=4&tsel=0&kc=2&tk=355506.254149&q="
        url = "https://translate.google.cn/translate_a/single?client=webapp&sl=ja&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=339377.238027&q="
        url_values = parse.quote(string)

        full_url = url + url_values
        print(full_url)
        exit()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
        req = request.Request(full_url,headers=headers)
        data = request.urlopen(req).read()
        html = data.decode("utf-8")
        needs = html.split(',')[0].split('"')
        need = needs[1]
    return need

def handleAddress(string):
    own_string = string.replace('地図を見る','')
    return own_string


def UpdateFang():
    ids = [26101, 26102, 26103, 26104, 26105, 26106, 26107, 26108, 26109, 26110, 26111, 27102, 27103, 27104, 27106,
           27107, 27108, 27109, 27111, 27113, 27114, 27115, 27116, 27117, 27118, 27119, 27120, 27121, 27122, 27123,
           27124, 27125, 27126, 27127, 27128, 28101, 28105, 28106, 28107, 28108, 28109, 28110, 28111]
    file_name = 'next.csv'

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
    dims = [1001,1002,1003,1004,1005]
    file_name = 'source.csv'

    source = ReadCsv(0, 50, file_name, 5)

    for value in dims:
        test_url = 'https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?limit=60&area[]=26104&area[]=26105&area[]=26106&area[]=26107&area[]=26108&area[]=26109&area[]=26110&area[]=26111&area[]=27102&area[]=27103&area[]=27104&area[]=27106&area[]=27107&area[]=27108&area[]=27109&area[]=27111&area[]=27113&area[]=27114&area[]=27115&area[]=27116&area[]=27117&area[]=27118&area[]=27119&area[]=27120&area[]=27121&area[]=27122&area[]=27123&area[]=27124&area[]=27125&area[]=27126&area[]=27127&area[]=27128&area[]=28101&area[]=28105&area[]=28106&area[]=28107&area[]=28108&area[]=28109&area[]=28110&area[]=28111&newly=&price_from=&price_to=&gross_from=&gross_to=&dim[]=%s&year=&b_area_from=&b_area_to=&houses_ge=&houses_le=&min=&l_area_from=&l_area_to=&keyword=&ex_real_search=&sort=property_created_at&sort_type=desc' % (value)
        data = {}
        soup = reqPage(test_url)
        data = HandleHtml(soup,data,test_url)

        own_url = NextPage(soup)


        time.sleep(30)
        saveCsv(value,data)
    return True

if __name__ == '__main__':

    UpdateFang()

    print('success')
    exit()


    # dims = [1001,1002,1003,1004,1005]
    #
    # for value in dims:
    #     test_url = 'https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?limit=60&area[]=26104&area[]=26105&area[]=26106&area[]=26107&area[]=26108&area[]=26109&area[]=26110&area[]=26111&area[]=27102&area[]=27103&area[]=27104&area[]=27106&area[]=27107&area[]=27108&area[]=27109&area[]=27111&area[]=27113&area[]=27114&area[]=27115&area[]=27116&area[]=27117&area[]=27118&area[]=27119&area[]=27120&area[]=27121&area[]=27122&area[]=27123&area[]=27124&area[]=27125&area[]=27126&area[]=27127&area[]=27128&area[]=28101&area[]=28105&area[]=28106&area[]=28107&area[]=28108&area[]=28109&area[]=28110&area[]=28111&newly=&price_from=&price_to=&gross_from=&gross_to=&dim[]=%s&year=&b_area_from=&b_area_to=&houses_ge=&houses_le=&min=&l_area_from=&l_area_to=&keyword=&ex_real_search=&sort=property_created_at&sort_type=desc' % (value)
    #     data = {}
    #     soup = reqPage(test_url)
    #     data = HandleHtml(soup,data,test_url)
    #
    #     own_url = NextPage(soup)
    #     if own_url == 0 :
    #         pass
    #     else:
    #         next_url = own_url
    #         while(next_url):
    #             time.sleep(3)
    #             data = HandleHtml(reqPage(next_url), data,next_url)
    #             next_url = NextPage(reqPage(next_url))
    #
    #     time.sleep(30)
    #     saveCsv(value,data)
    #
    #
    # print(test_url)
    # exit()


    # 抓取数据
    # for value in ids:
    #     test_url = 'https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?limit=60&area[]=%s&newly=&price_from=&price_to=&gross_from=&gross_to=&dim[]=1001&dim[]=1002&dim[]=1003&dim[]=1004&dim[]=1005&year=&b_area_from=&b_area_to=&houses_ge=&houses_le=&min=&l_area_from=&l_area_to=&keyword=&ex_real_search=&sort=property_created_at&sort_type=desc' % (value)
    #     data = {}
    #     soup = reqPage(test_url)
    #     data = HandleHtml(soup,data,test_url)
    #     own_url = NextPage(soup)
    #     if own_url == 0 :
    #         pass
    #     else:
    #         next_url = own_url
    #         while(next_url):
    #             time.sleep(3)
    #             data = HandleHtml(reqPage(next_url), data,next_url)
    #             next_url = NextPage(reqPage(next_url))
    #
    #     time.sleep(30)
    #     saveCsv(value,data)
    #
    # print('ssss')
    # exit()


    # area = {
    #     26: '京都府',
    #     27102: '大阪市都島区',
    #     27103: '大阪市福島区',
    #     27104: '大阪市此花区',
    #     27106: '大阪市西区',
    #     27107: '大阪市港区',
    #     27108: '大阪市大正区',
    #     27109: '大阪市天王寺区',
    #     27111: '大阪市浪速区',
    #     27113: '大阪市西淀川区',
    #     27114: '大阪市東淀川区',
    #     27115: '大阪市東成区',
    #     27116: '大阪市生野区',
    #     27117: '大阪市旭区',
    #     27118: '大阪市城東区',
    #     27119: '大阪市阿倍野区',
    #     27120: '大阪市住吉区',
    #     27121: '大阪市東住吉区',
    #     27122: '大阪市西成区',
    #     27123: '大阪市淀川区',
    #     27124: '大阪市鶴見区',
    #     27125: '大阪市住之江区',
    #     27126: '大阪市平野区',
    #     27127: '大阪市北区',
    #     27128: '大阪市中央区',
    #     28101: '神戸市東灘区',
    #     28102: '大阪市住之江区',
    #     28105: '神戸市兵庫区',
    #     28106: '神戸市長田区',
    #     28107: '神戸市須磨区',
    #     28108: '神戸市垂水区',
    #     28109: '神戸市北区',
    #     28110: '神戸市中央区',
    #     28111: '神戸市西区',
    # }
    # filename1 = '/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv'
    # filename = '/Applications/MAMP/htdocs/htdocs/python/houserInfoChnew.csv'
    # filename2 = '/Applications/MAMP/htdocs/htdocs/python/houserInfoChleaves.csv'
    # ids = '/Applications/MAMP/htdocs/htdocs/python/ids.csv'
    # moneys = '/Applications/MAMP/htdocs/htdocs/python/moneys.csv'
    # address = '/Applications/MAMP/htdocs/htdocs/python/address.csv'
    # a= [350,1144,1181,1272,1324,1361,1407,1529,1639,1923,2273,2400,2591]
    # a= [14,54,107]
    #
    # result = ReadCsv(2591, 2592, filename)
    # result = ReadCsv(107, 108, filename2)
    # # print(result)
    # # exit()
    # ids = ReadCsv(0, 3200, ids, 4)
    # money1 = ReadCsv(0, 3200, moneys, 4)
    # money2 = ReadCsv(0, 3200, moneys, 3)
    # address = ReadCsv(0, 3200, address, 4)

    # result = ReadCsv(1,3200, filename1)
    # arr = []
    # for value in result:
    #     tmp =[]
    #     tmp.append(result[value][0])
    #     tmp.append(handleAddress(result[value][3]))
    #     arr.append(tmp)
    #
    # SaveAddressCsv(arr)
    # print('success')
    # exit()

    #
    # tmp =[]
    # for value in result:
    #     tmp.append(int(result[value][0]))
    #     tmp.append(int(ids.get(result[value][0])))
    #     tmp.append(result[value][1])
    #     tmp.append(disposeImg(result[value][1],value))
    #     tmp.append(result[value][2])
    #     tmp.append(address.get(result[value][0]))
    #     tmp.append(result[value][4])
    #     tmp.append(money1.get(result[value][0]))
    #     tmp.append(money2.get(result[value][0]))
    #     tmp.append(result[value][5])
    #     tmp.append(result[value][6])
    #     tmp.append(result[value][7])
    #     tmp.append(result[value][8])
    #     tmp.append(result[value][9])
    #     tmp.append(result[value][10])
    #     tmp.append(result[value][11])
    #     tmp.append(result[value][12])
    #     tmp.append(result[value][13])
    #     tmp.append(result[value][14])
    #     tmp.append(result[value][15])
    #     tmp.append(result[value][16])
    #     tmp.append(result[value][17])
    #     tmp.append(result[value][18])
    #     tmp.append(result[value][19])
    #     tmp.append(result[value][20])
    #     tmp.append(result[value][21])
    #     tmp.append(result[value][22])
    #     tmp.append(result[value][23])
    #     tmp.append(result[value][24])
    #     tmp.append(result[value][25])
    #     tmp.append(result[value][26])
    #     tmp.append(int(time.mktime(time.strptime(result[value][27], "%Y/%m/%d"))))
    #     tmp.append(int(time.mktime(time.strptime(result[value][28], "%Y/%m/%d"))))
    #     tmp.append(result[value][29])
    #     tmp.append(result[value][30])
    #     tmp.append(result[value][31])
    #     tmp.append(result[value][32])
    # print(tmp)
    # exit()
    # 这些都没有插入进数据库
    # result = ReadCsv(300,400,filename2)
    # ids = ReadCsv(0, 3200, ids, 4)
    # money1 = ReadCsv(0, 3200, moneys, 4)
    # money2 = ReadCsv(0, 3200, moneys, 3)
    #
    # saveHouseingZh(result, ids, money1, money2)
    # print('success')
    # exit()
    # moneys = []
    # for value in result:
    #     tmp=[]
    #     tmp.append(value)
    #     tmp.append(handleMoney(result[value]) * 10000)
    #     tmp.append(math.ceil(handleMoney(result[value]) / 16.27) * 10000)
    #     moneys.append(tmp)
    #
    # SaveMoneyCsv(moneys)






    # result = reqPages('https://stock.tuchong.com/search?term=%E6%98%9F%E7%A9%BA&type=&layout=&use=0&search_from=head&source=extbaidudkey27#131679943527638938')
    # print(result)
    # exit()
    #
    # a = '399,3019,867295,1442872'
    #
    # tmp = {}
    #
    # result = ReadCsv(1,2)
    # for value in result:
    #     arr = []
    #     print(result[value][2])
    #     print(googleTranslate(result[value][2]))
    #     exit()
    #     arr.append(result[value][0])
    #     arr.append(result[value][1])
    #     arr.append(googleTranslate(result[value][2]))
    #     arr.append(result[value][3])
    #     arr.append(result[value][4])
    #     arr.append(result[value][5])
    #     arr.append(result[value][6])
    #     arr.append(result[value][7])
    #     arr.append(result[value][8])
    #     arr.append(result[value][9])
    #     arr.append(result[value][10])
    #     arr.append(result[value][11])
    #     arr.append(result[value][12])
    #     arr.append(result[value][13])
    #     arr.append(result[value][14])
    #     arr.append(result[value][15])
    #     arr.append(result[value][16])
    #     arr.append(result[value][17])
    #     arr.append(result[value][18])
    #     arr.append(result[value][19])
    #     arr.append(result[value][20])
    #     arr.append(result[value][21])
    #     arr.append(result[value][22])
    #     arr.append(result[value][23])
    #     arr.append(result[value][24])
    #     arr.append(result[value][25])
    #     arr.append(result[value][26])
    #     arr.append(result[value][27])
    #     arr.append(result[value][28])
    #     arr.append(result[value][29])
    #     arr.append(result[value][30])
    #     arr.append(result[value][31])
    #     arr.append(result[value][32])
    #     tmp[value] = arr
    #     # print(result[value][2])
    #     # print(result[value][3])
    #     # print(result[value][4])
    #     # print(result[value][5])
    #     # print(result[value][7])
    #     # print(result[value][8])
    #     # print(result[value][10])
    #     # print(result[value][12])
    #     # print(result[value][13])
    #     # print(result[value][15])
    #     # print(result[value][16])
    #     # print(result[value][18])
    #     # print(result[value][19])
    #     # print(result[value][20])
    #     # print(result[value][23])
    #     # print(result[value][24])
    #     # print(result[value][25])
    #     # print(result[value][26])
    #     # print(result[value][29])
    #     # print(result[value][31])
    #     # print(result[value][32])
    #
    # print(tmp)
    # exit()
    # # file_name = '/Applications/MAMP/htdocs/htdocs/python/ids.csv'
    # # ids = ReadCsv(0,3227,file_name,2)
    # # saveHouseing(result,ids)
    #
    # print('success')
    # exit()






