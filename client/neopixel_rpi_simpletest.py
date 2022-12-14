
import time

try:
    import board
    import neopixel
except (ModuleNotFoundError, NotImplementedError):
    import neopixel_over_modbustcp as neopixel
    from neopixel_over_modbustcp import Board as board


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", required=True, type=int, help="Number of pixels")
    parser.add_argument("-a", "--address", type=str, help="IP address of modbus server")
    args = parser.parse_args()

    pixel_pin = board.D18
    num_pixels = args.num
    ORDER = neopixel.GRB

    try:
        pixels = neopixel.NeoPixel(
                Pin=pixel_pin, n=num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER,
            )
    except TypeError as e:
        pixels = neopixel.NeoPixel(
            Pin=pixel_pin, n=num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER,
            host=args.address
        )
    
    while True:

        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(1)
        
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(1)

        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(1)

        rainbow_cycle(0.001) 