# -*- coding: utf-8 -*-
import execjs
import ssl
from urllib import request
from urllib import parse
import time


ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
proxy = "http://177.39.187.70:37315"

class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)

def googleTranslate(url):
    time.sleep(1)
    # proxy = 'http://178.79.46.5:59073'

    proxy_support = request.ProxyHandler({'http': proxy})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    req = request.Request(url, headers=headers)
    data = request.urlopen(req)
    html = data.read().decode("utf-8")
    needs = html.split(',')[0].split('"')
    need = needs[1]
    return need


#请求获取 翻译文字
def HandleUrl(content):
    if len(content) < 1:
        return ''
    js = Py4Js()
    tk = js.getTk(content)
    if len(content) > 4891:
        # print("翻译的长度超过限制！！！")
        return ''

    content = parse.quote(content)

    url = "https://translate.google.cn/translate_a/single?client=webapp&sl=ja&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (tk, content)


    return googleTranslate(url)

def ClearFang():
    filename = 'fangyuanInfoUpdate.csv'
    csvFile = open(filename, "w")
    csvFile.truncate()
    return True

if __name__ == '__main__':
    # content = '1億2000万円'
    # result = HandleUrl(content)

    ClearFang()
    print('sss')
    exit()