import execjs
from urllib import request
from urllib import parse
import csv
import ssl
import time
import json
import math
import re
import datetime
import pymysql
import sys
import logging

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
proxy = "http://177.39.187.70:37315"

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
    string = string.replace('億円','0000')
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
        req = request.Request(url,headers=headers)
        data = request.urlopen(req)
        html = data.read().decode("utf-8")
        needs = html.split(',')[0].split('"')
        need = needs[1]
        return need

# 批量 处理翻译
def googleTranslateTwo(url,datas,tmp2):
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
            datas[tmp2[value]] = needs[0][value][0].replace("\n","")


    return datas

#请求获取 翻译文字
def HandleUrl(content):
    if len(content) < 1:
        return ''
    js = Py4Js()
    tk = js.getTk(content)
    if len(content) > 4891:
        # print("翻译的长度超过限制！！！")
        return ''

    content = parse.quote(content)

    url = "https://translate.google.cn/translate_a/single?client=webapp&sl=ja&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (tk, content)


    return googleTranslate(url)

#请求获取 批量翻译文字
def HandleUrltwo(data):

    tmp = []
    need = {0:1,1:1,2:1,3:1,5:1,8:1,11:1,12:1,13:1,15:1,18:1,23:1,24:1,29:1,30:1,31:1}
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
        if value == len(tmp)-1:
            content += data[tmp[value]]
        else:
            content += data[tmp[value]].replace('〓','').replace('！','').replace('！','').replace('【','').replace('】','').replace('。','') + "\n"



    area = handleArea(data[13])
    price_jp = handleMoney(data[7])
    price_zh = math.ceil(handleMoney(data[7]) / 16.27)
    data.append(price_jp)
    data.append(price_zh)
    data.append(area)
    data.append(handleArea(data[17]))
    data.append(handleArea(data[15]))
    data.append(disposeImg(data[3],data[0]))
    data.append(disImg(data[3],data[0]))
    data.append(handlebuild(data[10]))
    data.append(handleyear(data[12]))
    data.append(handlefloors(data[11]))
    data.append(handlefamily(data[15]))
    data.append(handleconstruction(data[12]))
    data.append(handleNianHua(data[8]))

    data.append(handleAverage(price_zh,area))
    data[5] = data[5].replace('地図を見る','')

    js = Py4Js()
    tk = js.getTk(content)
    if len(content) > 4891:
        # print("翻译的长度超过限制！！！")
        return ''

    content = parse.quote(content)

    url = "https://translate.google.cn/translate_a/single?client=webapp&sl=ja&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (tk, content)

    return googleTranslateTwo(url,data,tmp2)

def ReadCsv(min,max,filename=None,type=1):
    if filename == None:
        f = '/Applications/MAMP/htdocs/htdocs/python/fangyuanInfo.csv'
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
            else:
                result[item[0]] = item[1]

    csvFile.close()

    return result

def ReadNeedCsv(need,types,filename=None,):
    if filename == None:
        f = '/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv'
    else:
        f = filename
    csvFile = open(f, "r")
    reader = csv.reader(csvFile)
    result = {}
    for item in reader:
        if types == 1:
            if item[0] not in need:
                result[item[0]] = item
        else:
            if item[0] in need:
                result[item[0]] = item

    return result

def SaveCsv(data):
    # 添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoCh.csv", "w", newline="") as datacsv:
    # 追加
    with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoCh.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp =[]
        for value in data:
            tmp.append(value)

        csvwriter.writerows(tmp)
    return 'true'

def SaveNewCsv(data):
    # 添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoChnew.csv", "w", newline="") as datacsv:
    # with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoChleave.csv", "w", newline="") as datacsv:
    # with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoChleaves.csv", "w", newline="") as datacsv:
    # with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoChleavess.csv", "w", newline="") as datacsv:
    # 追加
    # with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoChnew.csv", "a", newline="") as datacsv:
    # with open("/Applications/MAMP/htdocs/htdocs/python/houserInfoChleave.csv", "a", newline="") as datacsv:
    with open("/Applications/MAMP/htdocs/htdocs/python/fangyuanInfoZh.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        # tmp = []
        # for value in data:
        #     # tmp.append(data[value])
        #     tmp.append(value)

        csvwriter.writerow(data)
    return 'true'

def SaveFangData(data):
    conn2db = pymysql.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='fangcmstest',  # DB name
    )
    cur = conn2db.cursor()

    error_log = 'fang_error.log'
    logging.basicConfig(filename=error_log, level = logging.INFO)

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

    file_name = 'fangyuanInfoUpdate.csv'

    data = ReadCsv(0, 150,file_name)

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