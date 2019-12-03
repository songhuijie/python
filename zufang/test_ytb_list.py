import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from selenium import webdriver
import time
import MySQLdb

list_url = 'https://www.youtube.com/playlist?list='
url = 'https://www.youtube.com/results?search_query='
ytb_url = 'https://www.youtube.com'
def getHTMLText(url):
    executable_path = '/Applications/MAMP/htdocs/htdocs/python/chromedriver'

    # 设置chrome浏览器无界面模式
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=https://192.241.136.113:8080')

    browser = webdriver.Chrome(executable_path=executable_path)
    # 开始请求
    browser.set_page_load_timeout(30)
    browser.set_script_timeout(30)
    need_url = browser.get(url)
    time.sleep(10)
    # 打印页面网址
    # print(need_url)
    # url = browser.get(url)
    pageSource = browser.page_source
    browser.close()
    browser.quit()
    return pageSource

def fillUnivlist(html):
        soup = BeautifulSoup(html, 'html.parser')  # 用HTML解析网址
        # tag = soup.find('a', attrs={'id': 'view-all-endpoint'})

        # links = soup.select('div',attrs={'class': 'style-scope ytd-vertical-watch-card-list-renderer'})
        linkssides = soup.select('ytd-watch-card-compact-video-renderer[class^="style-scope ytd-vertical-watch-card-list-renderer"]')

        lenlinks = len(linkssides)
        if lenlinks:
            result_url = ''
            for i in range(lenlinks):
                if i == 0:
                    result_url = linkssides[i].find('a').get('href')
                else:
                    break

            if result_url == '':
                return False
            else:
                new_str = result_url.split('list=', 1)
                if len(new_str) < 2:
                    return False
                else:
                    return list_url + new_str[1]

        else:
            return False




def getData():
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )
    cur = conn2db.cursor()
    sql = "SELECT `id`,`sing_name` FROM `singer_list` WHERE `status` = 0 limit 100"
    cur.execute(sql)
    db_result = cur.fetchall()
    conn2db.commit()
    cur.close()
    conn2db.close()
    return db_result

def updateData(id,song_lists):
    conn2db = MySQLdb.connect(
        host='127.0.0.1',  # host
        port=3306,  # 默认端口，根据实际修改
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='test',  # DB name
    )
    cur = conn2db.cursor()
    sql_update = "UPDATE `singer_list` SET `song_lists` = '%s',`status` = 1 WHERE `id` = '%s'" % (song_lists,id)
    try:
        # 执行SQL语句
        cur.execute(sql_update)
        # 提交到数据库执行
        conn2db.commit()
        print(1)
    except:
        # 发生错误时回滚
        conn2db.rollback()
        print(2)
    # 关闭数据库连接
    conn2db.close()

    return True


def main():

    result = getData()


    # ip_url= 'https://whoer.net/zh'
    # getHTMLText(ip_url)
    # print(1)
    # exit()
    for value in result:


        time.sleep(90)
        try:
            html = getHTMLText(url + value[1])
            result = fillUnivlist(html)
            print(result)
            if result == False:
                updateData(value[0], '')
                continue
            else:
                print(value[0], result)
                updateData(value[0], result)
        except Exception as e:
            print(e)
            exit()

    print('success')
    exit()
     #要访问的网址
     #获取HTML


if __name__ == '__main__':
    main()
