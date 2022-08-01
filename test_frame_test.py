from client.neopixel_over_modbustcp import NeoPixel
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", required=True)
parser.add_argument("-f", "--frames", required=True, type=int)
args = parser.parse_args()

num_leds = 1000
num_frames = args.frames

tic = time.perf_counter()

for i in range(num_frames):
    pixels = NeoPixel(n=num_leds, brightness=1, host=args.address)
    pixels.fill(0xFFFE33)
    pixels.show()

toc = time.perf_counter()
time_diff = toc - tic

print(f"Time for {num_frames} frames is {time_diff} ({num_frames/time_diff} fps)")