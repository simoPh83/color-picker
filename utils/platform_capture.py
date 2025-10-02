"""
Platform-aware screen capture module for Color Picker
Optimizes screen capture methods based on the operating system
"""

import platform
import time
from PIL import Image, ImageGrab
from typing import Tuple, Optional

class PlatformScreenCapture:
    def __init__(self):
        self.os_type = self.detect_os()
        self.capture_method = self.get_optimal_capture_method()
        
    def detect_os(self) -> str:
        """Detect the current operating system"""
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        elif system == 'windows':
            return 'windows'
        elif system == 'linux':
            return 'linux'
        else:
            return 'unknown'
    
    def get_optimal_capture_method(self) -> str:
        """Get the optimal capture method for the current OS"""
        if self.os_type == 'macos':
            # MSS works excellently on macOS with multi-monitor support
            try:
                import mss
                return 'mss'
            except ImportError:
                return 'pil'
        elif self.os_type == 'windows':
            # Try Windows API first, then fall back to MSS/PIL
            try:
                import win32gui
                return 'win32'
            except ImportError:
                try:
                    import mss
                    return 'mss'
                except ImportError:
                    return 'pil'
        else:  # linux or unknown
            # MSS is preferred for Linux
            try:
                import mss
                return 'mss'
            except ImportError:
                return 'pil'
    
    def capture_screen_area(self, x: int, y: int, capture_size: int = 15) -> Optional[Image.Image]:
        """
        Capture a screen area around the specified coordinates
        Returns PIL Image or None if capture fails
        """
        try:
            if self.capture_method == 'mss':
                return self._capture_with_mss(x, y, capture_size)
            elif self.capture_method == 'win32':
                return self._capture_with_win32(x, y, capture_size)
            else:  # pil fallback
                return self._capture_with_pil(x, y, capture_size)
        except Exception as e:
            print(f"Screen capture failed with {self.capture_method}: {e}")
            # Try fallback method
            return self._capture_fallback(x, y, capture_size)
    
    def _capture_with_mss(self, x: int, y: int, capture_size: int) -> Image.Image:
        """Capture using MSS library (preferred for macOS/Linux)"""
        import mss
        
        half_size = capture_size // 2
        
        with mss.mss() as sct:
            monitor = {
                "top": y - half_size,
                "left": x - half_size,
                "width": capture_size,
                "height": capture_size
            }
            
            # MSS captures all monitors as one virtual desktop
            screenshot_mss = sct.grab(monitor)
            screenshot = Image.frombytes("RGB", screenshot_mss.size, screenshot_mss.bgra, "raw", "BGRX")
            
        return screenshot
    
    def _capture_with_win32(self, x: int, y: int, capture_size: int) -> Image.Image:
        """Capture using Windows API (Windows only)"""
        import win32gui
        import win32ui
        import win32con
        
        half_size = capture_size // 2
        
        # Get device context for the entire virtual screen
        hdesktop = win32gui.GetDesktopWindow()
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        mem_dc = img_dc.CreateCompatibleDC()
        
        # Create bitmap
        screenshot_bmp = win32ui.CreateBitmap()
        screenshot_bmp.CreateCompatibleBitmap(img_dc, capture_size, capture_size)
        mem_dc.SelectObject(screenshot_bmp)
        
        # Copy screen area to bitmap
        mem_dc.BitBlt((0, 0), (capture_size, capture_size), img_dc, 
                     (x - half_size, y - half_size), win32con.SRCCOPY)
        
        # Convert to PIL Image
        bmpinfo = screenshot_bmp.GetInfo()
        bmpstr = screenshot_bmp.GetBitmapBits(True)
        screenshot = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), 
                                    bmpstr, 'raw', 'BGRX', 0, 1)
        
        # Clean up
        mem_dc.DeleteDC()
        img_dc.DeleteDC()
        win32gui.ReleaseDC(hdesktop, desktop_dc)
        win32gui.DeleteObject(screenshot_bmp.GetHandle())
        
        return screenshot
    
    def _capture_with_pil(self, x: int, y: int, capture_size: int) -> Image.Image:
        """Capture using PIL ImageGrab (cross-platform fallback)"""
        half_size = capture_size // 2
        
        # Try with all_screens parameter for multi-monitor support
        try:
            bbox = (x - half_size, y - half_size, x + half_size, y + half_size)
            screenshot = ImageGrab.grab(bbox=bbox, all_screens=True)
        except Exception:
            # Fallback to single screen capture
            bbox = (x - half_size, y - half_size, x + half_size, y + half_size)
            screenshot = ImageGrab.grab(bbox=bbox)
            
        return screenshot
    
    def _capture_fallback(self, x: int, y: int, capture_size: int) -> Optional[Image.Image]:
        """Ultimate fallback using pyautogui"""
        try:
            import pyautogui
            
            half_size = capture_size // 2
            full_screenshot = pyautogui.screenshot()
            img_width, img_height = full_screenshot.size
            
            start_x = max(0, min(x - half_size, img_width - capture_size))
            start_y = max(0, min(y - half_size, img_height - capture_size))
            end_x = min(img_width, start_x + capture_size)
            end_y = min(img_height, start_y + capture_size)
            
            screenshot = full_screenshot.crop((start_x, start_y, end_x, end_y))
            return screenshot
            
        except Exception as e:
            print(f"Fallback capture failed: {e}")
            return None
    
    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get the color of a single pixel at the specified coordinates"""
        try:
            if self.capture_method == 'mss':
                return self._get_pixel_mss(x, y)
            elif self.capture_method == 'win32':
                return self._get_pixel_win32(x, y)
            else:
                return self._get_pixel_fallback(x, y)
        except Exception:
            # Fallback to pyautogui
            return self._get_pixel_fallback(x, y)
    
    def _get_pixel_mss(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get pixel color using MSS"""
        import mss
        
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            screenshot = sct.grab(monitor)
            # MSS returns BGRA, we need RGB
            bgra = screenshot.pixel(0, 0)
            return (bgra[2], bgra[1], bgra[0])  # Convert BGRA to RGB
    
    def _get_pixel_win32(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get pixel color using Windows API"""
        import win32gui
        
        hdc = win32gui.GetDC(0)
        pixel = win32gui.GetPixel(hdc, x, y)
        win32gui.ReleaseDC(0, hdc)
        
        # Convert BGR to RGB
        return ((pixel & 0xFF), ((pixel >> 8) & 0xFF), ((pixel >> 16) & 0xFF))
    
    def _get_pixel_fallback(self, x: int, y: int) -> Tuple[int, int, int]:
        """Get pixel color using pyautogui fallback"""
        import pyautogui
        return pyautogui.pixel(x, y)
    
    def get_info(self) -> dict:
        """Get information about the current platform and capture method"""
        return {
            "os_type": self.os_type,
            "capture_method": self.capture_method,
            "platform_system": platform.system(),
            "platform_version": platform.version()
        }
