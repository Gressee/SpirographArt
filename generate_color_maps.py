from config import *
from color_functions import *

import os
import numpy as np
import math
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

"""
Script is only run to generate a few nice color maps 
to save processing power later.
"""


def get_max_color_map_index():
    # Get the highest index in the color map dir
    max_index = 0

    map_dir = "color_maps" + path_spacer + "{0}x{1}".format(width, height) + path_spacer
    files = os.listdir(map_dir)

    for file in files:
        index = int(file.replace('map_', '').replace('.png', ''))
        if index > max_index:
            max_index = index

    return max_index


def main():
    map_dir = "color_maps" + path_spacer + "{0}x{1}".format(width, height) + path_spacer
    index = get_max_color_map_index() + 1

    color_range = (150, 150, 150, 30)

    while True:
        base_color = get_rand_color()

        """color_map = generate_color_map(get_rand_color(base_color=base_color, color_range=color_range),
                                       get_rand_color(base_color=base_color, color_range=color_range),
                                       get_rand_color(base_color=base_color, color_range=color_range),
                                       get_rand_color(base_color=base_color, color_range=color_range))
        """

        color_map = generate_color_map(get_rand_color(),
                                       get_rand_color(),
                                       get_rand_color(),
                                       get_rand_color())

        color_map = Image.fromarray(color_map, 'RGBA')
        color_map.save("{0}map_{1}.png".format(map_dir, str(index).rjust(3, '0')))
        index += 1

        print("Generated color map with base: {0}".format(base_color))





if __name__ == '__main__':
    main()
