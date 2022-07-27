from matplotlib import units
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('10.42.0.125', port=5020)
client.connect()
print(f"socket is open? {client.is_socket_open()}")
result = client.write_register(1, 0x05, units=1)
assert not result.isError()
result = client.read_holding_registers(1, units=1)
assert not result.isError()
print(f"rsult = {result.registers[0]}")
client.close() 