# coding:utf-8
import struct
import requests


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
        except Exception as e:
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



if __name__ == '__main__':
    url = 'https://vid3-l3.xvideos-cdn.com/videos/mp4/7/f/a/xvideos.com_7fae08fdb37ab5f92184fbc7a37a1e20.mp4?e=1564653655&ri=1024&rs=85&h=c6ef2729e40846c0c2f9d744363926df'
    file = Mp4info(url)
    try:
        time = int(file.get_duration() * 1000)
    except:
        time = 0

    print(time)
    exit()