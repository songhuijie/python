import csv
import pandas as pd
import MySQLdb
import random

hang = 83014
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
        sql = "INSERT INTO `xvideo_csv_%s` ( `video_id`,`video_access_address`,`video_duration`,`video_cover`,`cate_id`) VALUES ('%s','%s','%s','%s','%s')" % (data[4],data[3],data[0],data[1],data[2],data[4])

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


def handleCate(tmp):

    cate_array = ['video','the','3d','hentai','asmr','japanese-amateur','milf','mom','teen','wife','quality','jk','chat','anal','cartoon','person','oil','gal','gay','stocking','bisexual','etch','fucking','blow','chubby','massage','family','latin','lingerie','rape','life','racial','extension','root','ass','tits','woman','shooting','black','hair','mature','fetish','married','red','amateur','middle','gangbang']
    cate_ids = {'video':1,'the':2,'3d':3,'hentai':4,'asmr':5,'japanese-amateur':6,'milf':7,'mom':8,'teen':9,'wife':10,'quality':11,'jk':12,'chat':14,'anal':15,'cartoon':16,'person':18,'oil':19,'gal':20,'gay':21,'stocking':22,'bisexual':24,'etch':25,'fucking':26,'blow':27,'chubby':29,'massage':30,'family':31,'latin':32,'lingerie':33,'rape':34,'life':35,'racial':36,'extension':37,'root':38,'ass':39,'tits':40,'woman':41,'shooting':42,'black':43,'hair':44,'mature':45,'fetish':48,'married':50,'red':52,'amateur':53,'middle':54,'gangbang':58}
    list = [2,6,12,13,17,23,28,49,50,52,53,54,55,56,57,58]
    cate_id = ''
    if tmp == None:
        cate_id = random.sample(list, 1)[0]
    for val in cate_array:
        result = val in tmp
        if result == True:
            cate_id = cate_ids[val]
            break
        else:
            continue
    if cate_id == '':
        cate_id = random.sample(list, 1)[0]

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
        for value in reader_array[0]:
            array.append(value)
            # continue
        for value in reader_array[2]:
            new_value  = int(value.replace(' sec', '')) * 1000
            array.append(new_value)
            # continue
        for value in reader_array[3]:
            # continue
            array.append(value)
        for value in reader_array[6]:
            array.append(value)
        for value in reader_array[5]:
            # continue


            try:
                tmp = value.split(',')[0]
                cate_id = handleCate(tmp)
                array.append(cate_id)
            except:
                tmp = ''
                cate_id = handleCate(tmp)
                array.append(cate_id)
        # for value in reader_array[7]:
        #     continue

        hang += 1


        # saveData(array_cate_2,2)
        print(array)
        saveData(array,3)
        print('成功 %s 继续下次'% (hang))

    print('完毕')
    exit()