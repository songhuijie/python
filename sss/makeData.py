#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import MySQLdb
import time
import re
import math
import json
import datetime

def ReadCsv(file_name,type):

    csvFile = open(file_name, "r")
    reader = csv.reader(csvFile)
    # 建立空字典
    result = {}
    for item in reader:
        # 忽略第一行
        if type == 1:
            result[item[0]] = item
        else:
            result[item[0]] = item[1]
    csvFile.close()

    return result

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

def disposeImg(imgs,id):

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
        own_img = own_tmp.replace('\'','\"')
    else:
        own_img = ''
        msg = id + '暂无图片'

    return own_img

def disImg(imgs,id):
    if imgs:
        array = imgs.split(';')

        file_path = '/Uploads/datas/images/property/'

        tmp = file_path + id + '/' + array[0][array[0].rindex("/") + 1:]

        own_img = str(tmp)
    else:
        own_img = ''
        msg = id + '暂无图片'

    return own_img

def handleMoney(string):
    own_string = re.findall(r"\d+\.?\d*",string)


    need = ''
    for value in own_string:
        need += value


    return int(need)

def handleArea(string):
    own_string = re.findall(r"\d+\.?\d*",string)
    if len(own_string) == 0:
        return 0
    else:
        return int(float(own_string[0]))


def handlebuild(string):
    default_build = 191
    types = {'SRC建设': 186, 'RC建设': 187, '钢架': 188, '轻质钢架': 189, '木': 190, '其他': 191}

    result = types.get(string)
    if result == None:
        return default_build
    else:
        return result

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

def handleconstruction(string):
    tmp = string.split('（')
    return tmp[0]

def handleNianHua(string):
    own_string = re.findall(r"\d+\.?\d*", string)

    if len(own_string) == 0:
        return 0
    else:
        return math.ceil(float(own_string[0]) * 100)

def handleAverage(price,area):
    average_price = int(price) / area

    return int(round(average_price,1)*10000)



def SaveData(data,area_ids,address,zuobiaos,moneys,dims):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='fangcmstest',  # DB name
    )

    cur = conn2db.cursor()

    for value in data:


        # price_main = handleMoney(data[value][5])
        price_zh = int(moneys.get(value)[2]) / 10000
        price_jp = int(moneys.get(value)[1]) / 10000

        if area_ids.get(value) == None:
            type = 26101
        else:
            type = area_ids.get(value)[1]

        addresss = address.get(value)[1]
        zuobiao = zuobiaos.get(value)[2] + ',' + zuobiaos.get(value)[1]
        area = handleArea(data[value][11])
        build_area = handleArea(data[value][15])
        total_floor = handleArea(data[value][13])

        own_img = disposeImg(data[value][1],value)
        own_img_f = disImg(data[value][1],value)
        build = handlebuild(data[value][8])
        year = handleyear(data[value][10])
        floors = handlefloors(data[value][9])
        familys = handlefamily(data[value][13])
        construction = handleconstruction(data[value][10])
        NianHua = handleNianHua(data[value][6])
        if dims.get(value) == None:
            dim = 1
        else:
            dim_own = {'1001':1,'1002':2,'1003':3,'1004':4,'1005':5}
            dim = dim_own.get(dims.get(value))


        average_price = handleAverage(price_zh,area)
        # print(floors)
        # print(familys)



        sql = 'INSERT INTO `yk_used` ( `id`,`area_id`,`title`, `address`,`map`,`area`,`build_area`,`total_floor`,`file`,`img`,`status`,`source`,`build`,`year`,`floors`,`family`,`traffic`,`location`,`price_jp`,`price_zh`,`average_price`,`surface`,`surface_s`,`annual_income`,`building`,`rank`,`construction`,`interception`,`parking`,`land_rights`,`area_burden`,`ground`,`city_plan`,`application_area`,`building_coverage`,`volumetric`,`national_law`,`contact_situation`,`present_situation`,`delivery`,`schedulel_date`,`building_number`,`management_number`,`notes`,`transaction`) VALUES (\"%s","%s","%s","%s","%s","%s","%s","%s",\'%s\',"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            value, type, data[value][2],addresss, zuobiao,area,build_area,total_floor,own_img,own_img_f,1,dim,build,year,floors,familys,data[value][2],data[value][4], price_jp,price_zh,average_price,data[value][6],NianHua,data[value][7],data[value][8],data[value][9],construction,data[value][12],data[value][14],data[value][16], data[value][17],data[value][18],data[value][19],data[value][20],data[value][21],data[value][22], data[value][23],data[value][24], data[value][25],data[value][26],int(time.mktime(time.strptime(data[value][27], "%Y/%m/%d"))),data[value][29],data[value][30],data[value][31], data[value][32])

        cur.execute(sql)

    conn2db.commit()
    cur.close()
    conn2db.close()

    return True

if __name__ == '__main__':


    file_name = 'houserInfoChnew.csv'
    file_name_dim = 'rakumachigenre.csv'

    dims = ReadCsv(file_name_dim,2)

    data = ReadchunkCsv(1754,1800,file_name)

    area = 'ids.csv'
    addres = 'address.csv'
    zuobiao = 'zuobiaoss.csv'
    moneys = 'moneys.csv'

    area_ids = ReadchunkCsv(0,3300,area)
    address = ReadchunkCsv(0,3300,addres)
    zuobiaos = ReadchunkCsv(0,3300,zuobiao)
    moneys = ReadchunkCsv(0,3300,moneys)


    SaveData(data,area_ids,address,zuobiaos,moneys,dims)
    print('sss')
    exit()