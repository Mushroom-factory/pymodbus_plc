# I want to use pymodbus to read 3 registers from 30101, 30102, 30103 in PLC s7 1200, the data would be real type.
# And I want to write 2 number 23.3 and 1000.56 to 2 registers 30104 ad 30105. tell me the detail process and write code

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian


client = ModbusTcpClient('192.168.1.1') # PLC IP
client.connect()

result = client.read_holding_registers(address=30101, count=3)

if result.isError():
    print('Error reading registers:', result)
else:
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    value1 = decoder.decode_32bit_float()
    value2 = decoder.decode_32bit_float()
    value3 = decoder.decode_32bit_float()


builder = BinaryPayloadBuilder(byteorder=Endian.Big)
builder.add_32bit_float(23.3)
builder.add_32bit_float(1000.56)
payload = builder.to_registers()

result = client.write_registers(address=30104, values=payload)

if result.isError():
    print('Error writing registers:', result)
else:
    print('Registers written successfully')


client.close()
