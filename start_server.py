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

import neopixelsim

class CallbackDataBlock(ModbusSequentialDataBlock):
    """A datablock that stores the new value in memory,

    and passes the operation to a message queue for further processing.
    """

    def __init__(self, address, values):
        self.pixels = neopixelsim.Pixel(len(values))
        super().__init__(address, values)

    def setValues(self, address, values):  # pylint: disable=arguments-differ
        super().setValues(address, values)
        
        for i, colour in enumerate(values):
            self.pixels[i] = colour
            print(F"pixel {i} set to {colour}")


def run_callback_server():
    """Run callback server."""

    block = CallbackDataBlock(0, [0]*100)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)

    StartTcpServer(context, address=("0.0.0.0", 5020))


if __name__ == "__main__":
    run_callback_server()