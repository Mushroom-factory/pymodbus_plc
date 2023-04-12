from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

IP_ADDRESS = '192.168.1.1'
PORT = 502
SLAVE_ID = 1
START_ADDRESS = 0
NUMBER_OF_REGISTERS = 2  # For 32-bit float (real) data type, you need to read/write 2 registers (16-bit each)

def read_register(register_type, start_address, num_registers, slave_id):
    if register_type == 'coil':
        return client.read_coils(start_address, num_registers, unit=slave_id)
    elif register_type == 'holding':
        return client.read_holding_registers(start_address, num_registers, unit=slave_id)
    elif register_type == 'input_status':
        return client.read_discrete_inputs(start_address, num_registers, unit=slave_id)
    elif register_type == 'input_register':
        return client.read_input_registers(start_address, num_registers, unit=slave_id)
    else:
        raise ValueError("Invalid register type")

def write_register(register_type, start_address, values, slave_id):
    if register_type == 'coil':
        return client.write_coils(start_address, values, unit=slave_id)
    elif register_type == 'holding':
        return client.write_registers(start_address, values, unit=slave_id)
    else:
        raise ValueError("Invalid register type")

def float_to_registers(value):
    builder = BinaryPayloadBuilder(endian=Endian.Big)
    builder.add_32bit_float(value)
    return builder.to_registers()

def registers_to_float(registers):
    decoder = BinaryPayloadDecoder.fromRegisters(registers, endian=Endian.Big)
    return decoder.decode_32bit_float()

client = ModbusTcpClient(IP_ADDRESS, port=PORT)

# Read real data from PLC
register_type = 'holding'  # Change this to the desired register type
response = read_register(register_type, START_ADDRESS, NUMBER_OF_REGISTERS, SLAVE_ID)

if response.isError():
    print("Error reading registers")
else:
    float_value = registers_to_float(response.registers)
    print(f"Read value: {float_value}")

# Write real data to PLC
float_value_to_write = 123.45
registers_to_write = float_to_registers(float_value_to_write)

response = write_register(register_type, START_ADDRESS, registers_to_write, SLAVE_ID)

if response.isError():
    print("Error writing registers")
else:
    print(f"Wrote value: {float_value_to_write}")

client.close()
