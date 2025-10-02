"""
macOS Screen Recording Permission Helper
"""

import subprocess
import sys
import platform

def check_screen_recording_permission():
    """Check if the app has screen recording permission on macOS"""
    if platform.system() != 'Darwin':
        return True  # Not macOS, no permission needed
    
    try:
        # Try to capture a small area of the screen
        import mss
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 10, "height": 10}
            screenshot = sct.grab(monitor)
            
        # If we can capture, check if it's just the wallpaper
        # A real screen capture should have some variation
        from PIL import Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        
        # Simple test: if all pixels are the same, it might be wallpaper-only
        pixels = list(img.getdata())
        unique_colors = len(set(pixels))
        
        if unique_colors < 3:
            return False  # Likely wallpaper only
        
        return True
        
    except Exception:
        return False

def show_permission_dialog():
    """Show a dialog explaining how to grant screen recording permission"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        message = """Screen Recording Permission Required

The Color Picker needs permission to capture your screen content.

To grant permission:
1. Open System Preferences/Settings
2. Go to Security & Privacy → Privacy
3. Select "Screen Recording" from the left panel
4. Click the lock icon and enter your password
5. Add "Terminal" (or the app you're running Python from)
6. Restart the Color Picker

Would you like me to open System Preferences for you?"""

        result = messagebox.askyesno("Permission Required", message)
        
        if result:
            # Open System Preferences to Privacy settings
            subprocess.run(['open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture'])
        
        root.destroy()
        return result
        
    except ImportError:
        print("Screen Recording Permission Required!")
        print("Please grant screen recording permission in System Preferences")
        return False

def request_permission_if_needed():
    """Check permissions and request if needed"""
    if not check_screen_recording_permission():
        print("⚠️  Screen recording permission not granted or limited")
        show_permission_dialog()
        return False
    return True

if __name__ == "__main__":
    if request_permission_if_needed():
        print("✅ Screen recording permission is working")
    else:
        print("❌ Screen recording permission needed")
