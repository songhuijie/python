from selenium import webdriver
from time import sleep
import requests
import json
import csv
from geopy.geocoders import Nominatim
import ssl
import json
import webbrowser
import codecs
import urllib
import MySQLdb
import time

ssl._create_default_https_context = ssl._create_unverified_context

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Origin': 'https://cd.lianjia.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
}

def Chuli(req_url):
    # req_url = "http://www.baidu.com/link?url=ojjD2hHxviDl0j4T6MCQzRaQYUyYe0BX2aCXcNI5UliRtQum2Y7XH9_xZ08mzOJH"
    # req_url = 'https://www.google.co.jp/maps?q=' + string

    executable_path = '/Applications/MAMP/htdocs/htdocs/python/chromedriver'

    # 设置chrome浏览器无界面模式
    browser = webdriver.Chrome(executable_path=executable_path)
    # 开始请求
    browser.set_page_load_timeout(30)
    browser.set_script_timeout(30)
    sleep(5)
    need_url = browser.get(req_url)

    # 打印页面网址
    print(need_url)
    print(browser.get(req_url))
    # need = need_url.split('/')[6].replace('@', '').split(',')
    # needs = need[0] + ',' + need[1]

    browser.close()
    browser.quit()

    # return needs
    # return True
    # 关闭浏览器

    # browser.close()
    # browser.quit()

    # 关闭chromedriver进程

def get_real_url(string):
    req_url = 'https://www.google.co.jp/maps?q=' + string
    rs = requests.get(req_url,headers=headers,timeout=10)
    print(rs.url)
    exit()


def GetBaiduZB(string):
    ak = 'DHPZSVdV5uiwtQBFOGz5Ha7RbDBGYciE'
    url = "http://api.map.baidu.com/geoconv/v1/?coords="+ string +"&output=json&from=3&to=5&ak=" + ak

    key = '9550xz1w3x9645x176xw2833wzv21w3wy6089'
    oid = 9611
    url2 = "http://api.gpsspg.com/convert/coord/?oid=9611&key=9550xz1w3x9645x176xw2833wzv21w3wy6089&from=0&to=2&latlng=35.0020619,135.731663"

    req = requests.get(url,headers = headers)
    own_string = []
    if(req.status_code == 200):
        result = json.loads(req.text)
        for value in result.get('result'):
               own_string.append(str(value.get('y')))
               own_string.append(str(value.get('x')))
    else:
        pass

    return ','.join(own_string)

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
            elif type == 5:
                result[item[0]] = item[3]
            elif type == 10:
                result[item[0]] = item[13]
            else:
                result[item[0]] = item[1]
    csvFile.close()

    return result

def SaveZB(datas):
    with open("/Applications/MAMP/htdocs/htdocs/python/zuobiaos.csv", "w", newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerows(datas)
    return 'true'

def ReadCsvs(min,max,filename=None,type=1):
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


    return own_img

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


def MakeStr(string):

    return string.split('=')[0] + "=" + urllib.parse.quote(string.split('=')[1])

if __name__ == '__main__':

    # address = "四川省成都市新都区"
    # gps = Nominatim(user_agent=user_agent)
    # location = gps.geocode(address)
    # # location = gps.reverse(address)
    # print(location)
    #
    # exit()
    # print(location.longitude, location.latitude)
    # exit()


    # file_name = '/Applications/MAMP/htdocs/htdocs/python/houserInfoCh.csv'
    file_name = '/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv'
    data = ReadCsv(1,3,file_name,10)

    print(data)
    exit()

    file_name = '/Applications/MAMP/htdocs/htdocs/python/zuobiaoss.csv'
    data2 = ReadCsv(600,610,file_name,4)

    # print(data2)
    # print(urllib.parse.quote('大阪府大阪市大正区'))
    # exit()
    chrome_path = '/Applications/MAMP/htdocs/htdocs/python/chromedriver'



    for value in data2:
        print(data2[value])
        sleep(1)
        webbrowser.get('chrome')
        webbrowser.get('chrome').open(MakeStr(data2[value]))
    print('success')
    exit()


    # arr = []
    # for value in data:
    #     tmp = []
    #     tmp.append(value)
    #     tmp.append('https://www.google.co.jp/maps?q=' + data[value].replace('地図を見る', ''))
    #     arr.append(tmp)
    #
    # SaveZB(arr)
    # print('success')
    # exit()
    #
    # need_url = 'https://www.google.co.jp/maps/search/%E4%BA%AC%E9%83%BD%E5%BA%9C%E4%BA%80%E5%B2%A1%E5%B8%82%E7%95%91%E9%87%8E%E7%94%BA%E5%8D%83%E3%82%B1%E7%95%91%E9%AB%99%E6%A9%8B2-112/@35.0152348,135.3999669,13z/data=!3m1!4b1'
    # need = need_url.split('/')[6].replace('@','').split(',')
    # needs = need[0] + ',' + need[1]
    #
    # result = GetBaiduZB(needs)
    # print(result)
    # exit()
    #
    # print(result)
    # exit()