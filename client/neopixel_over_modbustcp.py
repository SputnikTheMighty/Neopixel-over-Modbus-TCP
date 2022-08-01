import struct
from pymodbus.client.sync import ModbusTcpClient
from math import ceil
  
# importing
import sys
import os
import logging

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(this_dir, '..'))
from utils import Words

REGISTERS_PER_PIXEL = 2 # 1 register = 2 bytes, therefore need 2 registers for full RGB
MAX_REG_PER_MESSAGE = 123 # from modbus standard

_LOGGER = logging.getLogger(__name__)

GRB = 'GRB'
RGB = 'RGB'

class Board:
    D18 = 5

class Registers:
    GLOBAL_BRIGHTNESS = 0
    START_OF_PIXELS = 2

class NeoPixel:

    def __init__(self, host, n, brightness=0.5, *args, **kwargs) -> None:
        self._brightness = brightness
        self._num_pixels = n
        self._buf = [0 for i in range(2 * n)]
        self._client = ModbusTcpClient(host, port=5020)
        self._client.connect()
        if not self._client.is_socket_open():
            print("No Connection!")
        self.num_msgs = ceil(n * REGISTERS_PER_PIXEL / MAX_REG_PER_MESSAGE)
        _LOGGER.debug(f"number of messages per frame = {self.num_msgs}")

    def fill(self, colour):
        ''' Set all pixels to one colour '''
        for i in range(self._num_pixels):
            self[i] = colour

    def show(self):
        ''' Send entire pixel array over Modbus TCP '''
        for msg in range(self.num_msgs):
            address = (msg * MAX_REG_PER_MESSAGE) + Registers.START_OF_PIXELS
            index = (msg * MAX_REG_PER_MESSAGE)
            if msg < self.num_msgs - 1:
                # full message
                _LOGGER.debug(f"sending message len {len(self._buf[index:index + MAX_REG_PER_MESSAGE])}, address {address}")
                result = self._client.write_registers(address, self._buf[index : index + MAX_REG_PER_MESSAGE])
                if result.isError():
                    _LOGGER.error(result)
            else:
                # final message (non-full message)
                _LOGGER.debug(f"sending message len {len(self._buf[index:])}, address {address}")
                result = self._client.write_registers(address, self._buf[index:])
                if result.isError():
                    _LOGGER.error(result)

    def __setitem__(self, index, colour):
        ''' 
        Set a pixel one colour in the internal buffer
        Takes int in form 0x00RRGGBB or tuple (red, green, blue) 
        '''
        if isinstance(colour, int):
            colour = colour & 0xFFFFFFFF
            regs = Words.from_int(colour, 'big', length=REGISTERS_PER_PIXEL)

        if isinstance(colour, tuple):
            assert len(colour) == 3
            regs = Words.from_bytes(bytes(colour), 'big')
        
        self._buf[2 * index] = regs[0]
        self._buf[(2 * index) + 1] = regs[1]

    @property
    def brightness(self):
        ''' Local brightness, not read from server '''
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):

        # check value is valid
        value = min(max(value, 0.0), 1.0)
        change = value - self._brightness
        if -0.001 < change < 0.001:
            return

        # write to server
        byte_value = struct.pack('f', value)
        register_values = Words.from_bytes(byte_value, endian='big')
        result = self._client.write_registers(Registers.GLOBAL_BRIGHTNESS, register_values[0:])
        if not result.isError():
            self._brightness = value


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", required=True, type=int, help="Number of pixels")
    parser.add_argument("-a", "--address", required=True, type=str, help="IP address of modbus server")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    pixels = NeoPixel(n=args.num, brightness=1, host=args.address)
    pixels.fill(0xFFFE33)
    pixels.show()

    print("written pixels")

    pixels.brightness = 0.6