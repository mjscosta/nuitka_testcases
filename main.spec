# -*- mode: python -*-
import package1.packaging.pyinstaller_specs as specs
block_cipher = None

a = Analysis(['main_tracker.py'],
             pathex=[os.path.join('.'),],
             binaries=None,
             datas=specs.datas,
             hiddenimports=specs.hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a = specs.processAnalysis(a)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')
