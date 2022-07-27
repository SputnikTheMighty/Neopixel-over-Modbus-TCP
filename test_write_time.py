from math import ceil
from pymodbus.client.sync import ModbusTcpClient

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", required=True)
args = parser.parse_args()

client = ModbusTcpClient(args.address, port=5020)
client.connect()
assert client.is_socket_open()

import time


num_leds = 1000
num_frames = 150

REGISTERS_PER_PIXEL = 2
MAX_REG_PER_MESSAGE = 124

# Write each LED separately (waaay too slow)
# tic = time.perf_counter()
# for frame in range(num_frames):
#     for reg in range(num_leds):
#         result = client.write_registers(2*reg, [i for i in range(2)], units=1)
#         if result.isError():
#             print(f"failed on reg {reg}")
#             break
# toc = time.perf_counter()
# print(f"time for {num_leds} LED update over {num_frames}: {round(toc - tic, 2)}s ({round(num_frames/(toc-tic), 2)} frames/s)")

# Write all LEDs together
num_msgs = ceil(num_leds*REGISTERS_PER_PIXEL/MAX_REG_PER_MESSAGE)
print(f"number of messages to update {num_leds} LEDs: {num_msgs}")

tic = time.perf_counter()
for frame in range(num_frames):
    for msg in range(num_msgs):
        if msg < num_msgs -1:
            result = client.write_registers(0, [msg*MAX_REG_PER_MESSAGE + i for i in range(MAX_REG_PER_MESSAGE-1)])
            assert not result.isError()
        else:
            result = client.write_registers(msg*MAX_REG_PER_MESSAGE, [msg*MAX_REG_PER_MESSAGE + i for i in range(num_leds%MAX_REG_PER_MESSAGE)])
            assert not result.isError()
toc = time.perf_counter()
print(f"time for {num_leds} LED update over {num_frames} frames: {round(toc - tic, 2)}s ({round(num_frames/(toc-tic), 2)} frames/s)")
result = client.read_holding_registers(num_leds*2 - 10, count=10, unit=1)
if not result.isError():
    print(f"final register values {result.registers}")


client.close() 