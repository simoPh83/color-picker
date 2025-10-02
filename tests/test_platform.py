#!/usr/bin/env python3
"""
Test script to verify platform-aware screen capture functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.platform_capture import PlatformScreenCapture
import pyautogui

def test_platform_detection():
    """Test platform detection and capture methods"""
    print("=== Platform Detection Test ===")
    
    # Initialize the capture system
    capture = PlatformScreenCapture()
    
    # Get platform info
    info = capture.get_info()
    print(f"Detected OS: {info['os_type']}")
    print(f"Capture Method: {info['capture_method']}")
    print(f"Platform System: {info['platform_system']}")
    print(f"Platform Version: {info['platform_version']}")
    
    print("\n=== Screen Capture Test ===")
    
    # Test screen capture at center of screen
    try:
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        print(f"Screen size: {screen_width}x{screen_height}")
        print(f"Testing capture at center: ({center_x}, {center_y})")
        
        # Test area capture
        screenshot = capture.capture_screen_area(center_x, center_y, 15)
        if screenshot:
            print(f"✅ Area capture successful: {screenshot.size}")
        else:
            print("❌ Area capture failed")
        
        # Test pixel capture
        pixel_color = capture.get_pixel_color(center_x, center_y)
        print(f"✅ Pixel color at center: RGB{pixel_color}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n=== Performance Comparison ===")
    
    # Compare with pyautogui
    import time
    
    # Test our method
    start_time = time.time()
    for _ in range(10):
        capture.get_pixel_color(center_x, center_y)
    our_time = time.time() - start_time
    
    # Test pyautogui method
    start_time = time.time()
    for _ in range(10):
        pyautogui.pixel(center_x, center_y)
    pyautogui_time = time.time() - start_time
    
    print(f"Our method (10 calls): {our_time:.4f}s")
    print(f"PyAutoGUI method (10 calls): {pyautogui_time:.4f}s")
    print(f"Speed ratio: {pyautogui_time/our_time:.2f}x")

if __name__ == "__main__":
    test_platform_detection()
