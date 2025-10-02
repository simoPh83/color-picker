# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Color Picker macOS application
This creates a standalone .app bundle for macOS with all dependencies included
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Get the directory where this spec file is located
spec_root = os.path.dirname(os.path.abspath(SPECPATH))

# Define the main script
main_script = os.path.join(spec_root, 'color_picker.py')

# Collect data files and hidden imports
datas = []
hiddenimports = []

# Collect MSS library data (for multi-screen support)
try:
    mss_datas = collect_data_files('mss')
    datas.extend(mss_datas)
    hiddenimports.extend(['mss', 'mss.factory', 'mss.darwin'])
except ImportError:
    pass

# Collect PyAutoGUI data files
try:
    pyautogui_datas = collect_data_files('pyautogui')
    datas.extend(pyautogui_datas)
    hiddenimports.extend(['pyautogui', 'pyscreeze', 'pytweening', 'pymsgbox'])
except ImportError:
    pass

# Collect PIL/Pillow data
try:
    pil_datas = collect_data_files('PIL')
    datas.extend(pil_datas)
    hiddenimports.extend(['PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageGrab'])
except ImportError:
    pass

# Collect webcolors data
try:
    webcolors_datas = collect_data_files('webcolors')
    datas.extend(webcolors_datas)
    hiddenimports.append('webcolors')
except ImportError:
    pass

# Collect NumPy
try:
    hiddenimports.extend(['numpy', 'numpy.core._methods', 'numpy.lib.format'])
except ImportError:
    pass

# macOS specific imports
if sys.platform == 'darwin':
    hiddenimports.extend([
        'PyObjC',
        'objc',
        'Foundation',
        'AppKit',
        'Quartz',
        'pyobjc_core',
        'pyobjc_framework_Cocoa',
        'pyobjc_framework_Quartz'
    ])

# Add our custom modules to hidden imports
hiddenimports.extend([
    'utils.platform_capture',
    'utils.macos_permissions'
])

# Analysis configuration
a = Analysis(
    [main_script],
    pathex=[spec_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'tornado',
        'zmq'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate files and optimize
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ColorPicker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file here if you have one
)

# Create the macOS app bundle
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ColorPicker',
)

# Create the .app bundle with proper macOS structure
app = BUNDLE(
    coll,
    name='ColorPicker.app',
    icon=None,  # You can add an .icns file here
    bundle_identifier='com.simonephmorciano.colorpicker',
    version='1.0.0',
    info_plist={
        'CFBundleName': 'Color Picker',
        'CFBundleDisplayName': 'Color Picker',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.simonephmorciano.colorpicker',
        'CFBundleExecutable': 'ColorPicker',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'CLRP',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
        'NSRequiresAquaSystemAppearance': False,
        
        # Request screen recording permission
        'NSScreenCaptureUsageDescription': 'Color Picker needs screen access to capture colors from your display.',
        'NSDesktopFolderUsageDescription': 'Color Picker needs screen recording permission to capture colors.',
        
        # Supported document types (optional)
        'CFBundleDocumentTypes': [],
        
        # App category
        'LSApplicationCategoryType': 'public.app-category.graphics-design',
        
        # Prevent App Translocation (helps with permissions)
        'NSAppleEventsUsageDescription': 'Color Picker uses AppleEvents for system integration.',
        
        # Additional permissions that might be needed
        'NSSystemAdministrationUsageDescription': 'Color Picker needs system access to capture screen colors.',
    },
)
