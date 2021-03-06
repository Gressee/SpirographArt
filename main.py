import numpy as np
import math
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

# https://en.wikipedia.org/wiki/Spirograph
# https://en.wikipedia.org/wiki/Epicycloid
# https://en.wikipedia.org/wiki/Hypocycloid

width = 1920
height = 1080


class Graph:

    def __init__(self, graph_style, center, min_rad, max_rad, line_width, color_style, blur_rad):
        global width, height

        # Get variables
        self.graph_style = graph_style
        self.center = center
        self.min_rad = min_rad
        self.max_rad = max_rad
        self.line_width = line_width
        self.color_style = color_style
        self.blur_rad = blur_rad

        # Init the image and drawer
        self.image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

        # Setup color
        if self.color_style == 'c':
            # Choose a color if color style is a constant color
            self.color = rand_color()
        elif self.color_style == 'a':
            # Choose a full band angle if color style is angle and the alpha value
            self.full_band_angle = random.randrange(15, 200) / 10
            self.color_alpha = random.randrange(200, 255)
        elif self.color_style == 'm':
            # Create/Choose a color map if the style is a map
            self.color_map = color_map(rand_color(), rand_color(), rand_color(), rand_color())
        else:
            print('Wrong Color style')

        # Draw the graph
        if self.graph_style == 'et':
            self.draw_epitrochoid()
        elif self.graph_style == 'ht':
            self.draw_hypotrochoid()
        else:
            print("Wroung Graph style")

        # Blur the graph
        self.image = self.image.filter(ImageFilter.GaussianBlur(self.blur_rad))

    def get_draw_color(self, x, y, teta):
        # Setup color
        if self.color_style == 'c':
            return self.color
        elif self.color_style == 'a':
            return tuple(color_angle(teta, self.full_band_angle, self.color_alpha))
        elif self.color_style == 'm':
            try:
                return tuple(self.color_map[y][x])
            except:
                return tuple((0, 0, 0, 0))

        else:
            return tuple((0, 0, 0, 0))

    def draw_epitrochoid(self):

        teta = random.randrange(0, 62) / 10  # Start angle
        r = 0  # rotating circle
        k = 0  # Factor for the relation between rotating and static circle
        d = 0  # distance between the draw point and the center of the rotating circle

        # Search for for one set until to outer circle of the epicycloid is in the dimensions
        while (k * r + r + d) < self.min_rad or (k * r + r + d) > self.max_rad:
            r = random.randrange(int(self.max_rad * 0.05), int(self.max_rad * 0.6))
            k = random.randrange(25, 50) / 10
            d = r * random.randrange(5, 30) / 10

        print("Epitrochoid: r = {0} \tk = {1} \td/r = {2}".format(r, k, d / r))

        # Get start pos for teta = 0
        start_x = int(round(self.center[0] + r * (k + 1) * math.cos(teta) - d * math.cos((k + 1) * teta)))
        start_y = int(round(self.center[1] + r * (k + 1) * math.sin(teta) - d * math.sin((k + 1) * teta)))

        while True:

            # Calc pos
            x = int(round(self.center[0] + r * (k + 1) * math.cos(teta) - d * math.cos((k + 1) * teta)))
            y = int(round(self.center[1] + r * (k + 1) * math.sin(teta) - d * math.sin((k + 1) * teta)))

            # Draw
            rad = self.line_width / 2
            self.draw.ellipse((x - rad, y - rad, x + rad, y + rad), fill=self.get_draw_color(x, y, teta))

            # Check if at beginning of circle and check that teta is at least 2 pi
            if start_x == x and start_y == y and teta >= 2 * math.pi:
                break
            else:
                # Advance teta
                teta += 0.002

    def draw_hypotrochoid(self):

        teta = random.randrange(0, 62) / 10  # Start angle
        r = 0  # rotating circle
        k = 0  # Factor for the relation between rotating and static circle
        d = 0  # distance between the draw point and the center of the rotating circle

        # Search for for one set until to outer circle of the epicycloid is in the dimensions

        while (k * r - r + d) < self.min_rad or (k * r - r + d) > self.max_rad:
            r = random.randrange(int(self.max_rad * 0.05), int(self.max_rad * 0.15))
            k = random.randrange(5, 50) / 10
            d = r * random.randrange(5, 50) / 10

        print("Hypotrochoid: r = {0} \tk = {1} \td/r = {2}".format(r, k, d / r))

        # Get start pos for teta = 0
        start_x = int(round(self.center[0] + r * (k - 1) * math.cos(teta) + d * math.cos((k - 1) * teta)))
        start_y = int(round(self.center[1] + r * (k - 1) * math.sin(teta) - d * math.sin((k - 1) * teta)))

        while True:

            # Calc pos
            x = int(round(self.center[0] + r * (k - 1) * math.cos(teta) + d * math.cos((k - 1) * teta)))
            y = int(round(self.center[1] + r * (k - 1) * math.sin(teta) - d * math.sin((k - 1) * teta)))

            # Draw
            rad = self.line_width / 2
            self.draw.ellipse((x - rad, y - rad, x + rad, y + rad), fill=self.get_draw_color(x, y, teta))

            # Check if at beginning of circle and check that teta is at least 2 pi
            if start_x == x and start_y == y and teta >= 2 * math.pi:
                break
            else:
                # Advance teta
                teta += 0.002


def rand_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Make it transparent only with a small chance
    trans = random.randrange(0, 3)
    if trans == 0:
        a = random.randint(100, 255)
    else:
        a = 255

    ret = (r, g, b, a)
    return ret


def color_angle(angle, full_band_angle, alpha):
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
                value = ((right - left) / (width - 1)) * x + left
                m[y][x][c] = int(round(value))

    return m


def compose_layers(images):
    """
    :param images: array with images objects (fist entry is the bottom layer)
    :return: alpha composed image
    """
    out = images[0]
    for i in range(len(images) - 1):
        out = Image.alpha_composite(out, images[i + 1])

    return out


def create_layer(layer_style):
    """
    In this function the basic random stuff is handled,
    like the position, the size, the blur,
    if the color should be from a map from the angle or const

    The fine tuning of the graph and what color specifically is handled in the
    canvas object itself

    :param layer_style: b - background; m - middle; f - foreground
    :return: image of the layer
    """
    global width, height

    # Set the random layer parameter stuff
    if layer_style == 'b':
        graph_style = random.choice(['et', 'ht'])
        center = [random.randrange(int(width * 0.1), int(width * 0.9)),
                  random.randrange(int(height * 0.1), int(height * 0.9))]
        min_rad = height
        max_rad = width
        line_width = random.randrange(12, 18)
        color_style = random.choice(['c', 'c', 'a', 'm', 'm'])
        blur_rad = random.randrange(8, 20)

    elif layer_style == 'm':
        graph_style = random.choice(['et', 'ht'])
        center = [random.randrange(int(width * 0.2), int(width * 0.8)),
                  random.randrange(int(height * 0.2), int(height * 0.8))]
        min_rad = height / 2
        max_rad = width / 2
        line_width = random.randrange(8, 12)
        color_style = random.choice(['c', 'a', 'm'])
        blur_rad = random.randrange(6, 12)

    elif layer_style == 'f':
        graph_style = random.choice(['et', 'ht'])
        center = [random.randrange(int(width * 0.3), int(width * 0.7)),
                  random.randrange(int(height * 0.3), int(height * 0.7))]
        min_rad = height * 0.4
        max_rad = width * 0.6
        line_width = random.randrange(3, 5)
        color_style = random.choice(['c', 'c', 'm'])
        blur_rad = random.randrange(1, 2)

    else:
        print("Wrong style")
        return None

    # Draw layer
    layer = Graph(graph_style, center, min_rad, max_rad, line_width, color_style, blur_rad)

    return layer.image


def generate_image():
    global width, height

    # Set number of layers
    b_layers = random.randrange(1, 3)
    m_layers = random.randrange(1, 3)
    f_layers = random.randrange(1, 3)

    # Background
    layers = [Image.new('RGBA', (width, height), (0, 0, 0, 255))]

    # Create background layers
    for i in range(b_layers):
        new_layer = create_layer('b')
        layers.append(new_layer)

    # Create middle layers
    for i in range(m_layers):
        new_layer = create_layer('m')
        layers.append(new_layer)

    # Create foreground layers
    for i in range(f_layers):
        new_layer = create_layer('f')
        layers.append(new_layer)

    # Combine layers
    composed_image = compose_layers(layers)

    return composed_image


if __name__ == "__main__":
    i = 0
    while True:
        print()
        img = generate_image()
        img.save('images/img_{0}.png'.format(str(i).rjust(3, '0')))
        print('Image generated')

        i += 1
