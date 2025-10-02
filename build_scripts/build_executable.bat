@echo off
echo Building Color Picker executable...
echo.

REM Activate virtual environment and run PyInstaller
"D:/Python playfolder/colour picker/.venv/Scripts/python.exe" -m PyInstaller color_picker.spec --clean

echo.
if exist "dist\ColorPicker.exe" (
    echo ✓ Build successful! Executable created at: dist\ColorPicker.exe
    echo.
    echo File size:
    dir "dist\ColorPicker.exe" | find "ColorPicker.exe"
    echo.
    echo You can now run the executable from: dist\ColorPicker.exe
    echo Or copy it to any Windows machine to run without Python installed.
) else (
    echo ✗ Build failed! Check the output above for errors.
)

echo.
pause