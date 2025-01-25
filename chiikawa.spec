# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['chiikawa.py'],
    pathex=[],
    binaries=[],
    datas=[('resources', 'resources')],  # 确保资源文件夹只包含必要的文件
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # 移除不必要的模块
    noarchive=True,  # 启用 noarchive 加速启动
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='chiikawa',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 确保禁用 UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 确保应用为窗口模式
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='chiikawa.app',
    icon="resources/images/rabbit-lie.png",
    bundle_identifier=None,
)