import platform
import sys

def get_screenshot_method():
    """Determine the best screenshot method based on the operating system"""
    os_name = platform.system().lower()
    
    if os_name == 'windows':
        try:
            import win32gui
            return 'win32'
        except ImportError:
            return 'pil'
    elif os_name == 'darwin':  # macOS
        return 'mss'  # MSS works well on macOS
    elif os_name == 'linux':
        return 'mss'  # MSS is good for Linux
    else:
        return 'pil'  # Fallback for unknown systems

def capture_screen_area_optimized(x, y, capture_size=15):
    """Optimized screen capture based on OS"""
    half_size = capture_size // 2
    method = get_screenshot_method()
    
    if method == 'win32':
        # Windows-specific implementation
        return capture_with_win32(x, y, capture_size)
    elif method == 'mss':
        # MSS implementation (good for macOS/Linux)
        return capture_with_mss(x, y, capture_size)
    else:
        # PIL fallback
        return capture_with_pil(x, y, capture_size)
