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
        self.pixel_array = [ [0]*bpp for i in range(n)]

    def show(self):
        print("rendering!")

    def fill(self):
        pass

    def __len__(self):
        """
        Number of pixels.
        """
        return self._pixels

    @property
    def n(self):
        return len(self)

    def __setitem__(self, index, colour):
        self.pixel_array[index] = colour

    def __getitem__(self, index):
        return self.pixel_array[index]

if __name__ == "__main__":

    pixels = Pixel(6)
    pixels[3] = [7,8,9]

    print(pixels.pixel_array)
    print(pixels[3])