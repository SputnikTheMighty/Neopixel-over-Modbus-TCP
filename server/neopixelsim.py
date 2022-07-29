'''
For use when there are no neopixels around!
'''

GRB = 'GRB'
GRBW = 'GRBW'
RGB = 'RGB'
RGBW = 'RGBW'

bpp = 3

class Pixel:

    def __init__(self, n, *args, **kwargs) -> None:
        self._pixels = n
        self._bytes = bpp * n
        self.pixel_array = [(0, 0, 0) for i in range(n)]
        self._brightness = 1

    def show(self):
        print("rendering!")

    def fill(self):
        pass

    def set_brightness(self, value):
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
            self.pixel_array[index] = colour
        elif isinstance(colour, int):
            self.pixel_array[index] = (((colour&0xFF0000) >> 16), ((colour&0x00FF00) >> 8), ((colour&0x0000FF) >> 0))
        elif isinstance(colour, bytes):
            print(f"setting {index} with {colour}")
            self.pixel_array[index] = (colour[0], colour[1], colour[2])


    def __getitem__(self, index):
        return self.pixel_array[index]

if __name__ == "__main__":

    pixels = Pixel(6)
    pixels[3] = (7,8,9)
    pixels[5] = 4829

    print(pixels.pixel_array)
    print(pixels[3])