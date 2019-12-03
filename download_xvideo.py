# -*- coding: utf-8 -*-
import requests
from contextlib import closing
import os


def download_file(url, path):
    with closing(requests.get(url, stream=True)) as r:
        chunk_size = 1024
        content_size = int(r.headers['content-length'])
        print('下载开始')
        with open(path, "wb") as f:
            n = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                loaded = n*1024.0/content_size
                f.write(chunk)
                print( '已下载{0:%}'.format(loaded))
                n += 1


if __name__ == '__main__':
    url = 'https://vid-egc.xvideos-cdn.com/videos/mp4/8/2/2/xvideos.com_82233a41c781ad73137684b636d1cb6d.mp4?aW6BPLEWkmU3WzbVThVfefrJUPeLIUzXndbIxbvjEFL4xzKXSjhT-OTvyo2njjSDo4O6h4LjXePLypEmBARzvQ6-vmYJ67Zuy3SlcSDeN71iZCyNeBAVcLxONQ0DnN_ZrqgGljdsqHUbqVutGk-ssIIadLA3r4AlCxNBBuot51_e_sK3kY10fN2_rkIwjby5j9zFZW2rjGY&ui=MTcyLjEwNC45MC4xNC0vdmlkZW80NTk1NDAwNS9f'
    path = '/Applications/MAMP/htdocs/htdocs/python/data/video/c.mp4'
    download_file(url, path)