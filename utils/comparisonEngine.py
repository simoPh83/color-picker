"""
Color Comparison Engine

This module provides advanced color comparison and analysis functionality
for comparing     # Add soph    # Add sop    # Add sophisticated hue analysis for all color comparisons
    # Try new HSL analysis first, fallback to original if needed
    try:
        hue_analysis = get_HSL_hue_analysis_first_neutral_only(color1, color2)
    except:
        hue_analysis = get_hue_analysis(color1, color2)
    
    # Create clipboard text from hue analysis
    clipboard_text = create_clipboard_text(hue_analysis)
    
    if hue_analysis:
        assessment += f" ({hue_analysis})"
    
    return assessment, color, clipboard_texthue analysis for all color comparisons
    # Try new HSL analysis first, fallback to original if needed
    try:
        hue_analysis = get_HSL_hue_analysis_first_neutral_only(color1, color2)
    except:
        hue_analysis = get_hue_analysis(color1, color2)
    
    # Create clipboard text from hue analysis
    clipboard_text = create_clipboard_text(hue_analysis)
    
    if hue_analysis:
        assessment += f" ({hue_analysis})"
    
    return assessment, color, clipboard_textue analysis for all color comparisons
    # Try new HSL analysis first, fallback to original if needed
    try:
        hue_analysis = get_HSL_hue_analysis_first_neutral_only(color1, color2)
    except:
        hue_analysis = get_hue_analysis(color1, color2)
    
    # Create clipboard text from hue analysis
    clipboard_text = create_clipboard_text(hue_analysis)
    
    if hue_analysis:
        assessment += f" ({hue_analysis})"
    
    return assessment, color, clipboard_textors and providing detailed similarity assessments.
"""

import webcolors
from .compare_hues import compare_colours
from .hues_lists import hues


def rgb_to_hsl(r, g, b):
    """
    Convert RGB values to HSL (Hue, Saturation, Lightness).
    
    Args:
        r, g, b (int): RGB values (0-255)
    
    Returns:
        tuple: (hue, saturation, lightness) where:
            - hue: 0-360 degrees
            - saturation: 0-100 percent
            - lightness: 0-100 percent
    """
    # Normalize RGB values to 0-1 range
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0
    
    # Find max and min values
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    
    # Calculate lightness
    lightness = (max_val + min_val) / 2.0
    
    # Calculate saturation and hue
    if max_val == min_val:
        # Achromatic (gray)
        saturation = 0.0
        hue = 0.0
    else:
        # Calculate saturation
        if lightness < 0.5:
            saturation = (max_val - min_val) / (max_val + min_val)
        else:
            saturation = (max_val - min_val) / (2.0 - max_val - min_val)
        
        # Calculate hue
        delta = max_val - min_val
        
        if max_val == r_norm:
            hue = ((g_norm - b_norm) / delta) % 6
        elif max_val == g_norm:
            hue = (b_norm - r_norm) / delta + 2
        else:  # max_val == b_norm
            hue = (r_norm - g_norm) / delta + 4
        
        hue *= 60  # Convert to degrees
    
    # Convert to percentages and ensure proper ranges
    hue = round(hue, 1)
    saturation = round(saturation * 100, 1)
    lightness = round(lightness * 100, 1)
    
    return hue, saturation, lightness


def calculate_color_similarity(color1, color2):
    """
    Calculate similarity between two RGB colors and return detailed assessment.
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
    
    Returns:
        tuple: (assessment_text, display_color, clipboard_text) where:
            - assessment_text: String describing similarity with distance
            - display_color: Color name for UI display
            - clipboard_text: Formatted text for clipboard ("tinted background: hue description")
    """
    if not color1 or not color2:
        return "No comparison available", "gray", "no comparison"
    
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    # Calculate Euclidean distance in RGB space
    distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
    
    # Get basic color categories for both colors
    color1_matches = get_simple_color_name(color1)
    color2_matches = get_simple_color_name(color2)
    
    basic_color1 = color1_matches[0][0] if color1_matches else "unknown"
    basic_color2 = color2_matches[0][0] if color2_matches else "unknown"
    
    # Provide meaningful similarity assessment
    if distance == 0:
        assessment = "Identical colors"
        color = "purple"
    elif distance < 10:
        assessment = "Nearly identical"
        color = "darkgreen"
    elif distance < 25:
        assessment = "Very similar"
        color = "green"
    elif distance < 50:
        assessment = "Similar"
        color = "olive"
    elif distance < 100:
        assessment = "Somewhat different"
        color = "orange"
    elif distance < 150:
        assessment = "Different"
        color = "darkorange"
    else:
        assessment = "Very different"
        color = "red"
    
    # Add sophisticated hue analysis for all color comparisons
    # Try new HSL analysis first, fallback to original if needed
    try:
        hue_analysis = get_HSL_hue_analysis_first_neutral_only(color1, color2)
    except:
        hue_analysis = get_hue_analysis(color1, color2)
    
    # Create clipboard text from hue analysis
    clipboard_text = create_clipboard_text(hue_analysis)
    
    if hue_analysis:
        assessment += f" ({hue_analysis})"
    
    return f"{assessment} (D{distance:.1f})", color, clipboard_text


def analyze_color_components(color1, color2):
    """
    Legacy function kept for backward compatibility.
    Now uses sophisticated hue analysis instead of simple RGB differences.
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
    
    Returns:
        str: Description of hue relationship
    """
    return get_hue_analysis(color1, color2)


def get_hue_analysis(color1, color2):
    """
    Analyze hue relationship between two colors using sophisticated hue quantization.
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
    
    Returns:
        str: Description of hue relationship
    """
    try:
        # Convert RGB tuples to lists for the compare_colours function
        color1_list = list(color1)
        color2_list = list(color2)
        
        # Use 12 subdivisions for good balance between accuracy and readability
        hue_comparison = compare_colours(color1_list, color2_list, 12)
        
        if len(hue_comparison) == 1:
            # Identical hues
            return f"same hue: {hue_comparison[0]}"
        elif len(hue_comparison) == 2:
            # Different hue categories
            return f"hue shift: {hue_comparison[0]} → {hue_comparison[1]}"
        elif len(hue_comparison) == 3:
            # Same hue category but leaning towards another
            return f"{hue_comparison[0]} leaning towards {hue_comparison[2]}"
        else:
            return ""
    except Exception as e:
        # Fallback to basic RGB analysis if hue analysis fails
        return get_basic_rgb_analysis(color1, color2)


def get_HSL_hue_analysis_first_neutral_only(color1, color2, hue_threshold=5, saturation_threshold=10, lightness_threshold=10):
    """
    Analyze HSL differences between two colors with only first color checked for neutrality.
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
        hue_threshold (float): Threshold in degrees for significant hue change
        saturation_threshold (float): Threshold in percentage for significant saturation change
        lightness_threshold (float): Threshold in percentage for significant lightness change
    
    Returns:
        str: Description like "hue: neutral -> orange (+15.9deg), saturation: +2%, lightness: -1%"
    """
    try:
        # Convert both colors to HSL
        h1, s1, l1 = rgb_to_hsl(*color1)
        h2, s2, l2 = rgb_to_hsl(*color2)
        
        # Analyze hue with NEW logic: only first color checked for neutrality + achromatic zone
        hue_analysis = analyze_hue_direction_first_neutral_only(h1, h2, hue_threshold, saturation1=s1, saturation2=s2, color1_rgb=color1, color2_rgb=color2)
        
        # Analyze saturation change
        saturation_diff = s2 - s1
        if abs(saturation_diff) < saturation_threshold:
            saturation_analysis = "same"
        else:
            sign = "+" if saturation_diff > 0 else ""
            saturation_analysis = f"{sign}{saturation_diff:.0f}%"
        
        # Analyze lightness change
        lightness_diff = l2 - l1
        if abs(lightness_diff) < lightness_threshold:
            lightness_analysis = "same"
        else:
            sign = "+" if lightness_diff > 0 else ""
            lightness_analysis = f"{sign}{lightness_diff:.0f}%"
        
        # Combine analysis
        components = []
        components.append(f"hue: {hue_analysis}")
        components.append(f"saturation: {saturation_analysis}")
        components.append(f"lightness: {lightness_analysis}")
        
        return ", ".join(components)
        
    except Exception as e:
        # Fallback to basic RGB analysis
        return get_basic_rgb_analysis(color1, color2)


def get_HSL_hue_analysis(color1, color2, hue_threshold=1, saturation_threshold=10, lightness_threshold=10):
    """
    Analyze HSL differences between two colors with sophisticated hue direction analysis.
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
        hue_threshold used to be 15, testing at 1 now
        hue_threshold (float): Threshold in degrees for significant hue change
        saturation_threshold (float): Threshold in percentage for significant saturation change
        lightness_threshold (float): Threshold in percentage for significant lightness change
    
    Returns:
        str: Description like "hue: same, saturation: +20%, lightness: -15%"
    """
    try:
        # Convert both colors to HSL
        h1, s1, l1 = rgb_to_hsl(*color1)
        h2, s2, l2 = rgb_to_hsl(*color2)
        
        # Analyze hue with direction using hues_list and saturation awareness
        hue_analysis = analyze_hue_direction(h1, h2, hue_threshold, saturation1=s1, saturation2=s2)
        
        # Analyze saturation change
        saturation_diff = s2 - s1
        if abs(saturation_diff) < saturation_threshold:
            saturation_analysis = "same"
        else:
            sign = "+" if saturation_diff > 0 else ""
            saturation_analysis = f"{sign}{saturation_diff:.0f}%"
        
        # Analyze lightness change
        lightness_diff = l2 - l1
        if abs(lightness_diff) < lightness_threshold:
            lightness_analysis = "same"
        else:
            sign = "+" if lightness_diff > 0 else ""
            lightness_analysis = f"{sign}{lightness_diff:.0f}%"
        
        # Combine analysis
        components = []
        components.append(f"hue: {hue_analysis}")
        components.append(f"saturation: {saturation_analysis}")
        components.append(f"lightness: {lightness_analysis}")
        
        return ", ".join(components)
        
    except Exception as e:
        # Fallback to basic RGB analysis
        return get_basic_rgb_analysis(color1, color2)


def get_simple_color_from_hsl(hue_degrees, saturation_percent, subdivisions=12, neutral_threshold=10):
    """
    Get simple color name considering both hue and saturation.
    
    Args:
        hue_degrees (float): Hue in degrees (0-360)
        saturation_percent (float): Saturation as percentage (0-100)
        subdivisions (int): Which hue list to use
        neutral_threshold (float): Saturation threshold below which colors are considered neutral
    
    Returns:
        str: Simple color name or 'neutral' for low-saturation colors
    """
    # If saturation is very low, consider it neutral regardless of hue
    if saturation_percent < neutral_threshold:
        return "neutral"
    
    # Otherwise, use the hue-based mapping
    hue_name = get_hue_name_from_degrees(hue_degrees, subdivisions)
    return hue_to_simple_color(hue_name)


def analyze_hue_direction_first_neutral_only(hue1, hue2, threshold=15, subdivisions=12, saturation1=None, saturation2=None, color1_rgb=None, color2_rgb=None):
    """
    Analyze hue direction change where only the FIRST color is checked for neutrality.
    Second color always shows its actual hue-based color name.
    Includes achromatic zone logic for nearly gray colors.
    
    Args:
        hue1, hue2 (float): Hue values in degrees (0-360)
        threshold (float): Minimum difference to consider significant
        subdivisions (int): Which hue list to use (6, 12, or 24)
        saturation1, saturation2 (float): Saturation percentages for neutral detection
        color1_rgb, color2_rgb (tuple): RGB tuples for achromatic zone RGB distance calculation
    
    Returns:
        str: Direction analysis like "neutral -> orange (+15.9deg)" or "same" or "similar grays"
    """
    # ACHROMATIC ZONE LOGIC: Check if both colors are essentially grays
    if saturation1 is not None and saturation2 is not None and color1_rgb is not None and color2_rgb is not None:
        # If both colors have very low saturation, check for very similar grays only
        if saturation1 < 10 and saturation2 < 10:
            # Calculate RGB distance
            import math
            rgb_distance = math.sqrt(sum((a-b)**2 for a, b in zip(color1_rgb, color2_rgb)))
            
            # Only handle the most similar achromatic cases
            if rgb_distance < 10:
                return "same"  # Very similar grays
            # For all other cases, fall through to regular hue direction logic
    
    # Handle achromatic colors (grays) - legacy check
    if hue1 == 0 and hue2 == 0:
        return "neutral"
    
    # Calculate circular hue difference
    hue_diff = hue2 - hue1
    
    # Normalize to [-180, 180] range for circular distance
    if hue_diff > 180:
        hue_diff -= 360
    elif hue_diff < -180:
        hue_diff += 360
    
    # NEW LOGIC: Only first color checked for neutrality
    if saturation1 is not None:
        # First color: check for neutrality based on saturation
        display1 = get_simple_color_from_hsl(hue1, saturation1, subdivisions, neutral_threshold=10)
    else:
        # Fallback: use hue-based name
        hue1_name = get_hue_name_from_degrees(hue1, subdivisions)
        display1 = hue_to_simple_color(hue1_name)
    
    # Second color: ALWAYS use hue-based name (ignore saturation for neutrality)
    hue2_name = get_hue_name_from_degrees(hue2, subdivisions)
    display2 = hue_to_simple_color(hue2_name)
    
    # Check if difference is significant
    if abs(hue_diff) < threshold:
        return "same"
    
    # If both colors are in the same simple color category, show directional movement
    if display1 == display2:
        # Get the next color in the direction of movement
        direction_is_clockwise = hue_diff > 0
        next_simple = get_next_simple_color_in_direction(hue2, direction_is_clockwise, subdivisions)
        
        if next_simple != display1:
            # Show movement toward the next color category using consistent " -> " notation
            return f"{display1} -> {next_simple} ({hue_diff:+.1f}deg)"
        else:
            # Fallback to basic directional description
            direction = "clockwise" if hue_diff > 0 else "counter-clockwise"
            return f"{display1} ({direction} {abs(hue_diff):.1f}deg)"
    
    # Show transition from first to second (different categories)
    return f"{display1} -> {display2} ({hue_diff:+.1f}deg)"


def analyze_hue_direction(hue1, hue2, threshold=15, subdivisions=12, saturation1=None, saturation2=None):
    """
    Analyze hue direction change using simple color categories, considering saturation for neutrals.
    
    Args:
        hue1, hue2 (float): Hue values in degrees (0-360)
        threshold (float): Minimum difference to consider significant
        subdivisions (int): Which hue list to use (6, 12, or 24)
        saturation1, saturation2 (float): Saturation percentages for better neutral detection
    
    Returns:
        str: Direction analysis using simple color names
    """
    # Handle achromatic colors (grays)
    if hue1 == 0 and hue2 == 0:
        return "neutral"
    
    # Calculate circular hue difference
    hue_diff = hue2 - hue1
    
    # Normalize to [-180, 180] range for circular distance
    if hue_diff > 180:
        hue_diff -= 360
    elif hue_diff < -180:
        hue_diff += 360
    
    # Get BOTH display names (saturation-aware) AND underlying hue categories
    if saturation1 is not None and saturation2 is not None:
        # Display names (what user sees)
        display1 = get_simple_color_from_hsl(hue1, saturation1, subdivisions)
        display2 = get_simple_color_from_hsl(hue2, saturation2, subdivisions)
        
        # Underlying hue categories (for direction analysis)
        hue1_name = get_hue_name_from_degrees(hue1, subdivisions)
        hue2_name = get_hue_name_from_degrees(hue2, subdivisions)
        underlying1 = hue_to_simple_color(hue1_name)
        underlying2 = hue_to_simple_color(hue2_name)
    else:
        # Fallback to hue-only analysis
        hue1_name = get_hue_name_from_degrees(hue1, subdivisions)
        hue2_name = get_hue_name_from_degrees(hue2, subdivisions)
        display1 = underlying1 = hue_to_simple_color(hue1_name)
        display2 = underlying2 = hue_to_simple_color(hue2_name)
    
    # If absolutely no difference, return same
    if abs(hue_diff) == 0:
        return f"same ({display1})"
    
    # Use underlying hue categories to determine if we should show direction or transition
    use_underlying_logic = (underlying1 == underlying2)
    
    # For ANY difference (even tiny ones), show directional movement
    if abs(hue_diff) < threshold:
        if use_underlying_logic:
            # Same underlying hue category - show direction (this is the key fix!)
            direction_is_clockwise = hue_diff > 0
            next_simple = get_next_simple_color_in_direction(hue2, direction_is_clockwise, subdivisions)
            
            if next_simple != underlying1:
                # Use "leaning towards" for small movements, "shifting to" for larger ones
                if abs(hue_diff) < (threshold / 3):
                    direction_word = "leaning towards"
                else:
                    direction_word = "shifting to"
                # Use display name for first color, but show direction to next color
                return f"{display1} {direction_word} {next_simple} ({hue_diff:+.1f}deg)"
            else:
                direction = "clockwise" if hue_diff > 0 else "counter-clockwise"
                return f"{display1} ({direction} {abs(hue_diff):.1f}deg)"
        else:
            # Different underlying categories - show direct transition using display names
            return f"{display1} -> {display2} ({hue_diff:+.1f}deg)"
    
    # Larger differences
    if use_underlying_logic:
        # Same underlying category but significant angular difference
        direction_is_clockwise = hue_diff > 0
        next_simple = get_next_simple_color_in_direction(hue2, direction_is_clockwise, subdivisions)
        
        if next_simple != underlying1:
            return f"{display1} shifting to {next_simple} ({hue_diff:+.1f}deg)"
        else:
            direction = "clockwise" if hue_diff > 0 else "counter-clockwise"
            return f"{display1} ({direction} {abs(hue_diff):.1f}deg)"
    else:
        # Different underlying categories - show direct transition
        return f"{display1} -> {display2} ({hue_diff:+.1f}deg)"


def get_hue_name_from_degrees(hue_degrees, subdivisions=12):
    """
    Get hue name from degrees using hues_list.
    
    Args:
        hue_degrees (float): Hue in degrees (0-360)
        subdivisions (int): Which hue list to use
    
    Returns:
        str: Hue name
    """
    if subdivisions not in hues:
        subdivisions = 12  # Default fallback
    
    hue_names = hues[subdivisions][0]
    hue_values = hues[subdivisions][1]
    
    # Handle neutral/achromatic
    if hue_degrees == 0:
        return "neutral"
    
    # Find closest hue
    min_distance = 360
    closest_index = 0
    
    for i, hue_value in enumerate(hue_values):
        # Calculate circular distance
        distance = abs(hue_degrees - hue_value)
        if distance > 180:
            distance = 360 - distance
        
        if distance < min_distance:
            min_distance = distance
            closest_index = i
    
    hue_name = hue_names[closest_index]
    
    # Remove apostrophe from Red' if present
    if hue_name.endswith("'"):
        hue_name = hue_name[:-1]
    
    return hue_name


def hue_to_simple_color(hue_name):
    """
    Convert hue wheel names to simple color categories using direct names from hues_lists.
    
    Args:
        hue_name (str): Hue name from the hue wheel
    
    Returns:
        str: Simple color category name (lowercase)
    """
    # Clean up name (remove apostrophe)
    clean_name = hue_name.replace("'", "") if hue_name else ""
    
    # Convert to lowercase for consistency
    return clean_name.lower()


def create_clipboard_text(hue_analysis):
    """
    Create formatted clipboard text from hue analysis.
    
    Args:
        hue_analysis (str): Hue analysis string like "neutral -> orange (+15.9deg)"
    
    Returns:
        str: Formatted clipboard text like "tinted background: neutral -> orange" or empty string for "same"
    """
    if not hue_analysis:
        return ""
    
    # Extract the hue part by finding text before first comma or parenthesis
    if ", " in hue_analysis:
        hue_part = hue_analysis.split(", ")[0]
    else:
        hue_part = hue_analysis
    
    # Remove "hue: " prefix if present
    if hue_part.startswith("hue: "):
        hue_part = hue_part[5:]
    
    # Remove degree measurements with regex
    import re
    hue_part = re.sub(r'\s*\([^)]*deg[^)]*\)', '', hue_part)
    
    # Return empty string for "same" cases - no meaningful change to copy
    if hue_part.strip() == "same":
        return ""
    
    return f"tinted background: {hue_part.strip()}"


def get_next_simple_color_in_direction(hue_degrees, clockwise=True, subdivisions=12):
    """
    Get the next simple color category when moving in the specified direction on the hue wheel.
    
    Args:
        hue_degrees (float): Current hue in degrees
        clockwise (bool): Direction to move (True = clockwise, False = counter-clockwise)
        subdivisions (int): Which hue list to use
    
    Returns:
        str: Next simple color category in the specified direction
    """
    if subdivisions not in hues:
        subdivisions = 12
    
    hue_names = hues[subdivisions][0]
    hue_values = hues[subdivisions][1]
    
    # Find current position
    current_index = 0
    min_distance = 360
    
    for i, hue_value in enumerate(hue_values):
        distance = abs(hue_degrees - hue_value)
        if distance > 180:
            distance = 360 - distance
        if distance < min_distance:
            min_distance = distance
            current_index = i
    
    # Get current simple color
    current_hue_name = hue_names[current_index]
    current_simple = hue_to_simple_color(current_hue_name)
    
    # Move in the specified direction to find the next different simple color
    step = 1 if clockwise else -1
    
    for offset in range(1, len(hue_names)):
        next_index = (current_index + (step * offset)) % len(hue_names)
        next_hue_name = hue_names[next_index]
        next_simple = hue_to_simple_color(next_hue_name)
        
        # Return the first different simple color we encounter
        if next_simple != current_simple:
            return next_simple
    
    # If we've gone full circle without finding a different simple color
    return current_simple


def get_adjacent_hue_name(hue_degrees, clockwise=True, subdivisions=12):
    """
    Get the adjacent hue name in the specified direction.
    
    Args:
        hue_degrees (float): Current hue in degrees
        clockwise (bool): Direction to move
        subdivisions (int): Which hue list to use
    
    Returns:
        str: Adjacent hue name or None
    """
    if subdivisions not in hues:
        subdivisions = 12
    
    hue_names = hues[subdivisions][0]
    hue_values = hues[subdivisions][1]
    
    # Find current position
    current_index = 0
    min_distance = 360
    
    for i, hue_value in enumerate(hue_values):
        distance = abs(hue_degrees - hue_value)
        if distance > 180:
            distance = 360 - distance
        if distance < min_distance:
            min_distance = distance
            current_index = i
    
    # Get adjacent index
    if clockwise:
        adjacent_index = (current_index + 1) % len(hue_names)
    else:
        adjacent_index = (current_index - 1) % len(hue_names)
    
    adjacent_name = hue_names[adjacent_index]
    
    # Remove apostrophe if present
    if adjacent_name.endswith("'"):
        adjacent_name = adjacent_name[:-1]
    
    return adjacent_name


def get_basic_rgb_analysis(color1, color2):
    """
    Fallback RGB component analysis for when hue analysis fails.
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
    
    Returns:
        str: Description of component differences
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    # Calculate differences in each component
    red_diff = r2 - r1
    green_diff = g2 - g1
    blue_diff = b2 - b1
    
    # Find the most significant difference (threshold of 10 to avoid noise)
    threshold = 10
    components = []
    
    if abs(red_diff) > threshold:
        if red_diff > 0:
            components.append("more red")
        else:
            components.append("less red")
    
    if abs(green_diff) > threshold:
        if green_diff > 0:
            components.append("more green")
        else:
            components.append("less green")
    
    if abs(blue_diff) > threshold:
        if blue_diff > 0:
            components.append("more blue")
        else:
            components.append("less blue")
    
    # Return the most significant differences (max 2 to keep it readable)
    if components:
        return "Color 2: " + ", ".join(components[:2])
    return ""


def get_simple_color_name(rgb):
    """
    Convert RGB to simple color name using scientific CSS3 color matching.
    
    Args:
        rgb (tuple): RGB tuple (r, g, b)
    
    Returns:
        list: List of (simple_name, css_name, distance) tuples for top matches
    """
    try:
        # Find the closest CSS3 colors and return top 3
        return get_top_color_matches(rgb)
    except Exception:
        # Fallback to basic detection
        return [("unknown", "unknown", 999)]


def get_top_color_matches(rgb, top_n=3):
    """
    Get top N closest color matches using CSS3 colors (deduplicated by RGB values).
    
    Args:
        rgb (tuple): RGB tuple (r, g, b) to match
        top_n (int): Number of top matches to return
    
    Returns:
        list: List of (simple_name, css_name, distance) tuples
    """
    target_r, target_g, target_b = rgb
    distances = []
    seen_rgb = set()  # Track RGB values we've already seen
    
    # Get all CSS3 color names
    css3_names = webcolors.names('css3')
    
    for name in css3_names:
        try:
            css_rgb = webcolors.name_to_rgb(name, spec='css3')
            css_r, css_g, css_b = css_rgb
            
            # Skip if we've already seen this exact RGB value
            rgb_tuple = (css_r, css_g, css_b)
            if rgb_tuple in seen_rgb:
                continue
            seen_rgb.add(rgb_tuple)
            
            # Calculate Euclidean distance
            distance = ((target_r - css_r) ** 2 + 
                       (target_g - css_g) ** 2 + 
                       (target_b - css_b) ** 2) ** 0.5
            
            # Map to simple color name
            simple_name = map_css_to_simple(name)
            distances.append((distance, simple_name, name, css_rgb))
            
        except ValueError:
            continue
    
    # Sort by distance and return top matches
    distances.sort()
    return [(simple_name, css_name, distance) for distance, simple_name, css_name, css_rgb in distances[:top_n]]


def map_css_to_simple(css_name):
    """
    Map CSS3 color names to simple color names.
    
    Args:
        css_name (str): CSS3 color name
    
    Returns:
        str: Simple color category name
    """
    css_name = css_name.lower()
    
    # Comprehensive mapping from CSS colors to simple names
    color_mapping = {
        # Reds
        'red': 'red', 'darkred': 'red', 'crimson': 'red', 'firebrick': 'red',
        'indianred': 'red', 'lightcoral': 'red', 'salmon': 'red', 'darksalmon': 'red',
        'lightsalmon': 'red', 'tomato': 'red', 'orangered': 'red',
        
        # Oranges
        'orange': 'orange', 'darkorange': 'orange', 'coral': 'orange', 
        'chocolate': 'orange', 'sandybrown': 'orange', 'peru': 'orange',
        'sienna': 'orange', 'saddlebrown': 'orange',
        
        # Yellows
        'yellow': 'yellow', 'gold': 'yellow', 'khaki': 'yellow', 'darkkhaki': 'yellow',
        'palegoldenrod': 'yellow', 'goldenrod': 'yellow', 'darkgoldenrod': 'yellow',
        'lightyellow': 'yellow', 'lemonchiffon': 'yellow', 'lightgoldenrodyellow': 'yellow',
        'papayawhip': 'yellow', 'moccasin': 'yellow', 'peachpuff': 'yellow',
        'wheat': 'yellow', 'navajowhite': 'yellow',
        
        # Yellow-Greens (the key ones!)
        'burlywood': 'yellow-green', 'tan': 'yellow-green', 'greenyellow': 'yellow-green', 
        'yellowgreen': 'yellow-green', 'olivedrab': 'yellow-green',
        'darkolivegreen': 'yellow-green', 'olive': 'yellow-green',
        
        # Greens
        'green': 'green', 'darkgreen': 'green', 'forestgreen': 'green', 'limegreen': 'green',
        'lime': 'green', 'seagreen': 'green', 'mediumseagreen': 'green', 'springgreen': 'green',
        'mediumspringgreen': 'green', 'darkseagreen': 'green', 'lightgreen': 'green',
        'palegreen': 'green', 'lawngreen': 'green', 'chartreuse': 'green',
        
        # Blues
        'blue': 'blue', 'darkblue': 'blue', 'mediumblue': 'blue', 'navy': 'blue',
        'midnightblue': 'blue', 'royalblue': 'blue', 'steelblue': 'blue',
        'dodgerblue': 'blue', 'deepskyblue': 'blue', 'cornflowerblue': 'blue',
        'skyblue': 'blue', 'lightskyblue': 'blue', 'lightsteelblue': 'blue',
        'lightblue': 'blue', 'powderblue': 'blue', 'cadetblue': 'blue',
        'aqua': 'blue', 'cyan': 'blue', 'lightcyan': 'blue', 'paleturquoise': 'blue',
        'aquamarine': 'blue-green', 'turquoise': 'blue-green', 'mediumturquoise': 'blue-green',
        'darkturquoise': 'blue-green', 'lightseagreen': 'blue-green', 'teal': 'blue-green',
        'darkcyan': 'blue-green',
        
        # Purples and Magentas
        'purple': 'purple', 'indigo': 'purple', 'darkviolet': 'purple', 'darkorchid': 'purple',
        'darkmagenta': 'magenta', 'violet': 'purple', 'plum': 'purple', 'thistle': 'purple',
        'orchid': 'purple', 'mediumorchid': 'purple', 'mediumpurple': 'purple',
        'blueviolet': 'purple', 'slateblue': 'purple', 'darkslateblue': 'purple',
        'mediumslateblue': 'purple', 'magenta': 'magenta', 'fuchsia': 'magenta',
        'deeppink': 'magenta', 'hotpink': 'pink', 'lightpink': 'pink', 'pink': 'pink',
        'mistyrose': 'pink', 'lavenderblush': 'pink',
        
        # Browns
        'brown': 'brown', 'maroon': 'brown', 'rosybrown': 'brown',
        
        # Grays and Whites
        'white': 'white', 'snow': 'white', 'honeydew': 'white', 'mintcream': 'white',
        'azure': 'white', 'aliceblue': 'white', 'ghostwhite': 'white', 'whitesmoke': 'white',
        'seashell': 'white', 'beige': 'white', 'oldlace': 'white', 'floralwhite': 'white',
        'ivory': 'white', 'antiquewhite': 'white', 'linen': 'white', 'lavender': 'white',
        'black': 'black', 'dimgray': 'gray', 'dimgrey': 'gray', 'gray': 'gray', 'grey': 'gray',
        'darkgray': 'gray', 'darkgrey': 'gray', 'silver': 'gray', 'lightgray': 'gray',
        'lightgrey': 'gray', 'gainsboro': 'gray', 'slategray': 'gray', 'slategrey': 'gray',
        'lightslategray': 'gray', 'lightslategrey': 'gray', 'darkslategray': 'gray',
        'darkslategrey': 'gray',
    }
    
    return color_mapping.get(css_name, css_name)