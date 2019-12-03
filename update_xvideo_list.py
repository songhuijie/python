import requests
import MySQLdb
from bs4 import BeautifulSoup
import time
import re
import struct
import logging
import redis
import json

offset = 0
limit  = 1000

cate_id = 60
corp_id = 'dingfein9qeztkhlnwaz'
corp_secret = '24AeMm-pljTU-zlCHRqEp0V-AyLw6LTVgAk4OqK9MXRy5KO0oMoxqkVhsaf5wtie'
chatId = 'chat8c41abadfb28827b720505943f1bf8ba'
redis_key = 'xvideo_update_key'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
}

proxy_ip_own = '160.19.246.55:37455'
proxies = {
    "https": "https://80.83.137.102:8888"
}

url = 'https://www.xvideos.com'
search_url = 'https://www.xvideos.com/?k=精选&sort=relevance&datef=today'

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

def reqPage(url,proxies):
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
    sql = "SELECT `id`,`video_access_address` FROM `xvideo_month`  where insert_time = 0 order By id desc limit %s,%s" % (
        offset, limit)
    cur.execute(sql)
    db_result = cur.fetchall()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result

def getDataXid(id):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )
    cur = conn2db.cursor()
    sql = "SELECT count(`id`) FROM `xvideo`  where cate_id = %s"% (
        id)
    cur.execute(sql)
    db_result = cur.fetchone()

    if db_result[0] <= 100:
        sql2 = "SELECT `video_id` FROM `xvideo`  where cate_id = %s ORDER BY id asc" % (
            id)

    else:
        sql2 = "SELECT `video_id` FROM `xvideo`  where cate_id = %s ORDER BY id desc" % (
            id)

    cur.execute(sql2)
    db_result2 = cur.fetchone()

    conn2db.commit()
    cur.close()
    conn2db.close()

    return db_result2[0]

def saveData2(id):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )
    now_time = 1
    cur = conn2db.cursor()
    sql = "UPDATE  `xvideo_month`  set `insert_time` = '%s' where id = '%s'"% (now_time,id)
    try:
        cur.execute(sql)  # 执行sql语句
        conn2db.commit()  # 提交到数据库执行
        # print('更新成功')
    except:
        # print('更新失败')
        conn2db.rollback()  # 发生错误后回滚

    cur.close()
    conn2db.close()
    return 'true'

def saveData(data):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='master',  # 用户名
        passwd='xvideo123?.qwe',  # 密码
        db='xvideo',  # DB name
        charset="utf8"
    )

    now_time = int(time.time())
    cur = conn2db.cursor()
    sql = "UPDATE  `xvideo_month`  set `video_title` = '%s',`video_duration` = '%s',`video_cover` = '%s',`video_urlLow` = '%s',`video_urlhigh` = '%s',`video_hls` = '%s',`video_hls_url` = '%s',`views` = '%s',`insert_time` = '%s',`video_tag` = '%s' where id = '%s'"% (data[2],data[5],data[8],data[3],data[4],data[7],data[6],data[1],now_time,data[9],data[0])

    # exit()

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

def RecordLog(msg):
    callfile = '/var/own_project/python/log/xvideo.log'
    logging.basicConfig(filename=callfile, filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    logging.info(msg)

    return True



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

def handleHls(url,proxies):
    html = reqPage(url,proxies)
    hls = []
    regex = r"NAME=\"(.*)\""

    matches = re.finditer(regex, html, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            hls.append(int(match.group(1).replace('p', '')))

    hls.sort(reverse=True)
    return ','.join('%s' %id for id in hls)

def handleContent(data,content_array,proxy_ip):

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
    try:
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

                    try:
                        if video_hls != '':
                            content_array.append(handleHls(video_hls, proxy_ip))
                    except:
                        print('执行try except')
                        continue

                elif groupNum == 1 and match.group(1) == 'ThumbUrl169':
                    content_array.append(match.group(2))
                else:
                    continue

        views = soup.find_all(name='div', attrs={"class": "video-tags-list"})
        text = []
        if len(views) > 0:
            texts = views[0].find_all('a')
            for value in texts:
                text.append(value.get_text())

        content_array.append(','.join(text))

        return content_array

    except Exception as e:
        print('Reason:', e)
        return False

def Dingding():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    access_token = r.get('access_token')
    # r.delete('access_token')
    # print(3)
    # exit()


    if access_token == None:
        url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' % (corp_id, corp_secret)
        response = requests.get(url)
        response_str = response.text
        response_dict = json.loads(response_str)
        error_code_key = "errcode"
        access_token_key = "access_token"

        if error_code_key in response_dict:
            error_code_bool = True
        else:
            error_code_bool = False

        if access_token_key in response_dict:
            access_token_key_bool = True
        else:
            access_token_key_bool = False

        if error_code_bool == True and response_dict[error_code_key] == 0 and access_token_key_bool ==True:
             access_token = response_dict[access_token_key]
             r.setex('access_token',7200, access_token)
             return access_token
        else:
            return False

    return access_token
    # print(access_token)

def _gen_text_msg(text):
    msg_type = 'text'
    msg = { "content": text }
    return msg_type, msg

def send_text_to_chat(access_token, chat_id, text):
    msg_type, msg = _gen_text_msg(text)
    return _send_msg_to_chat(access_token, chat_id, msg_type, msg)

def _send_msg_to_chat(access_token, chat_id, msg_type, msg):
    body_dict = {
        "chatid": chat_id,
        "msgtype": msg_type
    }
    body_dict[msg_type] = msg
    body = json.dumps(body_dict)
    print("https://oapi.dingtalk.com/chat/send?access_token=%s" %(access_token))
    response_str = requests.post("https://oapi.dingtalk.com/chat/send?access_token=%s" %(access_token), body)

    print(response_str)
    print(response_str.text)
    return response_str

def getNeedProxy():
    return proxy_ip_own
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


    proxy = r.get(redis_key)
    if proxy:
        return proxy
    else:
        proxy = getProxys()
        r.set(redis_key, proxy)
        return proxy

def getProxys():

    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

    proxy = r.lrange('proxy',0,0)
    print(r.llen('proxy'))
    if len(proxy) < 1:
        response_str = getProxydata()
        print(response_str)
        list = json.loads(response_str)
        # data = getProxydata()
        print(list)
        for value in list:
            print(value)
            r.lpush('proxy', str(value['Ip']) + ':' + str(value['Port']))

        proxy = r.lrange('proxy', 0, 0)

        r.ltrim('proxy', 1, -1)
        return proxy[0]
    else:
        r.ltrim('proxy', 1, -1)

        return  proxy[0]

def getProxydata():
    url = 'http://ged.ip3366.net/api/?key=20190829153652708&getnum=30&anonymoustype=3&filter=1&area=2&order=2&formats=2&proxytype=1'
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理

                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url, headers=headers,timeout=5)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                if req.status_code == 200:
                    # 返回BeautifulSoup对象
                    return req.text
                    # return BeautifulSoup(req.text, 'html5lib')
        except:
            pass
        time.sleep(3)
        num += 1

def changeProxy():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    proxy = getProxys()
    r.set(redis_key, proxy)
    return proxy

if __name__ == '__main__':


    data = getData()
    for value in data:
        time.sleep(5)

        proxy_ip = getNeedProxy()
        print(proxy_ip)
        proxy = {'https': ''}
        proxy['https'] = proxy_ip
        result = handleContent(reqPage(value[1],proxy),[value[0]],proxy)

        if result == False:
            print('未获取到')
            saveData2(value[0])
            # changeProxy()
            continue
        elif len(result) <= 9:
            print('获取失效')
            # changeProxy()
            continue
        else:

            saveData(result)




    # print(data)
    exit()
