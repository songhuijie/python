# -*- coding: utf-8 -*-
import os
from  PIL import Image,ImageFont,ImageDraw

l = [1,23,4]
text = u"这是一段测试文本，test 123。{}\n ".format(l[1])
im = Image.new("RGB", (300, 50), (255, 255, 255))

dr = ImageDraw.Draw(im)
print(dr)
exit()
font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 14)
dr.text((10, 5), text, font=font, fill="#000000")
im.show()
im.save("t.png")