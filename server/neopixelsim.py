'''
For use when there are no neopixels around!
'''

GRB = 'GRB'
GRBW = 'GRBW'
RGB = 'RGB'
RGBW = 'RGBW'

class Board:
    D18 = 5

bpp = 3

class Pixel:

    def __init__(self, n, *args, **kwargs) -> None:
        self._pixels = n
        self._bytes = bpp * n
        self.pixel_array = [(0, 0, 0) for i in range(n)]
        self._brightness = 1

    def show(self):
        print("rendering!")

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value

    def __len__(self):
        """
        Number of pixels.
        """
        return self._pixels

    @property
    def n(self):
        return len(self)

    def __setitem__(self, index, colour):
        if isinstance(colour, tuple):
            self.pixel_array[index] = colour[0:3]
        elif isinstance(colour, int):
            self.pixel_array[index] = tuple((colour & 0x00FFFFFF).to_bytes(3, 'big'))
        elif isinstance(colour, bytes):
            print(f"setting {index} with {colour}")
            self.pixel_array[index] = tuple(colour[0:3])


    def __getitem__(self, index):
        return self.pixel_array[index]

if __name__ == "__main__":

    pixels = Pixel(6)
    pixels[3] = (7,8,9)
    pixels[5] = 4829
    pixels[2] = bytes((33, 78, 2))

    print(pixels.pixel_array)
    print(pixels[3])