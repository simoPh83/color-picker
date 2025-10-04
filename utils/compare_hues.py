from .hues_lists import hues
def hue_quantize(colour, hue_subdivisions=12):
    """Returns a list with hue value, hue name, quantized hue value.
    The 'colour' argument is a list with rgb values,
    the 'hue_subdivisions' argument decides which hue list to use from hues_lists.py"""

    # Make hue a global variable
    hue = 0

    # colours divisions : "6": secondaries, "12": tertiaries, "24": quaternaries
    if hue_subdivisions in hues:
        hue_names = hues[hue_subdivisions][0]
        hue_values = hues[hue_subdivisions][1]
    else:
        hue_names = []
        hue_values = []

    # Normalise RGB
    colour_n = []
    for i in range(3):
        colour_n.append(colour[i]/255)
    r_n = colour_n[0]
    g_n = colour_n[1]
    b_n = colour_n[2]

    # Identify max and min
    max_value = max(colour_n)
    min_value = min(colour_n)
    max_index = colour_n.index(max_value)

    # Formula to get Hue value from RGB
    # If max == 0 it's black, hue = 0
    if max_value == min_value:
        hue = 0
        closest_hue_name = "neutral"
        closest_hue_value = 0
    else:
        # Max is red
        if max_index == 0:
            hue = (g_n - b_n) / (max_value - min_value)
        # Max is green
        elif max_index == 1:
            hue = 2.0 + (b_n - r_n) / (max_value - min_value)
        # Max is blue
        elif max_index == 2:
            hue = 4.0 + (r_n - g_n) / (max_value - min_value)

        # Convert to degrees
        hue *= 60
        if hue <= 0:
            hue += 360

        # Find closest hue
        min_distance = 360
        closest_hue_name = ""

        # Find the closest colour in the list

        for i in range(len(hue_values)):
            distance = hue - hue_values[i]
            if abs(distance) < min_distance:
                min_distance = distance
                closest_hue_index = i
        closest_hue_name = hue_names[closest_hue_index]
        closest_hue_value = hue_values[closest_hue_index]


        # Remove "'" in "Red'", if closest to 360°
        if closest_hue_name == "Red'":
            closest_hue_name = closest_hue_name[:-1]

    # returns a list with the original hue value, the quantized hue name and quantized hue value
    return [hue, f"{closest_hue_name}", closest_hue_value]


def compare_colours(first_colour, second_colour, hue_subdivisions=12):
    """Compares two lists of RGB values and returns a list.
    If the hues are exactly the same it returns a single element with the hue name;
    if the hues are different enough to fall into different hue names it returns a two elements list
    with the first and second hue's name;
    if the hues are similar enough to have the same name it returns a list with three elements:
    the first hue's name, the second hue's name (which will be the same) and the name of the hue
    towards the second hue is leaning into, compared to the first one.
    Args: first_colour and second_colour are lists of RGB values,
    hue_subdivisions decides which hue list to use from hues_list.py"""

    # Quantise the two colours based on chosen list and therefore accuracy
    colour1_data = hue_quantize(first_colour, hue_subdivisions)
    colour2_data = hue_quantize(second_colour, hue_subdivisions)

    # Choose accuracy by addressing the right list of hue names and values
    if hue_subdivisions in hues:
        hue_names = hues[hue_subdivisions][0]
        hue_values = hues[hue_subdivisions][1]
    else:
        hue_names = []
        hue_values = []

    # Get the index of the closest hue in the chosen list
    hue2_index = hue_values.index(colour2_data[2])


    # Get the difference in hue values
    hue_difference = float(colour2_data[0]) - colour1_data[0]
    # If the hues are exactly the same return a single hue name
    if hue_difference == 0:
        return [colour2_data[1]]
    else:
        # Invert the leaning direction to account for the wrapping of the hues list (Red)
        if colour1_data[2] == hue_values[0] or colour2_data[2] == hue_values[0]:
            wrap = -1
        else:
            wrap = 1
        # If the hues fall in the same hue name within the chosen accuracy
        if colour1_data[1] == colour2_data[1]:
            # If the second hue is in front of the first, it is leaning towards the next hue name in the list
            if hue_difference < 0:
                lean = hue_names[(hue2_index - (1 * wrap)) % len(hue_names)]
                # Remove "'" in the hue name, if closest to 360°,
                # to make it equal to the first hue name in the list (closest to 0°)
                if lean == hue_names[-1]:
                    lean = lean[:-1]
            # If the second hue is behind the first, it is leaning towards the previous hue name in the list
            elif hue_difference > 0:
                lean = hue_names[(hue2_index + (1 * wrap)) % len(hue_names)]
                # Remove "'" in the hue name, if closest to 360°,
                # to make it equal to the first hue name in the list (closest to 0°)
                if lean == hue_names[-1]:
                    lean = lean[:-1]
            # Return the first and second hue names (which are the same)
            # and the hue name towards the second is leaning into
            return [colour1_data[1], colour2_data[1], lean]
        # If the hues are different enough, given the chosen accuracy, to fall into different hue names
        # return the first and the second hue names
        else:
            return [colour1_data[1], colour2_data[1]]
