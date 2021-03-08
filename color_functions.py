from config import *
import basics

import numpy as np
import math
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

"""
All functions related to colors are in this file
"""


def get_rand_color(base_color=(-1, -1, -1, -1), color_range=(-1, -1, -1, -1)):
    """
    Generates a color in a specific range if requested
    :param base_color:  color tuple for the base to start from
    :param color_range: how much the values can differentiate from the base
    :return: color tuple
    """

    # If no range is given
    if base_color == (-1, -1, -1, -1) and color_range == (-1, -1, -1, -1):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # Make it transparent only with a small chance
        trans = random.randrange(0, 3)
        if trans == 0:
            a = random.randint(190, 255)
        else:
            a = 255

        ret = tuple((r, g, b, a))

    # If s specific range is given
    else:
        low = basics.clamp(int(round(base_color[0] - color_range[0] / 2)), 0, 255)
        high = basics.clamp(int(round(base_color[0] - color_range[0] / 2)), 0, 255)
        r = random.randint(low, high)

        low = basics.clamp(int(round(base_color[1] - color_range[1] / 2)), 0, 255)
        high = basics.clamp(int(round(base_color[1] - color_range[1] / 2)), 0, 255)
        g = random.randint(low, high)

        low = basics.clamp(int(round(base_color[2] - color_range[2] / 2)), 0, 255)
        high = basics.clamp(int(round(base_color[2] - color_range[2] / 2)), 0, 255)
        b = random.randint(low, high)

        low = basics.clamp(int(round(base_color[3] - color_range[3] / 2)), 0, 255)
        high = basics.clamp(int(round(base_color[3] - color_range[3] / 2)), 0, 255)
        a = random.randint(low, high)

        ret = tuple((r, g, b, a))

    return ret


def get_color_from_angle(angle, full_band_angle, alpha):
    """
    One color rgb value is always 0
    :param full_band_angle: at what angle the color band starts over
    :param angle: angle for which the color
    :param alpha: alpha value for the color, stays constant
    :return: color
    """

    # is the angle between "angle" and the last start point for a new color band
    # is < that full_band_angle
    relative_angle = angle
    while relative_angle > full_band_angle:
        relative_angle -= full_band_angle

    # Set red without offset and clamp to 0
    red = -(255 / ((1 / 3) * full_band_angle)) * abs(relative_angle + 0) + 255
    if red <= 0:
        # Try other function bc red should got down stay at 0 and then go up again
        red = -(255 / ((1 / 3) * full_band_angle)) * abs(relative_angle - ((3 / 3) * full_band_angle)) + 255
    elif red <= 0:
        red = 0
    red = int(round(red))

    # Set green with a 1/3 fba offset
    green = -(255 / ((1 / 3) * full_band_angle)) * abs(relative_angle - ((1 / 3) * full_band_angle)) + 255
    green = int(round(green))
    if green <= 0:
        green = 0

    # Set blue with a 2/3 fba offset
    blue = -(255 / ((1 / 3) * full_band_angle)) * abs(relative_angle - ((2 / 3) * full_band_angle)) + 255
    blue = int(round(blue))
    if blue <= 0:
        blue = 0

    r = (red, green, blue, alpha)
    return r


def generate_color_map(tl_color, tr_color, bl_color, br_color):
    """
    Makes a map with 3 input colors to get a complete map
    Colors approach linear
    :param tl_color: color at top left
    :param tr_color: color at top right
    :param bl_color: color at bottom left
    :param br_color: color at bottom right
    :return: np array with a color for every coordinate
    """

    m = np.zeros((total_height, total_width, 4), dtype=np.uint8)

    for c in range(4):
        for y in range(len(m)):

            # define the value for the most left and right edge for every new row
            left = ((bl_color[c] - tl_color[c]) / (total_height - 1)) * y + tl_color[c]
            right = ((br_color[c] - tr_color[c]) / (total_height - 1)) * y + tr_color[c]

            for x in range(len(m[y])):
                # get color for every x in the line
                value = ((right - left) / (total_width - 1)) * x + left
                m[y][x][c] = int(round(value))

    return m
