# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

prefix = Path(sys.prefix)
conda_bin = prefix / 'Library' / 'bin'

# Conda 的 Tcl/Tk 等 DLL 位于 Library/bin，PyInstaller 分析时默认不在 PATH 中
os.environ['PATH'] = str(conda_bin) + os.pathsep + os.environ.get('PATH', '')

_conda_dlls = [
    'tcl86t.dll',
    'tk86t.dll',
    'libmpdec-4.dll',
    'libcrypto-3-x64.dll',
    'liblzma.dll',
    'libbz2.dll',
    'zlib.dll',
]
binaries = [(str(conda_bin / dll), '.') for dll in _conda_dlls if (conda_bin / dll).exists()]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=[('locales', 'locales')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WingetGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
