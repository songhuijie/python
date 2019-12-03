# coding=UTF-8
"""
標題：展示板
功能：顯示底圖及文字。
開發人員：seakingx
建立時間：2018.11.06
最後修改：2018.11.09
python 2.7 , pyglet
"""

import pyglet

if __name__ == '__main__':
    # 背景圖片儲存在 執行檔案的 res 目錄下
    filename = r"./font/1.jpg"

    img = pyglet.image.load(filename).get_texture(rectangle=True)
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

    checks = pyglet.image.create(32, 32, pyglet.image.CheckerImagePattern())
    background = pyglet.image.TileableTexture.create_for_image(checks)

    # Enable alpha blending, required for image.blit.
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    window = pyglet.window.Window(visible=False, resizable=True, caption= u"會議展示")
    window.width = img.width
    window.height = img.height
    # 拷貝 微軟雅黑字型檔案 msyh.ttf  華文琥珀字型檔案STHUPO.ttf  到執行目錄的fonts 子目錄下
    pyglet.font.add_file(r'./font/msyh.ttf')
    pyglet.font.add_file(r'./font/STHUPO.ttf')

    # 檢查字型是否正常裝載
    # print pyglet.font.have_font(u'微軟雅黑')
    # print pyglet.font.have_font(u'華文琥珀')

    font1 = pyglet.font.load(u'微软雅黑'.encode('gbk'), 16)
    font2 = pyglet.font.load(u'华文琥珀'.encode('gbk'), 16)

    font0_name = 'Times New Roman'
    font1_name = u'微软雅黑'.encode('gbk')
    font2_name = u'华文琥珀'.encode('gbk')
    label1 = pyglet.text.Label(u'Hello, Python 測試',
                              font_name=font1_name,
                              font_size=32,
                              x=window.width // 2, y=window.height // 2 - 50,
                              anchor_x='center', anchor_y='center')
    label2 = pyglet.text.Label(u'頁面展示',
                              font_name=font2_name,
                              font_size=48,
                              color=(255,215,0,255),
                              x=window.width // 2, y=window.height // 2 + 50,
                              anchor_x='center', anchor_y='center')

    label3 = pyglet.text.Label(u'By Seakingx',
                              font_name=font0_name,
                              font_size=24,
                              x=window.width // 2 + 100, y=window.height // 2 - 110,
                              anchor_x='center', anchor_y='center')
    window.set_visible()


    @window.event
    def on_draw():
        window.clear()
        background.blit_tiled(0, 0, 0, window.width, window.height)
        img.blit(window.width // 2, window.height // 2, 0)
        label1.draw()
        label2.draw()
        label3.draw()

    pyglet.app.run()