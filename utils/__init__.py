"""
Utility modules for the Color Picker application.

This package contains platform-specific functionality and helper modules.
"""

from .platform_capture import PlatformScreenCapture
from .macos_permissions import request_permission_if_needed

__all__ = ['PlatformScreenCapture', 'request_permission_if_needed']
