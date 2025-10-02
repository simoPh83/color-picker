"""
Utility modules for the Color Picker application.

This package contains platform-specific functionality and helper modules.
"""

from .platform_capture import PlatformScreenCapture
from .macos_permissions import request_permission_if_needed
from .comparisonEngine import (
    calculate_color_similarity,
    analyze_color_components,
    get_simple_color_name,
    get_top_color_matches,
    map_css_to_simple
)

__all__ = [
    'PlatformScreenCapture', 
    'request_permission_if_needed',
    'calculate_color_similarity',
    'analyze_color_components', 
    'get_simple_color_name',
    'get_top_color_matches',
    'map_css_to_simple'
]
