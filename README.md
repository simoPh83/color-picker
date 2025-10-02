# 🎨 Professional Color Picker# Simple Color Picker Tool



A sophisticated dual-mode color picker application with scientific color detection, built with Python and Tkinter.A Windows-compatible color picker tool that identi```
color-picker/
├── color_picker.py           # Main application
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── platform_capture.py  # OS-aware screen capture
│   └── macos_permissions.py # macOS permission handling
├── tests/                    # Test files
│   ├── test_buttons.py
│   └── test_platform.py
├── requirements/             # Dependency files
│   ├── requirements.txt
│   └── requirements-macos.txt
├── build_scripts/           # Build tools
│   ├── build_macos.sh
│   ├── color_picker_macos.spec
│   └── build_executable.ps1
├── instructions/            # Documentation
└── venv/                   # Virtual environment (created)
```olors using simple names (red, green, blue, etc.) rather than fancy names.



![Color Picker Demo](https://img.shields.io/badge/Platform-Windows-blue.svg)## Features

![Python Version](https://img.shields.io/badge/Python-3.7+-green.svg)

![License](https://img.shields.io/badge/License-MIT-yellow.svg)- **GUI Version**: Easy-to-use graphical interface

- **CLI Version**: Command-line version for continuous color monitoring

## ✨ Features- **Simple Color Names**: Returns basic color names like "red", "green", "yellow-green" instead of complex names

- **Multiple Formats**: Shows RGB values, hex codes, and color names

### 🔍 **Dual-Mode Color Picking**- **Copy to Clipboard**: Easy copying of color values

- **Single Mode**: Pick individual colors with detailed analysis- **Real-time Picking**: Click anywhere on screen to pick colors

- **Dual Mode**: Compare two colors side-by-side with intelligent similarity assessment

## Installation

### 🧪 **Scientific Color Detection**

- **CSS3 Standard**: Uses scientific CSS3 color database for accurate color naming1. Make sure Python 3.7+ is installed

- **Color-Blind Friendly**: Perfect for users with color vision deficiencies2. Install required packages:

- **Smart Matching**: Euclidean distance algorithm for precise color identification   ```bash

   pip install pyautogui webcolors pillow numpy

### 🔬 **Intelligent Color Comparison**   ```

- **Similarity Assessment**: "Nearly identical", "Very similar", "Different", etc.

- **Component Analysis**: Shows which color is "more blue", "more red", etc.## Usage

- **Delta Values**: Precise numerical distance measurements (Δ)

- **Smart Logic**: Only shows component analysis for same-category colors### GUI Version (Recommended)



### 🔧 **Professional Tools**Run the graphical color picker:

- **Live Magnifier**: Real-time magnification with crosshairs for pixel-perfect picking```bash

- **Multi-Monitor Support**: Works seamlessly across multiple displayspython color_picker.py

- **Copy Functionality**: One-click copy RGB and HEX values to clipboard```

- **Spacebar Activation**: Ergonomic hands-free color picking

**How to use:**

### 🎯 **Perfect UI/UX**1. Click the "Pick Color" button

- **Compact Design**: Professional, space-efficient interface2. Your cursor will change to a crosshair

- **Static Layout**: Mode toggle button never moves between modes3. Click anywhere on your screen to pick a color

- **Aligned Controls**: RGB/HEX buttons perfectly aligned with their color panels4. The tool will show:

- **Auto-Reset**: Second panel automatically clears when starting new comparisons   - Color preview

   - RGB values (e.g., R: 255, G: 0, B: 0)

## 🚀 Quick Start   - Hex code (e.g., #FF0000)

   - Simple color name (e.g., "Red")

### Option 1: Run the Executable (Recommended)5. Use "Copy RGB" or "Copy Hex" buttons to copy values to clipboard

1. Download `color_picker.exe` from the [Releases](../../releases) page6. Press ESC to cancel color picking

2. Double-click to run - no installation required!

### CLI Version

### Option 2: Run from Source

1. **Clone the repository:**Run the command-line version for continuous monitoring:

   ```bash```bash

   git clone https://github.com/yourusername/professional-color-picker.gitpython color_picker_cli.py

   cd professional-color-picker```

   ```

**How to use:**

2. **Install dependencies:**1. Move your mouse over any color on screen

   ```bash2. The terminal will continuously show the color information

   pip install -r requirements.txt3. Press Ctrl+C to exit

   ```

## Color Mapping

3. **Run the application:**

   ```bashThe tool maps colors to these simple names:

   python color_picker.py

   ```### Primary Colors

- **Red**: Pure red tones

## 📋 Requirements- **Green**: Pure green tones  

- **Blue**: Pure blue tones

```

pyautogui>=0.9.54### Secondary Colors

webcolors>=1.13- **Yellow**: Yellow tones

Pillow>=10.0.0- **Orange**: Orange tones

numpy>=1.24.0- **Purple**: Purple/violet tones

mss>=7.0.1- **Pink**: Pink tones

pywin32>=306

```### Mixed Colors

- **Yellow-Green**: Greenish yellow or yellowish green

## 🎮 How to Use- **Blue-Green**: Teal, cyan-like colors

- **Red-Purple**: Magenta-like colors

### Single Mode

1. Click **"Pick"** button### Neutral Colors

2. Move mouse to desired color- **Black**: Very dark colors

3. Press **Spacebar** to capture- **White**: Very light colors

4. View detailed color information and copy RGB/HEX values- **Gray**: Neutral gray tones

- **Brown**: Brown tones

### Dual Mode

1. Click **"2"** button (bottom-left) to enter dual mode### Special

2. Click **"Pick"** button- **Unknown**: Colors that don't fit clear categories

3. Move mouse to first color and press **Spacebar**

4. Move mouse to second color and press **Spacebar**## Files

5. View intelligent color comparison with similarity analysis

- `color_picker.py`: Main GUI application

### Controls- `color_picker_cli.py`: Command-line version

- **Spacebar**: Pick color at mouse position- `README.md`: This documentation

- **Escape**: Cancel picking process

- **RGB/HEX buttons**: Copy values to clipboard## Tips

- **"1"/"2" button**: Toggle between single/dual mode

1. **For GUI version**: The tool works by detecting mouse clicks, so make sure to actually click (don't just hover)

## 🔬 Color Comparison Examples2. **For CLI version**: Just hover your mouse over colors to see their information in real-time

3. **Accuracy**: The tool works best with distinct colors; very subtle color differences might be classified similarly

- `"Nearly identical (Δ8.1)"` - Very close colors4. **Windows Compatibility**: Fully tested on Windows 10/11

- `"Very similar (Color 2: more blue, less red) (Δ23.4)"` - Same category with component analysis

- `"Different (Δ125.7)"` - Different color categories## Troubleshooting

- `"Identical colors (Δ0.0)"` - Perfect match

1. **"No module named 'pyautogui'"**: Run `pip install pyautogui webcolors pillow numpy`

## 🛠️ Building from Source2. **Permission errors**: Make sure Python has permission to access the screen

3. **Color picking not working**: Try running as administrator if you have issues

To create your own executable:

## Color Detection Algorithm

```bash

# Install PyInstallerThe tool uses a custom algorithm that:

pip install pyinstaller1. First checks if the color is grayscale (black/white/gray)

2. Then identifies primary colors (red/green/blue) by checking dominance

# Build executable3. Identifies secondary colors by checking color combinations

pyinstaller --onefile --windowed --hidden-import=PIL._tkinter_finder --hidden-import=webcolors --hidden-import=mss color_picker.py4. Finally identifies mixed colors for in-between cases

```

This ensures you get simple, understandable color names rather than obscure color terminology.
## 📁 Project Structure

```
professional-color-picker/
├── color_picker.py          # Main application
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── .gitignore             # Git ignore rules
└── LICENSE                # MIT License
```

## 🎯 Technical Highlights

- **Multi-Monitor Support**: Windows API integration for seamless screen capture
- **Scientific Accuracy**: CSS3 color database with 147 named colors
- **Performance Optimized**: Threaded live preview with 20 FPS magnifier updates
- **Error Resilient**: Multiple fallback methods for screen capture
- **Memory Efficient**: Smart resource management and cleanup

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- Built with Python and Tkinter
- Color detection powered by [webcolors](https://github.com/ubernostrum/webcolors)
- Screen capture using [PyAutoGUI](https://github.com/asweigart/pyautogui) and [MSS](https://github.com/BoboTiG/python-mss)
- Image processing with [Pillow](https://github.com/python-pillow/Pillow)

## 🔗 Links

- **Repository**: [GitHub](https://github.com/yourusername/professional-color-picker)
- **Issues**: [Report a Bug](../../issues)
- **Releases**: [Download Latest](../../releases)

---

**Made with ❤️ for designers, developers, and color enthusiasts!**