from pymodbus.client.sync import ModbusTcpClient
from math import ceil

REGISTERS_PER_PIXEL = 2 # 1 register = 2 bytes, therefore need 2 registers for full RGB
MAX_REG_PER_MESSAGE = 124 # from modbus standard

GRB = 'GRB'

class Board:
    D18 = 5

class NeoPixel:

    def __init__(self, n, brightness, host, *args, **kwargs) -> None:
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
            address = msg * MAX_REG_PER_MESSAGE
            if msg < self.num_msgs - 1:
                # full message
                result = self._client.write_registers(address, self._buf[address : address + MAX_REG_PER_MESSAGE])
                assert not result.isError()
            else:
                # final message (non-full message)
                result = self._client.write_registers(address, self._buf[address :])
                assert not result.isError()

    def __setitem__(self, index, colour):
        ''' Set a pixel one colour, takes int in form 0x00RRGGBB or tuple (red, green, blue) '''
        if isinstance(colour, int):
            self._buf[2 * index] = (colour & 0xFF0000) >> 16
            self._buf[2 * index + 1] = colour & 0x00FFFF

        if isinstance(colour, tuple):
            assert len(colour) == 3
            self._buf[2 * index] = colour[0]
            self._buf[2 * index] = (colour[1] << 8) + colour[2]

if __name__ == "__main__":

    pixels = NeoPixel(n = 10, brightness=1, host='192.168.0.232')
    pixels.fill(0xFF0033)
    pixels.show()