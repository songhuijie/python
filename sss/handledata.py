# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import csv
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import os
import urlparse2



__path__ = '../fangcms/Uploads/datas/images/property/'
proxies = {
    "http": "http://178.79.46.5:59073"
}
url_index = 'https://www.rakumachi.jp'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Origin': 'https://cd.lianjia.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
}

f = open(r'/Applications/MAMP/htdocs/htdocs/python/sss/house.txt', 'r')  # 打开所保存的cookies内容文件
cookies = {}  # 初始化cookies字典变量
for line in f.read().split(';'):  # 按照字符：进行划分读取
    # 其设置为1就会把字符串拆分成2份
    name, value = line.strip().split('=', 1)
    cookies[name] = value



def SaveData(data):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='fangcmstest',  # DB name
    )

    cur = conn2db.cursor()
    for value in data:

        sql = "INSERT INTO `yk_area_cate` ( `id`, `name`,`alias`,`pid`, `spid`, `ordid`) VALUES (\
                    '%s','%s','%s','%s','%s','%s')" % (
            value[0], value[1], value[2],value[3],0,255)
        cur.execute(sql)

    conn2db.commit()
    cur.close()
    conn2db.close()

    return 'true'

def ReadCsv():
    with open("/Applications/MAMP/htdocs/htdocs/python/rakumachi.csv", "r+", newline="") as datacsv:
        reader = csv.reader(datacsv)
        headers = next(reader)
        rows = [row for row in reader]

    return rows

def ReadchunkCsv(min,max,filename=None):
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

def SaveCsvFangInfo(data):
    # with open("/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv", "w", newline="") as datacsv:
    with open("/Applications/MAMP/htdocs/htdocs/python/fangyuanInfoUpdate.csv", "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # csvwriter.writerow(["id", "图片","物件名","所在地","沿線交通","販売価格","表面利回り表面利回り","想定年間収入想定年間収入","建物構造建物構造","階数階数","築年月","建物面積","間取り","総戸数総戸数","駐車場駐車場","土地面積","土地権利土地権利","私道負担面積","地目地目","都市計画区域都市計画区域","用途地域用途地域","建ぺい率建ぺい率","容積率容積率","国土法届出国土法届出","接道状況接道状況","現況現況","引渡し引渡し","次回更新予定日","更新日","建築確認番号","管理番号","注意事項","取引態様"])
        tmp =[]

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
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1
def HandleImg(soup,tmps,id):


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
            open(file_path + listimg[value].get('src')[listimg[value].get('src').rindex("/") + 1:], 'wb').write(ir.content)
        tmp.append(url_index + listimg[value].get('src'))


    imgs = ";".join(tmp)
    tmps.append(imgs)
    return tmps

def Own_HandleHtml(soup,id,type_id,source):
    tmp = []

    if soup == None:
        return tmp
    else:
        tmp.append(id)
        tmp.append(type_id)
        tmp.append(source)
        tmp = HandleImg(soup,tmp,id)
        info = soup.find('table',class_="Effect03")
        listinfo = info.select('td')

        for value in range(len(listinfo)):
            # tmp.append(value.get_text())
            tmp.append("".join(listinfo[value].get_text().replace('\n', '').split()))
        return tmp

def seleniumHandle(url):

    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='/Applications/MAMP/htdocs/htdocs/python/geckodriver')
    driver.get(url)
    time.sleep(0.3)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    return soup


def getArea(own_int):

    url = "https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?page=1&limit=60&area[]=" + str(own_int) + "&newly=&price_from=&price_to=&gross_from=&gross_to=&dim[]=1001&dim[]=1002&dim[]=1003&dim[]=1004&dim[]=1005&year=&b_area_from=&b_area_to=&houses_ge=&houses_le=&min=&l_area_from=&l_area_to=&keyword=&ex_real_search=&sort=property_created_at&sort_type=desc"

    soup = reqPage(url)
    listurls = soup.select('div[class^="listCheckbox"]')
    print(listurls)
    exit()

def handleSource(string):
    own_source = string.split('/')
    sources = {'dim1001':1,'dim1002':2,'dim1003':3,'dim1004':4,'dim1005':5}

    if sources.get(own_source[6]) == None:
        source = 1
    else:
        source = sources.get(own_source[6])

    return source


def test():
    # 200 ,300
    # result = ReadchunkCsv(3400,3600)
    # tmp = []
    # for value in result:
    #     for i in result:
    #         test = []
    #         test.append(value)
    #         test.append(result[value])
    #     tmp.append(test)
    #
    # tmp2 = []
    # print(tmp)
    # exit()
    # for value in tmp:
    #     time.sleep(5)
    #     soup = reqPage(value[1])
    #     if soup == None:
    #         pass
    #     else:
    #         result = HandleHtml(soup, value[0])
    #         tmp2.append(result)
    #
    #
    # if len(tmp2) > 0:
    #     SaveCsv(tmp2)
    # file_name = '/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv'
    # result = ReadchunkCsv(1,10,file_name)
    #
    #
    # for value in result:
    #     print(result[value][1])
    #     exit()
    # print(result)
    # exit()
    # b = '京都府亀岡市畑野町 '
    # a = 'https://www.rakumachi.jp/syuuekibukken/area/prefecture/dimAll/?page=53&limit=60&area[]=26&area[]=27102&area[]=27103&area[]=27104&area[]=27106&area[]=27107&area[]=27108&area[]=27109&area[]=27111&area[]=27113&area[]=27114&area[]=27115&area[]=27116&area[]=27117&area[]=27118&area[]=27119&area[]=27120&area[]=27121&area[]=27122&area[]=27123&area[]=27124&area[]=27125&area[]=27126&area[]=27127&area[]=27128&area[]=28101&area[]=28102&area[]=28105&area[]=28106&area[]=28107&area[]=28108&area[]=28109&area[]=28110&area[]=28111&newly=&price_from=&price_to=&gross_from=&gross_to=&dim[]=1001&dim[]=1002&dim[]=1003&dim[]=1004&dim[]=1005&year=&b_area_from=&b_area_to=&houses_ge=&houses_le=&min=&l_area_from=&l_area_to=&keyword=&ex_real_search=&sort=property_created_at&sort_type=desc'
    # url = 'https://www.google.co.jp/maps?q=%E4%BA%AC%E9%83%BD%E5%BA%9C%E4%BA%80%E5%B2%A1%E5%B8%82%E7%95%91%E9%87%8E%E7%94%BA%E5%8D%83%E3%82%B1%E7%95%91%E9%AB%99%E6%A9%8B2-112'
    # r = requests.get(url)
    # print(r.url)
    # exit()
    # url = 'https://maps.google.com/maps/geo?output=json&key=AIzaSyChLmJVGDMSu-T3JGjneu_XK6J_48fNNDY&q=%E5%A4%A7%E9%98%AA%E5%BA%9C%E5%A4%A7%E9%98%AA%E5%B8%82%E5%A4%A9%E7%8E%8B%E5%AF%BA%E5%8C%BA%E4%B8%8A%E6%9C%AC%E7%94%BA5%E4%B8%81%E7%9B%AE'
    # r = requests.get(url)
    # print(r.text)
    # exit()

    area = {
        26: '京都府',
        26101: '京都府北区',
        26102: '京都上京区',
        26103: '京都左京区',
        26104: '京都中京区',
        26105: '京都東山区',
        26106: '京都下京区',
        26107: '京都南区',
        26108: '京都右京区',
        26109: '京都伏見区',
        26110: '京都山科区',
        26111: '京都西京区',
        27: '大阪市',
        27102: '大阪市都島区',
        27103: '大阪市福島区',
        27104: '大阪市此花区',
        27106: '大阪市西区',
        27107: '大阪市港区',
        27108: '大阪市大正区',
        27109: '大阪市天王寺区',
        27111: '大阪市浪速区',
        27113: '大阪市西淀川区',
        27114: '大阪市東淀川区',
        27115: '大阪市東成区',
        27116: '大阪市生野区',
        27117: '大阪市旭区',
        27118: '大阪市城東区',
        27119: '大阪市阿倍野区',
        27120: '大阪市住吉区',
        27121: '大阪市東住吉区',
        27122: '大阪市西成区',
        27123: '大阪市淀川区',
        27124: '大阪市鶴見区',
        27125: '大阪市住之江区',
        27126: '大阪市平野区',
        27127: '大阪市北区',
        27128: '大阪市中央区',
        28: '神戸市',
        28101: '神戸市東灘区',
        28105: '神戸市兵庫区',
        28106: '神戸市長田区',
        28107: '神戸市須磨区',
        28108: '神戸市垂水区',
        28109: '神戸市北区',
        28110: '神戸市中央区',
        28111: '神戸市西区',
    }

    area2 = {
        26: 'jingdu',
        26101: 'jingdubei',
        26102: 'jingdushangjing',
        26103: 'jingduzuojing',
        26104: 'jingduzhongjing',
        26105: 'jingdudongshan',
        26106: 'jingduxiajin',
        26107: 'jingdunanqu',
        26108: 'jingduyoujinqu',
        26109: 'jingdufujianqu',
        26110: 'jingdusankequ',
        26111: 'jingduxijingqu',
        27: 'daban',
        27102: 'dabandudao',
        27103: 'dabanfudao',
        27104: 'dabancihua',
        27106: 'dabanxi',
        27107: 'dabangang',
        27108: 'dabandazheng',
        27109: 'dabantianwangshi',
        27111: 'dabanlangsu',
        27113: 'dabanxidingchuan',
        27114: 'dabandongdingchuang',
        27115: 'dabandongcheng',
        27116: 'shengye',
        27117: 'dabanxuqu',
        27118: 'dabanchengdu',
        27119: 'dabanabeiye',
        27120: 'dabanzhuji',
        27121: 'dabandongzhuji',
        27122: 'dabanxicheng',
        27123: 'dabandingchuan',
        27124: 'dabanhejian',
        27125: 'dabanzhuzhijiang',
        27126: 'pingye',
        27127: 'dabanbei',
        27128: 'dabanzhongyang',
        28: 'shenhu',
        28101: 'shenhudongtan',
        28105: 'shenhubingku',
        28106: 'shenhuchangtian',
        28107: 'shenhuxumo',
        28108: 'shenhuchuishui',
        28109: 'shenhubei',
        28110: 'shenhuzhongyang',
        28111: 'shenhuxiqu',
    }
    area3 = {
        26: 0,
        26101: 26,
        26102: 26,
        26103: 26,
        26104: 26,
        26105: 26,
        26106: 26,
        26107: 26,
        26108: 26,
        26109: 26,
        26110: 26,
        26111: 26,
        27: 0,
        27102: 27,
        27103: 27,
        27104: 27,
        27106: 27,
        27107: 27,
        27108: 27,
        27109: 27,
        27111: 27,
        27113: 27,
        27114: 27,
        27115: 27,
        27116: 27,
        27117: 27,
        27118: 27,
        27119: 27,
        27120: 27,
        27121: 27,
        27122: 27,
        27123: 27,
        27124: 27,
        27125: 27,
        27126: 27,
        27127: 27,
        27128: 27,
        28: 0,
        28101: 28,
        28105: 28,
        28106: 28,
        28107: 28,
        28108: 28,
        28109: 28,
        28110: 28,
        28111: 28,
    }
    arr = []

    for value in area:
        tmp = []
        tmp.append(value)
        tmp.append(area[value])
        tmp.append(area2[value])
        tmp.append(area3[value])
        arr.append(tmp)

    SaveData(arr)
    print('success')
    exit()

    # area = {
    #     26:'京都府'
    # }
    # for value in area:
    #     time.sleep(3)
    #     getArea(value)

    print('success')
    exit()

def GetInfo():
    filename = 'rakumachigenres.csv'
    result = ReadchunkCsv(0, 1, filename)

    if len(result) == 0:
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

if __name__ == '__main__':

    print(cookies)
    exit()
    GetInfo()

    print('sssss')
    exit()


