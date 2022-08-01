import logging
_LOGGER = logging.getLogger(__name__)


import sys
import os
import struct

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(this_dir, '..'))
from utils import Words

from pymodbus.datastore import (
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSequentialDataBlock,
)
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.version import version

try:
    import neopixel
    import board
except (NotImplementedError, ModuleNotFoundError):
    print("Code not running on RPI, running neopixelsim as neopixel")
    import neopixelsim as neopixel
    from neopixelsim import Board as board

REGISTERS_PER_PIXEL = 2

from enum import IntEnum

class register(IntEnum):
    GLOBAL_BRIGHTNESS = 1
    PIXEL_START = 3

class CallbackDataBlock(ModbusSequentialDataBlock):
    """A datablock that stores the new value in memory,

    and passes the operation to a message queue for further processing.
    """

    def __init__(self, address, values, pixels):
        super().__init__(address, values)
        self.pixels = pixels

    def setValues(self, address, values):  # pylint: disable=arguments-differ
        super().setValues(address, values)
        
        if address == register.GLOBAL_BRIGHTNESS:
            _LOGGER.debug(f"setting brightness!: {values[0:2]}")
            byte_value = Words(values[0:2]).to_bytes(endian='big')
            float_value = struct.unpack('f', byte_value)[0]
            _LOGGER.debug(f"setting brightness as float: {float_value}")
            self.pixels.brightness = float_value
            address += 2
            values = values[2:]
            if len(values) == 0:
                _LOGGER.debug("nothing more to do!")
                return
        
        colours = zip(values[0::2], values[1::2]) # 2 registers for every pixel
               
        for i, colour in enumerate(colours):
            regs = Words(colour)
            self.pixels[i] = regs.to_int(endian='big')


def run_callback_server(num):
    """Run callback server."""

    pixels = neopixel.Pixel(Pin=board.D18, n=num, auto_write=True, pixel_order=neopixel.GRB)
    block = CallbackDataBlock(1, [0]*((REGISTERS_PER_PIXEL*num) + 2), pixels) # 2 registers per pixel and +2 for global brightness
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)

    StartTcpServer(context, address=("0.0.0.0", 5020))
    print(pixels[0])


if __name__ == "__main__":

    # temp_list = [8429, 239, 10824, 1994, 196, 13853, 111, 5328]
    # print([hex(x) for x in temp_list])
    # print(split_16bit_list_into_colours(temp_list))

    # colour = (0xDEAD, 0xBEEF)
    # word = Words(colour)
    # print(colour)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", required=True, type=int, help="Number of pixels")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    run_callback_server(args.num)