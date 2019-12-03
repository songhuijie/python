import requests
import MySQLdb
from bs4 import BeautifulSoup
import time
import re
import struct
import logging

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',

}

proxies = {
    "https": "https://115.124.75.225:8080"
}

url = 'https://www.xvideos.com'
search_url = 'https://www.xvideos.com/?k='

db_name = 1
offset = 0
limit = 2

class Mp4info:
    def __init__(self, file):
        self.file = file
        self.seek = 0
        self.duration = 0
        self.s = requests.session()
        self.timeout = 6
        self.s.headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

    # 设置请求头  set request header
    # 传入的seek表示代表需要跳过的字节数量  use seek to skip initial data
    # 在这里进行判断是为了后续获取视频的宽高信息预留的  the condition here is for reserving space for getting the media data
    def _set_headers(self, seek, type):
        if type in ['moov', 'duration']:
            self.s.headers['Range'] = 'bytes={}-{}'.format(seek, seek + 7)

    def _send_request(self):
        try:
            data = self.s.get(url=self.file, stream=True,
                              timeout=self.timeout).raw.read()
        except requests.Timeout:
            raise '连接超时:超过6秒(默认)服务器没有响应任何数据！'  # timeout 6 seconds, the server fails to respond and assumes there is no data
        return data

    def _find_moov_request(self):
        self._set_headers(self.seek, type='moov')
        data = self._send_request()
        size = int(struct.unpack('>I', data[:4])[0])
        flag = data[-4:].decode('ascii')
        return size, flag

    def _find_duration_request(self):
        # 4+4是moov的大小和标识,跳过20个字符，直接读到time_scale，duration  # 4+4 is the first 8 characters denoting charset, skip the next 20 to time_scale and duration
        self._set_headers(seek=self.seek+4+4+20, type='duration')
        data = self._send_request()
        time_scale = int(struct.unpack('>I', data[:4])[0])
        duration = int(struct.unpack('>I', data[-4:])[0])
        return time_scale, duration

    def get_duration(self):
        while True:
            size, flag = self._find_moov_request()
            if flag == 'moov':
                time_scale, duration = self._find_duration_request()
                self.duration = duration/time_scale
                return self.duration
            else:
                self.seek += size

def reqPage(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers,proxies = proxies)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def reqHead(url):
    num = 0
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                #加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.head(url)
                #req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    return req.headers
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def getData(db_name):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )
    cur = conn2db.cursor()
    sql = "SELECT `id`,`video_access_address` FROM `xvideo_csv_%s`  where insert_time = 0 limit %s,%s"% (db_name,offset,limit)
    # sql = "SELECT `id`,`video_id`,`video_access_address`,`video_title` FROM `xvideo`  where video_duration = 0 order By id desc limit %s,%s" % (
    # offset, limit)
    cur.execute(sql)
    db_result = cur.fetchall()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result

def saveData(data):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )

    cur = conn2db.cursor()
    sql = "INSERT INTO `xvideo` ( `video_id`,`video_access_address`,`video_title`,`video_duration`,`video_cover`,`video_urlLow`,`video_urlhigh`,`video_hls`,`video_hls_url`,`views`,`cate_id`) VALUES "


    for value in range(len(data)):
        if len(data[value]) != 11:
            sql += " ('" + data[value][1] + "','" + data[value][0] + "','""', '" + str(0) +"','""','""','""', '""','""', '""', " + str(
                data[value][2]) + ")"
        else:
            sql += " ('" + data[value][1] + "','" + data[value][0] +"','" + data[value][4] +"', "+ str(data[value][7]) +",'" + data[value][10] +"','" + data[value][5] +"','" + data[value][6] +"', '"+ data[value][9] +"','"+ data[value][8] +"', "+ str(data[value][3]) +", "+ str(data[value][2]) +")"

        if value == int(len(data)) - 1 :
            sql+= ';'
        else:
            sql+= ','


    # exit()
    cur.execute(sql)
    conn2db.commit()
    cur.close()
    conn2db.close()
    return 'true'

def updateData(data,type):
    conn2db = MySQLdb.connect(
        host='172.105.209.53',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )


    cur = conn2db.cursor()
    if type == 1:
        sql = "update xvideo set views = '%s',video_title = '%s',video_urlLow = '%s',video_urlhigh = '%s',video_duration = '%s',video_hls_url = '%s',video_hls = '%s',video_cover = '%s' Where id='%s';" % (data[1],data[2],data[3],data[4],data[5],data[6],data[7], data[8], data[0])
    else:
        sql = "update xvideo set video_duration = '%s' Where id='%s';" % (
        data[1], data[0])


    try:
        cur.execute(sql)  # 执行sql语句
        conn2db.commit()  # 提交到数据库执行
    except:
        conn2db.rollback()  # 发生错误后回滚

    cur.close()
    conn2db.close()
    return 'true'

def RecordLog(msg):
    callfile = '/var/own_project/python/log/xvideo.log'
    logging.basicConfig(filename=callfile, filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    logging.info(msg)

    return True


def handleBaseUrl():
    print('s')

def handleSoup(soup,data_array,cate_id):

    lists = soup.find_all('div',{'class':'thumb-block'})

    videos = len(lists)
    if videos >= 1:
        for i in range(videos):
            array = []

            if len(data_array) < 100:
            # if i == 0:
                array.append(url + lists[i].find('a').get('href'))
                array.append(lists[i].find('a').find('img').get('data-videoid'))
                array.append(cate_id)
                data_array.append(array)
            else:
                break
    else:
        RecordLog('抓取失败')

    return data_array

def handleHls(url):
    html = reqPage(url)
    hls = []
    regex = r"NAME=\"(.*)\""

    matches = re.finditer(regex, html, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            hls.append(int(match.group(1).replace('p', '')))

    hls.sort(reverse=True)
    return ','.join('%s' %id for id in hls)

def handleContent(data,content_array):


    if data == None:
        return False

    soup = BeautifulSoup(data,'html5lib')

    views = soup.select('strong[id^="nb-views-number"]')
    if len(views) > 0:
        views_number = views[0].get_text().replace(',','')
    else:
        views_number = 0
    content_array.append(views_number)

    regex = r"""
        	html5player.set(.*)\('(.*)'\)
        	"""

    matches = re.finditer(regex, data, re.MULTILINE | re.VERBOSE)
    for matchNum, match in enumerate(matches, start=1):

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1


            if groupNum == 1 and match.group(1) == 'VideoTitle':
                content_array.append(match.group(2))
            elif groupNum == 1 and match.group(1) == 'VideoUrlLow':
                content_array.append(match.group(2))
            elif groupNum == 1 and match.group(1) == 'VideoUrlHigh':
                video_url_high = match.group(2)
                file = Mp4info(video_url_high)
                try:
                    time = int(file.get_duration() * 1000)
                except:
                    time = 0
                content_array.append(video_url_high)
                content_array.append(time)
            elif groupNum == 1 and match.group(1) == 'VideoHLS':
                video_hls = match.group(2)
                content_array.append(video_hls)
                content_array.append(handleHls(video_hls))

            elif groupNum == 1 and match.group(1) == 'ThumbUrl169':
                content_array.append(match.group(2))
            else:
                continue

    return content_array

def handleContentTwo(data,content_array):

    if data == None:
        return False

    regex = r"""
            	html5player.set(.*)\('(.*)'\)
            	"""

    matches = re.finditer(regex, data, re.MULTILINE | re.VERBOSE)
    for matchNum, match in enumerate(matches, start=1):

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            if  groupNum == 1 and match.group(1) == 'VideoUrlHigh':
                video_url_high = match.group(2)
                file = Mp4info(video_url_high)
                try:
                    time = int(file.get_duration() * 1000)
                except:
                    time = 0

                content_array.append(time)
            elif groupNum == 1 and match.group(1) == 'VideoUrlLow':
                video_url_high = match.group(2)
                file = Mp4info(video_url_high)
                try:
                    time = int(file.get_duration() * 1000)
                except:
                    time = 0

                content_array.append(time)
            else:
                time = 0
                content_array.append(time)
                continue

    return content_array

if __name__ == '__main__':


    cate_names = getData(db_name)


    print(cate_names)
    exit()
    print('开始')
    for value in cate_names:

        time.sleep(5)
        if value[3] == '':
            print(value)
            result = handleContent(reqPage(value[2]), [value[0]])
            if result == False:
                print('空数据 跳过')
                continue
            elif len(result) < 9:
                print('数据没有抓取完 跳过')
                continue
            else:
                updateData(result, 1)
        else:

            result = handleContentTwo(reqPage(value[2]), [value[0]])
            if result == False:
                print('空 跳过')
            else:
                updateData(result, 2)
                print('更新完毕 只更新了 视频长度')



    print('全部完毕')
    print('success')
    exit()