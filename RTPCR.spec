# -*- mode: python -*-
a = Analysis(['RTPCR.py'],
             pathex=['C:\\Users\\Beth Cimini\\Desktop\\CellProfilerStats'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='RTPCR.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
