#!/usr/bin/env python3
"""
Test script for the new HSL-based color analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.comparisonEngine import get_HSL_hue_analysis, rgb_to_hsl

def test_hsl_analysis():
    """Test the new HSL analysis with various color pairs"""
    
    test_cases = [
        # Test case: (color1, color2, description)
        ((255, 0, 0), (255, 100, 0), "Red to Orange"),
        ((255, 0, 0), (255, 0, 100), "Red with different saturation/lightness"),
        ((100, 150, 200), (120, 170, 220), "Light blue variations"),
        ((231, 232, 230), (255, 255, 0), "Light gray to bright yellow"),
        ((128, 128, 128), (64, 64, 64), "Gray lightness change"),
        ((255, 0, 0), (0, 255, 0), "Red to Green (opposite hues)"),
        ((200, 100, 50), (220, 120, 70), "Brown variations"),
    ]
    
    print("🎨 HSL Color Analysis Test Results")
    print("=" * 60)
    
    for i, (color1, color2, description) in enumerate(test_cases, 1):
        print(f"\n{i}. {description}")
        print(f"   Color 1: RGB{color1}")
        print(f"   Color 2: RGB{color2}")
        
        # Show HSL values
        h1, s1, l1 = rgb_to_hsl(*color1)
        h2, s2, l2 = rgb_to_hsl(*color2)
        print(f"   HSL 1: H={h1:.1f}°, S={s1:.1f}%, L={l1:.1f}%")
        print(f"   HSL 2: H={h2:.1f}°, S={s2:.1f}%, L={l2:.1f}%")
        
        # Get analysis
        analysis = get_HSL_hue_analysis(color1, color2)
        print(f"   📊 Analysis: {analysis}")
        print("-" * 50)

if __name__ == "__main__":
    test_hsl_analysis()