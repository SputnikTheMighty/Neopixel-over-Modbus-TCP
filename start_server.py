import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

from pymodbus.datastore import (
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSequentialDataBlock,
)
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.version import version

try:
    import neopixel
except NotImplementedError:
    import neopixelsim as neopixel

REGISTERS_PER_PIXEL = 2

from enum import IntEnum

class register(IntEnum):
    GLOBAL_BRIGHTNESS = 0
    PIXEL_START = 1

class CallbackDataBlock(ModbusSequentialDataBlock):
    """A datablock that stores the new value in memory,

    and passes the operation to a message queue for further processing.
    """

    def __init__(self, address, values):
        self.pixels = neopixel.Pixel(len(values)/2 + 1, auto_write=True) # +1 for global brightness
        super().__init__(address, values)

    def setValues(self, address, values):  # pylint: disable=arguments-differ
        super().setValues(address, values)

        if address == register.GLOBAL_BRIGHTNESS:
            self.pixels.set_brightness(values[0])
        
        
        for i, colour in enumerate(values):
            self.pixels[i] = colour
            print(F"pixel {i} set to {colour}")


def run_callback_server(num):
    """Run callback server."""

    block = CallbackDataBlock(0, [0]*2*num)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)

    StartTcpServer(context, address=("0.0.0.0", 5020))


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", required=True, type=int, help="Number of pixels")
    args = parser.parse_args()
    run_callback_server(args.num)