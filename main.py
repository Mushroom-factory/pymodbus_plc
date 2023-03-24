from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# Set up a Modbus TCP/IP client and connect to the PLC:
plc_ip = '192.168.1.10' # replace with your PLC's IP address
plc_port = 5020 # replace with your PLC's Modbus TCP/IP port number

client = ModbusTcpClient(plc_ip, port=plc_port)
client.connect()

# Use the client to read the value of register 30001:
address = 30001 # replace with the address of the register you want to read
num_words = 1 # the number of words to read (in this case, just 1)

result = client.read_holding_registers(address, num_words)

if result.isError():
    print('Error reading register:', result)
else:
    # decode the binary payload into a float value
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    value = decoder.decode_32bit_float()

    print('Value of register', address, ':', value)

client.close()