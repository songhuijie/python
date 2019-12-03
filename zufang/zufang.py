import requests
from bs4 import BeautifulSoup
import time
import csv

fang_url = 'https://cd.zu.fang.com/house-a0132/'

proxies = {
    # "http": "http://178.79.46.5:59073"
    "http": "http://111.13.134.22:80"
}

def GetListOfSingers(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理


                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                req = requests.get(url,  proxies=proxies)
                # req = requests.get(url, headers=headers)
                # req = requests.get(url)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                # if req.status_code == 200:
                    # 返回BeautifulSoup对象
                return BeautifulSoup(req.text, 'html5lib')
                # return req.text
        except:
            pass
        time.sleep(3)
        num += 1


def saveCsv(data):
    #添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/rakumachi.csv", "w", newline="") as datacsv:
    #追加
    with open("zufang.csv", "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp =[]


        csvwriter.writerows(data)

    return 'true'

def main():


    soup = GetListOfSingers(fang_url)
    links = soup.select('dl[class^="list hiddenMap rel"]')
    # links = soup.find('div', attrs={'class': 'houseList'})

    result =[]
    for value in links:

        if value.find('dd') != None:
            result.append(value.find('dd').get_text().replace("\n",'').replace(" ",''))
        else:
            continue

    saveCsv(result)


if __name__ == '__main__':
    main()