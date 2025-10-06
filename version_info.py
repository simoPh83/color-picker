# Version file for PyInstaller
# This helps antivirus software identify the executable as legitimate

from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, 
    StringStruct, VarFileInfo, VarStruct
)

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'Color Picker App'),
        StringStruct('FileDescription', 'Color Picker Utility'),
        StringStruct('FileVersion', '1.0.0.0'),
        StringStruct('InternalName', 'ColorPicker'),
        StringStruct('LegalCopyright', 'Copyright (C) 2025'),
        StringStruct('OriginalFilename', 'ColorPicker.exe'),
        StringStruct('ProductName', 'Color Picker'),
        StringStruct('ProductVersion', '1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)