import csv
import pandas as pd
import MySQLdb
import random

db_name = 1
hang = 1
def ReadCsv(min,max,filename=None,type=1):
    if filename == None:
        f = '/Applications/MAMP/htdocs/htdocs/python/xvideos.com-db.csv'
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


    return result

def saveData(data,type):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )

    str2 = ','
    cur = conn2db.cursor()
    if type == 1:
        sql = "INSERT INTO `cate_csv` ( `cate_name`) VALUES ('%s')" % (str2.join(data))
    elif type == 2:
        sql = "INSERT INTO `cate_csv_2` ( `cate_name`) VALUES ('%s')" % (str2.join(data))
    else:
        sql = "update `xvideo_csv_%s` set `video_tag` = '%s' Where video_id = %s" % (data[2],data[1],data[0])

    # for value in range(len(data)):
    #     if value == len(data) -1:
    #         sql += " ('" + data[value] + "');"
    #     else:
    #         sql += " ('" + data[value] + "'),"

    cur.execute(sql)
    conn2db.commit()
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

    str2 = ','
    cur = conn2db.cursor()

    sql = "SELECT `id`,`video_access_address` FROM `xvideo_csv_%s`" % (db_name);

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

if __name__ == '__main__':
    # filename = '/Applications/MAMP/htdocs/htdocs/python/xvideos.com-db.csv'
    filename = '/var/www/html/xvideo_csv/xvideos.com-db.csv'


    reader = pd.read_csv(filename, sep=';',header=None,skiprows=hang,iterator=True,chunksize=1)

    for reader_array in reader:

        # array_url = []
        # array_sec = []
        # array_pic = []
        # array_tags = []
        # array_cate = []
        array = []

        for value in reader_array[6]:
            array.append(value)
        for value in reader_array[5]:
            # continue


            try:
                tags = value
                array.append(tags)
                tmp = value.split(',')[0]
                bool = handleCate(tmp)

                if bool != False:
                    array.append(bool)
            except:
                tmp = ''
                bool = handleCate(tmp)

        # for value in reader_array[7]:
        #     continue

        hang += 1

        if len(array) < 3:
            SavaCsv(array)
        else:
            saveData(array, 3)
        print(array)
        print('成功 %s 继续下次'% (hang))

    print('完毕')
    exit()