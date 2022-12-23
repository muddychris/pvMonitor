""" A basic client demonstrating how to use pysolarmanv5."""
from pysolarmanv5 import PySolarmanV5


def main():
    """Create new PySolarman instance, using IP address and S/N of data logger

    Only IP address and S/N of data logger are mandatory parameters. If port,
    mb_slave_id, and verbose are omitted, they will default to 8899, 1 and 0
    respectively.
    """
    
    print ("Connecting")
    modbus = PySolarmanV5(
        "192.168.2.172", 4065770491, port=8899, mb_slave_id=1, verbose=False)

    """Query six input registers, results as a list"""
    print ("33022 : ", end =" ")
    print(modbus.read_input_registers(register_addr=33022, quantity=6))
    
    print ("33092 : ", end =" ")
    print(modbus.read_input_registers(register_addr=33092, quantity=6))

    """Query six holding registers, results as list"""
    print ("43000 : ", end =" ")
    print(modbus.read_holding_registers(register_addr=43000, quantity=6))

    """Query single input register, result as an int"""
    print ("33139 : ", end =" ")
    print(modbus.read_input_register_formatted(register_addr=33139, quantity=1))

    """Query single input register, apply scaling, result as a float"""
    print ("33035 : ", end =" ")
    print(
        modbus.read_input_register_formatted(register_addr=33035, quantity=1, scale=0.1)
    )

    print ("33132 : ", end =" ")
    print(
        modbus.read_input_register_formatted(register_addr=33133, quantity=1, scale=0.1)
    )

    """Query two input registers, shift first register up by 16 bits, result as a signed int, """
    print(
        modbus.read_input_register_formatted(register_addr=33079, quantity=2, signed=1)
    )

    """Query single holding register, apply bitmask and bitshift left (extract bit1 from register)"""
    print(
        modbus.read_holding_register_formatted(
            register_addr=43110, quantity=1, bitmask=0x2, bitshift=1
        )
    )


if __name__ == "__main__":
    main()