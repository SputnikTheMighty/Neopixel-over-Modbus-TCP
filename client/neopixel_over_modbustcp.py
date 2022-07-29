import struct
from pymodbus.client.sync import ModbusTcpClient
from math import ceil
  
# importing
import sys
import os
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(this_dir, '..'))
from utils import Words

REGISTERS_PER_PIXEL = 2 # 1 register = 2 bytes, therefore need 2 registers for full RGB
MAX_REG_PER_MESSAGE = 124 # from modbus standard

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
        self.num_msgs = ceil(n*REGISTERS_PER_PIXEL/MAX_REG_PER_MESSAGE)

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
                result = self._client.write_registers(address, self._buf[index : index + MAX_REG_PER_MESSAGE])
                assert not result.isError()
            else:
                # final message (non-full message)
                result = self._client.write_registers(address, self._buf[index:])
                assert not result.isError()

    def __setitem__(self, index, colour):
        ''' 
        Set a pixel one colour in the internal buffer
        Takes int in form 0x00RRGGBB or tuple (red, green, blue) 
        '''
        if isinstance(colour, int):
            byte_src = colour.to_bytes(4, 'big')
            regs = Words.from_bytes(byte_src, 'big')

        if isinstance(colour, tuple):
            assert len(colour) == 3
            regs = Words.from_bytes(colour, 'big')
        
        print(regs)
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
        byte_value = int.from_bytes(struct.pack('f', value), 'big')
        register_values = [(byte_value & 0xFFFF0000) >> 16, (byte_value & 0x0000FFFF)]
        result = self._client.write_registers(Registers.GLOBAL_BRIGHTNESS, register_values)
        if not result.isError():
            self._brightness = value


if __name__ == "__main__":

    pixels = NeoPixel(n = 10, brightness=1, host='192.168.0.232')
    pixels.fill(0xFFFE33)
    pixels.show()

    pixels.brightness = 0.6