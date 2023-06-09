# I want to use pymodbus to read 3 registers from 30101, 30102, 30103 in PLC s7 1200, the data would be real type.
# And I want to write 2 number 23.3 and 1000.56 to 2 registers 30104 ad 30105. tell me the detail process and write code

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian

plc_ip = '192.168.1.10' # replace with your PLC's IP address
plc_port = 503 # replace with your PLC's Modbus TCP/IP port number
start_address = 0
# Can't be 30101 because it's higher than the register
# should be 101 or 0x01

# Set the number of registers to read
num_registers = 10 # Must be the same as in PLC

client = ModbusTcpClient(plc_ip, port=plc_port)
client.connect()

result = client.read_holding_registers(address= start_address, count=num_registers, unit=2)


if result.isError():
    print('Error reading registers:', result)
else:
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    value1 = decoder.decode_16bit_int()
    value2 = decoder.decode_16bit_int()
    value3 = decoder.decode_16bit_int()
    print('value 1 = {}, value 2 = {}, value 3 = {}'.format(value1,value2,value3))


builder = BinaryPayloadBuilder(byteorder=Endian.Big)
builder.add_16bit_int(23)
builder.add_16bit_int(1000)
payload = builder.to_registers()

result = client.write_registers(address=10, values=payload)

if result.isError():
    print('Error writing registers:', result)
else:
    print('Registers written successfully')


client.close()
