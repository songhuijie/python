#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from urllib.request import urlopen
import urllib.request
from urllib import parse
import requests

import json
headers = {
    'authority':'maps.googleapis.com',
    'cache-control':'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'x-client-data': 'CLK1yQEIirbJAQijtskBCMS2yQEIqZ3KAQioo8oBCL+nygEI7KfKAQjiqMoBGPqlygE=',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

google_map_key = 'AIzaSyChLmJVGDMSu-T3JGjneu_XK6J_48fNNDY'

def getGeoForAddress(address):
    # address = "上海市中山北一路121号"

    addressUrl = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=" + google_map_key
    # addressUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address=%E5%A4%A7%E9%98%AA%E5%BA%9C%E5%A4%A7%E9%98%AA%E5%B8%82%E6%B7%80%E5%B7%9D%E5%8C%BA%E4%B8%89%E6%B4%A5%E5%B1%8B%E5%8D%97%E4%BA%8C%E4%B8%81%E7%9B%AE&key=AIzaSyChLmJVGDMSu-T3JGjneu_XK6J_48fNNDY'

    # 中文url需要转码才能识别
    # addressUrlQuote = parse.quote(addressUrl, ':?=/')
    # addressUrlQuoteHeader = urllib.request.Request(addressUrlQuote,headers=headers)
    # response = urlopen(addressUrlQuoteHeader)
    # responseJson = json.loads(response.read(), encoding='gbk')

    addressUrlQuote = parse.quote(addressUrl, ':?=/')
    response = requests.get(addressUrlQuote,headers=headers)
    responseJson = json.loads(response.text)

    print(responseJson)
    if responseJson.get('status') == 'OVER_QUERY_LIMIT':
        print('OVER_QUERY_LIMIT')
        return False
    else:
        lat = responseJson.get('results')[0]['geometry']['location']['lat']
        lng = responseJson.get('results')[0]['geometry']['location']['lng']
        print(address + '的经纬度是: %f, %f' % (lat, lng))
        return [lat, lng]

    # type of response is string
    # print(type(response))
    # type of responseJson is dict
    # print(type(responseJson))




if __name__ == '__main__':
    result = getGeoForAddress('大阪府大阪市淀川区三津屋南二丁目')
    print(result)
    exit()
