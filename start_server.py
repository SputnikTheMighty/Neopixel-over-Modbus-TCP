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
except (NotImplementedError, ModuleNotFoundError):
    print("Importing neopixelsim as neopixel")
    import neopixelsim as neopixel

REGISTERS_PER_PIXEL = 2

from enum import IntEnum

class register(IntEnum):
    GLOBAL_BRIGHTNESS = 0
    PIXEL_START = 1

class Colour:
    def __init__(self, red, green, blue):
        self._buf = bytes([red, green, blue])

    @property
    def red(self):
        return self._buf[0]
    @property
    def blue(self):
        return self._buf[1]
    @property
    def green(self):
        return self._buf[2]

    def __getitem__(self, index):
        return self._buf(index)

    def __call__(self):
        return self._buf

    def __repr__(self) -> str:
        return f"RGB({' '.join(hex(x) for x in self._buf)})"

    @classmethod
    def from_registers(cls, registers):
        assert len(registers) == 2
        return Colour(registers[0] & 0x00FF, (registers[0] & 0xFF00) >> 8, registers[1] & 0x00FF)


def split_16bit_list_into_colours(register_list):

    colours = zip(register_list[0::2], register_list[1::2])
    colours = [Colour.from_registers(x) for x in colours]
    return colours

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
            address += 1
            values = values[1:]
        
        colours = split_16bit_list_into_colours(values)
        for index, colour in enumerate(colours):
            self.pixels[address + index] = colour()


def run_callback_server(num):
    """Run callback server."""

    block = CallbackDataBlock(0, [0]*2*num)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)

    StartTcpServer(context, address=("0.0.0.0", 5020))
    print(block.pixels[num])


if __name__ == "__main__":

    temp_list = [8429, 239, 10824, 1994, 196, 13853, 111, 5328]
    print([hex(x) for x in temp_list])
    print(split_16bit_list_into_colours(temp_list))

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", required=True, type=int, help="Number of pixels")
    args = parser.parse_args()
    run_callback_server(args.num)