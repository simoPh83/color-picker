# -*- mode: python ; coding: utf-8 -*-

# PyInstaller spec file for Color Picker application
# This file contains all the settings needed to build the executable
# Run with: pyinstaller color_picker.spec

a = Analysis(
    ['color_picker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL._tkinter_finder',
        'PIL.ImageTk',
        'PIL.Image',
        'webcolors',
        'numpy',
        'pyautogui',
        'mss',
        'win32gui',
        'win32ui',
        'win32con',
        'pywin32'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
        'tornado',
        'zmq'
    ],
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
    name='ColorPicker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for a windowed app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an .ico file path here if you have an icon
    version_file=None,  # You can add a version file here if needed
)