import numpy as np
from PIL import Image
import random
import math


class Epicycloid:
    # https://en.wikipedia.org/wiki/Epicycloid

    def __init__(self, img, center):
        self.img = img
        self.center = center

        self.color = [255, 0, 0]

        self.o_rad = random.randrange(20, 40)
        self.i_rad = self.o_rad * random.randrange(2,4)

        print("R = {0}\tr = {1}".format(self.o_rad, self.i_rad))

    def draw(self):
        teta = 0
        r = self.o_rad
        R = self.i_rad

        while teta <= 20:

            # Calc pos
            x = self.center[0] + (R + r) * math.cos(teta) - r * math.cos(((R + r)/r) * teta)
            y = self.center[1] + (R + r) * math.sin(teta) - r * math.sin(((R + r) / r) * teta)

            # Round and draw pos
            x = int(round(x))
            y = int(round(y))
            self.img[y][x] = self.color

            # Advance teta
            teta += 0.005


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
