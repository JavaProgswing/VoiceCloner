# -*- mode: python ; coding: utf-8 -*-
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)

exe_name = config.get('executable_name', 'voice-cloner')

# Generate file_version.txt dynamically
version_str = config.get('version', '1.0.0.0')
try:
    version_tuple = tuple(map(int, version_str.split('.')))
except ValueError:
    version_tuple = (1, 0, 0, 0)

company_name = config.get('company_name', 'Your Company Name')
product_name = config.get('product_name', 'Your Product Name')
file_description = config.get('file_description', 'File Description')
copyright_str = config.get('copyright', 'Copyright © 2025')

version_file_content = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0,0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', '{company_name}'),
         StringStruct('FileDescription', '{file_description}'),
         StringStruct('FileVersion', '{version_str}'),
         StringStruct('InternalName', '{exe_name}'),
         StringStruct('LegalCopyright', '{copyright_str}'),
         StringStruct('OriginalFilename', '{exe_name}'),
         StringStruct('ProductName', '{product_name}'),
         StringStruct('ProductVersion', '{version_str}')])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""

with open('file_version.txt', 'w', encoding='utf-8') as f:
    f.write(version_file_content)

a = Analysis(
    ['voice_server.py'],
    pathex=[],
    binaries=[('ffmpeg.exe', '.')],
    datas=[(os.path.join('env311', 'Lib', 'site-packages', 'gruut', 'VERSION'), 'gruut'), (os.path.join('env311', 'Lib', 'site-packages', 'TTS'), 'TTS')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION')],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='file_version.txt',
)
