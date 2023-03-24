from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import struct

# Connect to the PLC (replace the IP address with your PLC's IP address)
client = ModbusTcpClient('192.168.1.10',5020)
# client.connect()
try:
    # Read 3 registers starting from address 0x01
    response = client.read_holding_registers(address=0x01, count=30, unit=1)

    # Convert the raw binary data to real numbers
    values = [struct.unpack('!f', bytes(bytearray(response.registers[i:i+2])))[0] for i in range(0, len(response.registers), 2)]

    # Print the read values
    print(f"Read values: {values}")

except ModbusIOException as e:
    print(f"Error reading from PLC: {e}")
    client.close()
    exit()

# Write 2 registers starting from address 0x04
client.write_registers(address=0x04, values=[int(x * 100) for x in [100.21, 4.3]], unit=1)

# Disconnect from the PLC
client.close()
