import requests
import json
import time
import csv

def GetListOfSingers(url):
    num = 0
    # 一个页面最多尝试请求三次
    while num < 3:
        # 请求页面信息,添加请求异常处理，防止某个页面请求失败导致整个抓取结束，
        try:
            if url:
                # 加上代理


                # req = requests.get(url, headers=headers,cookies = cookies ,proxies=proxies)
                # req = requests.get(url, headers=headers, proxies=proxies)
                req = requests.get(url)
                # req = requests.get(url, headers=headers,cookies = cookies) 带cookies
                # if req.status_code == 200:
                    # 返回BeautifulSoup对象
                return req.text
        except:
            pass
        time.sleep(3)
        num += 1

def MakeData(data):
    text = json.loads(data)

    CardMINIONArray = []
    CardSPELLArray = []
    CardweaponArray = []
    CardHEROArray = []
    for value in text:
        if value.get('type') == 'MINION':
            CardMINIONArray.append(value.get('name'))
        elif value.get('type') == 'SPELL':
            CardSPELLArray.append(value.get('name'))
        elif value.get('type') == 'WEAPON':
            CardweaponArray.append(value.get('name'))
        else:
            CardHEROArray.append(value.get('name'))

    return  [CardMINIONArray,CardSPELLArray,CardweaponArray,CardHEROArray]

def saveCsv(data):
    #添加
    # with open("/Applications/MAMP/htdocs/htdocs/python/rakumachi.csv", "w", newline="") as datacsv:
    #追加
    with open("singList.csv", "w", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        # 追加不添加头
        # csvwriter.writerow(["id", "url"])
        tmp =[]
        for i in range(len(data)):
            if i == 0:
                csvwriter.writerow(['随从'])
                csvwriter.writerow(data[i])
            elif i == 1:
                csvwriter.writerow(['法术'])
                csvwriter.writerow(data[i])
            elif i == 2:
                csvwriter.writerow(['武器'])
                csvwriter.writerow(data[i])
            else:
                csvwriter.writerow(['英雄'])
                csvwriter.writerow(data[i])

    return 'true'


def main():
    singer_url  = 'https://api.hearthstonejson.com/v1/25770/zhCN/cards.collectible.json'
    data = GetListOfSingers(singer_url)
    handle_data = MakeData(data)
    saveCsv(handle_data)

if __name__ == '__main__':
    main()