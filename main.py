import numpy as np
import math
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

# https://en.wikipedia.org/wiki/Spirograph
# https://en.wikipedia.org/wiki/Epicycloid
# https://en.wikipedia.org/wiki/Hypocycloid

width = 3840
height = 2160
layers = 1


class Canvas:

    def __init__(self):
        global width, height

        # Init the image and drawer
        self.image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

        self.color_map = color_map((255, 0, 0, 100),
                                   (0, 255, 0, 255),
                                   (0, 0, 255, 255),
                                   (255, 0, 0, 200))

    def draw_circle(self, x, y, rad, color):
        draw = ImageDraw.Draw(self.image)
        draw.ellipse((x-rad, y-rad, x+rad, y+rad), fill=color)

    def draw_epicycloid(self, max_rad, min_rad, center, line_width):

        # Start angle
        teta = 0

        # Outer circle
        r = 0

        # Factor for the relation between outer and inner circle
        k = 0

        # Search for for one set until to outer circle of the epicycloid is in the dimensions
        while (2*r + k*r) < min_rad or (2*r + k*r) > max_rad:
            r = random.randrange(int(max_rad * 0.05), int(max_rad * 0.6))
            k = random.randrange(5, 50)/10

        # Get start pos for teta = 0
        start_x = int(round(center[0] + r*(k + 1) * math.cos(teta) - r * math.cos((k + 1) * teta)))
        start_y = int(round(center[1] + r*(k + 1) * math.sin(teta) - r * math.sin((k + 1) * teta)))

        while True:

            # Calc pos
            x = int(round(center[0] + r * (k + 1) * math.cos(teta) - r * math.cos((k + 1) * teta)))
            y = int(round(center[1] + r * (k + 1) * math.sin(teta) - r * math.sin((k + 1) * teta)))

            # Draw
            rad = line_width/2
            try:
                color = tuple(self.color_map[y][x])
            except:
                color = (0, 0, 0, 255)
            self.draw.ellipse((x-rad, y-rad, x+rad, y+rad), fill=color)

            # Check if at beginning of circle and check that teta is at least 2 pi
            if start_x == x and start_y == y and teta >= 2 * math.pi:
                break
            else:
                # Advance teta
                teta += 0.002

    def draw_hypocycloid(self, max_rad, min_rad, center, line_width):

        # Start angle
        teta = 0

        # rotating circle
        r = 0

        # Factor for the relation between rotating and static circle
        k = 0

        # Search for for one set until to outer circle of the epicycloid is in the dimensions
        while (k*r) < min_rad or (k*r) > max_rad:
            r = random.randrange(int(max_rad * 0.05), int(max_rad * 0.2))
            k = random.randrange(5, 50)/10
            # k = random.randrange(5, 10) / random.randrange(5, 15)

        # Get start pos for teta = 0
        start_x = int(round(center[0] + r*(k - 1) * math.cos(teta) + r * math.cos((k - 1) * teta)))
        start_y = int(round(center[1] + r*(k - 1) * math.sin(teta) - r * math.sin((k - 1) * teta)))

        while True:

            # Calc pos
            x = int(round(center[0] + r * (k - 1) * math.cos(teta) + r * math.cos((k - 1) * teta)))
            y = int(round(center[1] + r * (k - 1) * math.sin(teta) - r * math.sin((k - 1) * teta)))

            # Draw
            rad = line_width/2
            self.draw.ellipse((x-rad, y-rad, x+rad, y+rad), fill=color_angle(teta, 60, 255))

            # Check if at beginning of circle and check that teta is at least 2 pi
            if start_x == x and start_y == y and teta >= 2 * math.pi:
                break
            else:
                # Advance teta
                teta += 0.002


def color_angle(angle, full_band_angle, alpha):
    """
    One color rgb value is always 0
    :param alpha: alpha value for the color, stays constant
    :param full_band_angle: at what angle the color band starts over
    :param angle: angle for which the color
    :return: color
    """

    # is the angle between "angle" and the last start point for a new color band
    # is < that full_band_angle
    relative_angle = angle
    while relative_angle > full_band_angle:
        relative_angle -= full_band_angle

    # Set red without offset and clamp to 0
    red = -(255/((1/3) * full_band_angle)) * abs(relative_angle + 0) + 255
    if red <= 0:
        # Try other function bc red should got down stay at 0 and then go up again
        red = -(255 / ((1 / 3) * full_band_angle)) * abs(relative_angle - ((3/3) * full_band_angle)) + 255
    elif red <= 0:
        red = 0
    red = int(round(red))

    # Set green with a 1/3 fba offset
    green = -(255 / ((1 / 3) * full_band_angle)) * abs(relative_angle - ((1/3) * full_band_angle)) + 255
    green = int(round(green))
    if green <= 0:
        green = 0

    # Set blue with a 2/3 fba offset
    blue = -(255 / ((1 / 3) * full_band_angle)) * abs(relative_angle - ((2/3) * full_band_angle)) + 255
    blue = int(round(blue))
    if blue <= 0:
        blue = 0

    r = (red, green, blue, alpha)
    return r


def color_map(tl_color, tr_color, bl_color, br_color):
    """
    Makes a map with 3 input colors to get a complete map
    Colors approach linear
    :param tl_color: color at top left
    :param tr_color: color at top right
    :param bl_color: color at bottom left
    :param br_color: color at bottom right
    :return: np array with a color for every coordinate
    """

    global width, height

    m = np.zeros((height, width, 4), dtype=np.uint8)

    for c in range(4):
        for y in range(len(m)):

            # define the value for the most left and right edge for every new row
            left = ((bl_color[c] - tl_color[c]) / (height - 1)) * y + tl_color[c]
            right = ((br_color[c] - tr_color[c]) / (height - 1)) * y + tr_color[c]

            for x in range(len(m[y])):

                # get color for every x in the line
                value = ((right-left)/(width-1)) * x + left
                m[y][x][c] = value

    return m


def main():
    global width, height, layers

    for i in range(3):
        c = Canvas()
        c.draw_epicycloid(height/2 + 200, height/2 - 200, (width/2, height/2), 20)
        c.image = c.image.filter(ImageFilter.GaussianBlur(radius=20))
        # c.image.show()
        c.image.save("test_images/img{0}.png".format(str(i).rjust(2, '0')))
        print('Generated image')




if __name__ == "__main__":
    main()
