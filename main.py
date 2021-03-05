import numpy as np
from PIL import Image
import random
import math

# https://en.wikipedia.org/wiki/Spirograph
# https://en.wikipedia.org/wiki/Epicycloid


class Epicycloid:

    def __init__(self, img, center):
        self.img = img
        self.center = center

        self.color = [255, 0, 0]

        self.o_rad = random.randrange(40, 100)
        k = random.randrange(25, 35) / random.randrange(9, 12)
        self.i_rad = self.o_rad * k

        print("R = {0}\tr = {1}".format(self.o_rad, self.i_rad))

    def draw(self):

        # Define some stuff
        teta = 0
        r = self.o_rad
        R = self.i_rad

        # Get start pos for teta = 0
        start_x = int(round(self.center[0] + (R + r) * math.cos(teta) - r * math.cos(((R + r) / r) * teta)))
        start_y = int(round(self.center[1] + (R + r) * math.sin(teta) - r * math.sin(((R + r) / r) * teta)))

        while True:

            # Calc pos
            x = self.center[0] + (R + r) * math.cos(teta) - r * math.cos(((R + r)/r) * teta)
            y = self.center[1] + (R + r) * math.sin(teta) - r * math.sin(((R + r) / r) * teta)

            # Round and draw pos
            x = int(round(x))
            y = int(round(y))
            self.img[y][x] = self.color

            # Check if at beginning of circle and check that teta is at least 2 pi
            if start_x == x and start_y == y and teta >= 2*math.pi:
                break
            else:
                # Advance teta
                teta += 0.002

def main():

    layers = 1
    width = 1600
    height = 900

    # Image
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(len(image)):
        for x in range(len(image[y])):
            image[y][x][0] = 255
            image[y][x][1] = 255
            image[y][x][2] = 255

    e = Epicycloid(image, [width/2, height/2])
    e.draw()

    data = Image.fromarray(image, 'RGB')
    data.save("Test.png")
    data.show()


if __name__ == "__main__":
    main()
