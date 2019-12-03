# -*- mode: python -*-
a = Analysis(['get_cover.py'],
             pathex=['/Library/Frameworks/Python.framework/Versions/3.7/Python', '/Applications/MAMP/htdocs/htdocs/python'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='get_cover',
          debug=False,
          strip=None,
          upx=True,
          console=True )
