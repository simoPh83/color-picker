"""
Color Comparison Engine

This module provides advanced color comparison and analysis functionality
for comparing two RGB colors and providing detailed similarity assessments.
"""

import webcolors


def calculate_color_similarity(color1, color2):
    """
    Calculate similarity between two RGB colors and return detailed assessment.
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
    
    Returns:
        tuple: (assessment_text, display_color) where:
            - assessment_text: String describing similarity with distance
            - display_color: Color name for UI display
    """
    if not color1 or not color2:
        return "No comparison available", "gray"
    
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
    
    # Add component analysis if colors are in the same basic category
    component_analysis = ""
    if basic_color1 == basic_color2 and distance > 5:  # Only if same category and noticeably different
        component_analysis = analyze_color_components(color1, color2)
        if component_analysis:
            assessment += f" ({component_analysis})"
    
    return f"{assessment} (D{distance:.1f})", color


def analyze_color_components(color1, color2):
    """
    Analyze which color has more of each component (red, green, blue).
    
    Args:
        color1 (tuple): RGB tuple (r, g, b) for first color
        color2 (tuple): RGB tuple (r, g, b) for second color
    
    Returns:
        str: Description of component differences, e.g., "Color 2: more red, less blue"
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