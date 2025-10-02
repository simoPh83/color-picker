#!/bin/bash
# Build script for Color Picker macOS app
# Run this script from the project root directory

set -e  # Exit on any error

echo "🔧 Building Color Picker for macOS..."
echo "======================================"

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f "color_picker.py" ]; then
    echo "❌ Error: color_picker.py not found. Please run this script from the project directory."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source venv/bin/activate
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf __pycache__/
find . -name "*.pyc" -delete

# Build the app using the spec file
echo "🔨 Building with PyInstaller spec file..."
pyinstaller build_scripts/color_picker_macos.spec --clean --noconfirm

# Check if build was successful
if [ -d "dist/ColorPicker.app" ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📁 Your app is located at: dist/ColorPicker.app"
    echo ""
    echo "📋 Next steps:"
    echo "1. Test the app: open dist/ColorPicker.app"
    echo "2. Grant screen recording permission when prompted"
    echo "3. Copy to Applications folder if it works correctly"
    echo ""
    echo "🔒 Security Note:"
    echo "The app will need screen recording permission to work properly."
    echo "macOS will prompt for this when you first run the app."
    echo ""
    
    # Get app size
    app_size=$(du -sh "dist/ColorPicker.app" | cut -f1)
    echo "📊 App size: $app_size"
    
    # Show both executable and app bundle
    echo ""
    echo "📦 Built files:"
    echo "   - ColorPicker.app (macOS app bundle - recommended)"
    echo "   - ColorPicker (command line executable)"
    echo ""
    
    # Offer to open the app
    read -p "🚀 Would you like to test the app now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🎯 Opening ColorPicker.app..."
        open "dist/ColorPicker.app"
    fi
    
else
    echo "❌ Build failed!"
    echo "Check the output above for errors."
    exit 1
fi
