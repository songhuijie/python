import csv
import MySQLdb
from bs4 import BeautifulSoup
import requests
import time

db_name = 1
offset = 0
limit = 100

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
}

proxies = {
    "https": "https://203.142.76.171:3128"
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
                req = requests.get(url, headers=headers,proxies = proxies,timeout=5)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    # return req.text
                    return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def saveData(data,type):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )

    cur = conn2db.cursor()

    sql = "update `xvideo` set `video_tag` = '%s' Where id = %s" % (data[1],data[0])

    # for value in range(len(data)):
    #     if value == len(data) -1:
    #         sql += " ('" + data[value] + "');"
    #     else:
    #         sql += " ('" + data[value] + "'),"

    try:
        cur.execute(sql)  # 执行sql语句
        conn2db.commit()  # 提交到数据库执行
        print('更新成功')
    except:
        print('更新失败')
        conn2db.rollback()  # 发生错误后回滚

    cur.close()
    conn2db.close()
    return 'true'

def getData():
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )

    cur = conn2db.cursor()

    # sql = "SELECT `id`,`video_access_address` FROM `xvideo` where video_tag is null limit %s,%s" % (offset,limit)
    sql = "SELECT `id`,`video_access_address` FROM `xvideo` where video_tag is  null order By id desc limit %s,%s" % (offset,limit)

    cur.execute(sql)
    db_result = cur.fetchall()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result

def SavaCsv(data):
    # with open("/Applications/MAMP/htdocs/htdocs/python/houseInfo.csv", "w", newline="") as datacsv:
    # with open("/Applications/MAMP/htdocs/htdocs/python/tag.csv", "a", newline="") as datacsv:
    with open("/var/www/html/xvideo_csv/tag.csv", "a", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))

        # csvwriter.writerow(data)
        csvwriter.writerow(data)
    return 'true'

def handleCate(tmp):

    cate_array = ['video','the','3d','hentai','asmr','japanese-amateur','milf','mom','teen','wife','quality','jk','chat','anal','cartoon','person','oil','gal','gay','stocking','bisexual','etch','fucking','blow','chubby','massage','family','latin','lingerie','rape','life','racial','extension','root','ass','tits','woman','shooting','black','hair','mature','fetish','married','red','amateur','middle','gangbang']
    cate_ids = {'video':1,'the':2,'3d':3,'hentai':4,'asmr':5,'japanese-amateur':6,'milf':7,'mom':8,'teen':9,'wife':10,'quality':11,'jk':12,'chat':14,'anal':15,'cartoon':16,'person':18,'oil':19,'gal':20,'gay':21,'stocking':22,'bisexual':24,'etch':25,'fucking':26,'blow':27,'chubby':29,'massage':30,'family':31,'latin':32,'lingerie':33,'rape':34,'life':35,'racial':36,'extension':37,'root':38,'ass':39,'tits':40,'woman':41,'shooting':42,'black':43,'hair':44,'mature':45,'fetish':48,'married':50,'red':52,'amateur':53,'middle':54,'gangbang':58}
    list = [2,6,12,13,17,23,28,49,50,52,53,54,55,56,57,58]
    cate_id = ''
    if tmp == None:
        # cate_id = random.sample(list, 1)[0]
        return False
    for val in cate_array:
        result = val in tmp
        if result == True:
            cate_id = cate_ids[val]
            break
        else:
            continue
    if cate_id == '':
        return False
        # cate_id = random.sample(list, 1)[0]

    return cate_id

def handleTag(soup,data):
    if soup == None:
        return False

    views = soup.find_all(name='div',attrs={"class":"video-tags-list"})

    text = []
    if len(views) > 0:
        texts = views[0].find_all('a')
        for value in texts:
            text.append(value.get_text())

    data.append(','.join(text))
    return data

if __name__ == '__main__':

    data = getData()

    for value in data:
        time.sleep(5)

        tag = handleTag(reqPage(value[1]),[value[0]])
        if tag == False:
            print('访问失败 跳过')
        else:
            print(tag)
            saveData(tag,3)
            print('完毕')
    exit()