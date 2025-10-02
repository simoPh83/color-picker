#!/usr/bin/env python3
"""
Simple test to verify button styling on macOS
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from utils.platform_capture import PlatformScreenCapture

def test_button_styles():
    """Test the button styling approach"""
    
    # Create a simple test window
    root = tk.Tk()
    root.title("Button Style Test")
    root.geometry("400x200")
    
    # Initialize platform capture to get OS info
    screen_capture = PlatformScreenCapture()
    platform_info = screen_capture.get_info()
    
    # Get button styles (same logic as in color_picker.py)
    if platform_info['os_type'] == 'macos':
        button_style = {
            'relief': 'raised',
            'borderwidth': 2,
            'font': ('Arial', 10, 'bold'),
            'fg': 'black'
        }
    else:
        button_style = {
            'bg': '#4CAF50',
            'fg': 'white'
        }
    
    # Create test buttons
    label = tk.Label(root, text=f"Testing on: {platform_info['os_type']}", font=('Arial', 12))
    label.pack(pady=10)
    
    pick_btn = tk.Button(root, text="Pick", width=8, height=1, **button_style)
    pick_btn.pack(pady=5)
    
    dual_btn = tk.Button(root, text="2", width=2, height=1, **button_style)
    dual_btn.pack(pady=5)
    
    # Test with system default (no custom styling)
    default_btn = tk.Button(root, text="System Default", font=('Arial', 10, 'bold'))
    default_btn.pack(pady=5)
    
    # Add instructions
    instructions = tk.Label(root, text="Are all button texts visible?", font=('Arial', 10))
    instructions.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_button_styles()
