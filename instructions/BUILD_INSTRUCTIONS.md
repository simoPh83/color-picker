# Color Picker macOS Build Instructions

## Quick Build Command

```bash
# Navigate to project directory
cd "/Volumes/Marketing/Simone Morciano/python working folder/colour picker/color-picker"

# Activate virtual environment
source venv/bin/activate

# Run the build script
./build_macos.sh
```

## Manual Build Commands

### Option 1: Using the build script (Recommended)
```bash
./build_macos.sh
```

### Option 2: Direct PyInstaller command
```bash
# Simple build (creates both .app and executable)
pyinstaller --onedir --windowed --name=ColorPicker color_picker.py --clean --noconfirm

# Using custom spec file (if you want more control)
pyinstaller color_picker_macos.spec --clean --noconfirm
```

## Build Output

After successful build, you'll find:
- `dist/ColorPicker.app` - macOS application bundle (recommended)
- `dist/ColorPicker` - Command line executable

## App Size
- Approximately **22MB** (includes all Python dependencies)

## Dependencies Included
- ✅ Python 3.13 runtime
- ✅ tkinter (GUI framework)
- ✅ PIL/Pillow (image processing)
- ✅ NumPy (numerical operations)
- ✅ PyAutoGUI (mouse/keyboard automation)
- ✅ webcolors (color name mapping)
- ✅ MSS (multi-screen capture)
- ✅ Platform-specific capture module
- ✅ macOS permissions handler

## Installation

1. **Test the app**: `open dist/ColorPicker.app`
2. **Grant permissions** when prompted (Screen Recording)
3. **Copy to Applications**: 
   ```bash
   cp -R dist/ColorPicker.app /Applications/
   ```

## Troubleshooting

### Build Issues
- Make sure virtual environment is activated
- Install missing dependencies: `pip install -r requirements-macos.txt`
- Clean previous builds: `rm -rf build/ dist/`

### Permission Issues
- The app needs **Screen Recording** permission
- Go to: System Settings → Privacy & Security → Screen & System Audio Recording
- Add the app or Terminal to the allowed list

### App Won't Start
- Check Console.app for error messages
- Try running from Terminal: `dist/ColorPicker.app/Contents/MacOS/ColorPicker`

## Advanced Build Options

### Custom Icon
Add an icon by modifying the spec file:
```python
icon='path/to/your/icon.icns'
```

### Code Signing (for distribution)
```bash
# Sign the app bundle
codesign --deep --sign "Developer ID Application: Your Name" dist/ColorPicker.app

# Create a DMG for distribution
hdiutil create -volname "Color Picker" -srcfolder dist/ColorPicker.app -ov -format UDZO ColorPicker.dmg
```

## File Structure
```
dist/
├── ColorPicker.app/           # macOS app bundle
│   ├── Contents/
│   │   ├── Info.plist        # App metadata
│   │   ├── MacOS/
│   │   │   └── ColorPicker   # Main executable
│   │   └── Resources/        # App resources
│   └── ...
└── ColorPicker               # Standalone executable
```
