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

def SavaCsv(data):
    # with open("/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv", "w", newline="") as datacsv:
    with open("/Applications/MAMP/htdocs/htdocs/python/need_map.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))


        # csvwriter.writerow(data)
        csvwriter.writerows(data)
    return 'true'

def ReadNeedCsv(file_name,results):
    if file_name == None:
        f = 'rakumachi.csv'
    else:
        f = file_name
    csvFile = open(f, "r")
    reader = csv.reader(csvFile)

    result = []
    for item in reader:
        # 忽略第一行
        if int(item[0]) in results:
            tmp = []
            tmp.append(item[0])
            tmp.append(item[4])
            result.append(tmp)
    csvFile.close()

    return result

#数据库 配置
def MysqlConfig():
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='fangcmstest',  # DB name
    )
    return conn2db


def SaveData(data,zuobiaos,dims):
    conn2db = MysqlConfig()
    cur = conn2db.cursor()

    for value in data:

        if dims.get(value) == None:
            dim = 1
        else:
            dim_own = {'1001':1,'1002':2,'1003':3,'1004':4,'1005':5}
            dim = dim_own.get(dims.get(value))

        if zuobiaos.get(value) == None:
            zuobiao = ''
        else:
            zuobiao = zuobiaos.get(value)[2] + ',' + zuobiaos.get(value)[1]

        if data[value][42] == '':
            data[value][42] = 192


        sql = 'INSERT INTO `yk_used` ( `id`,`area_id`,`title`, `address`,`map`,`area`,`build_area`,`total_floor`,`file`,`img`,`status`,`source`,`build`,`year`,`floors`,`family`,`traffic`,`location`,`price_jp`,`price_zh`,`average_price`,`surface`,`surface_s`,`annual_income`,`building`,`rank`,`construction`,`interception`,`parking`,`land_rights`,`area_burden`,`ground`,`city_plan`,`application_area`,`building_coverage`,`volumetric`,`national_law`,`contact_situation`,`present_situation`,`delivery`,`schedulel_date`,`building_number`,`management_number`,`notes`,`transaction`) VALUES (\"%s","%s","%s","%s","%s","%s","%s","%s",\'%s\',"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            value, data[value][1], data[value][3],data[value][4], zuobiao,data[value][36],data[value][37],data[value][38],data[value][39],data[value][40],1,dim,data[value][41],data[value][42],data[value][43],data[value][44],data[value][3],data[value][5], data[value][34],data[value][35],data[value][47],data[value][7],data[value][46],data[value][8],
            data[value][9],data[value][10],data[value][45],data[value][13],data[value][15],data[value][17], data[value][18],data[value][19],data[value][20],data[value][21],data[value][22],data[value][23], data[value][24],data[value][25], data[value][26],data[value][27],int(time.mktime(time.strptime(data[value][29], "%Y/%m/%d"))),data[value][30],data[value][31],data[value][32], data[value][33])

        cur.execute(sql)

    conn2db.commit()
    cur.close()
    conn2db.close()

    return True

def SelectMap():
    conn2db = MysqlConfig()

    cursor = conn2db.cursor()


    sql = "Select id from `yk_used` where map = ''"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        ids = []
        for row in results:
            ID = row[0]
            ids.append(ID)
            # 打印结果
        return ids
    except:
        print("Error: unable to fecth data")

if __name__ == '__main__':

    results = SelectMap()
    file_name = 'fangyuanInfoZh.csv'


    need = ReadNeedCsv(file_name,results)

    SavaCsv(need)

    print('ss')
    # print(result)
    exit()
    file_name = 'fangyuanInfoZh.csv'

    file_name_dim = 'rakumachigenre.csv'
    dims = ReadCsv(file_name_dim,2)

    zuobiao = 'zuobiaoss.csv'
    zuobiaos = ReadchunkCsv(0, 3300, zuobiao)

    data = ReadchunkCsv(2000,3000,file_name)


    SaveData(data,zuobiaos,dims)
    print('sss')
    exit()