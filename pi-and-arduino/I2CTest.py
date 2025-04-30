import smbus
import time

# I2C bus
bus = smbus.SMBus(1)

# TCA9548A address and channel
TCA9548A_ADDRESS = 0x70
TCA9548A_CHANNEL = 0  # Change this if your INA219 is on a different channel

# INA219 address
INA219_ADDRESS = 0x40  # Or 0x41, depending on address select pins

# INA219 Registers
INA219_CONFIG_REGISTER = 0x00
INA219_BUS_VOLTAGE_REGISTER = 0x02

def select_i2c_channel(channel):
    """Selects the I2C channel on the TCA9548A."""
    try:
        bus.write_byte_data(TCA9548A_ADDRESS, 0, 1 << channel)
        time.sleep(0.001)
        return True
    except Exception as e:
        print(f"Error selecting channel {channel}: {e}")
        return False

def read_ina219_register(register):
    """Reads a 16-bit register from the INA219."""
    if not select_i2c_channel(TCA9548A_CHANNEL):
        print("Failed to select TCA9548A channel. Aborting read.")
        return None
    try:
        data = bus.read_i2c_block_data(INA219_ADDRESS, register, 2)
        value = (data[0] << 8) | data[1]
        return value
    except Exception as e:
        print(f"Error reading INA219 register 0x{register:02X}: {e}")
        return None

def configure_ina219():
    """Configures the INA219 for voltage reading.  Important!"""
    if not select_i2c_channel(TCA9548A_CHANNEL):
        print("Failed to select TCA9548A channel. Aborting configuration.")
        return False
    try:
        # Configuration Register (0x00)
        # Simplified for voltage-only reading
        # 0b0001100000000000 = 0x1800
        # Bus Voltage Range: 32V
        # PGA Gain: Divide by 1
        # Bus ADC Resolution: 12-bit
        # Shunt ADC Resolution: Disabled
        # Operating Mode: Bus Voltage Continuous
        config_value = 0x1800
        bus.write_i2c_data(INA219_ADDRESS, INA219_CONFIG_REGISTER,
                           [(config_value >> 8) & 0xFF, config_value & 0xFF])
        time.sleep(0.001)
        return True
    except Exception as e:
        print(f"Error configuring INA219: {e}")
        return False



def get_bus_voltage():
    """Reads the bus voltage from the INA219 in volts."""
    voltage_value = read_ina219_register(INA219_BUS_VOLTAGE_REGISTER)
    if voltage_value is not None:
        voltage_mV = (voltage_value >> 3) * 4
        voltage_V = float(voltage_mV) / 1000.0
        return voltage_V
    else:
        return None

if __name__ == "__main__":
    try:
        # Initialize and configure the INA219
        if not configure_ina219():
            print("INA219 configuration failed.")
            exit(1)

        # Read and print bus voltage
        while True:
            voltage_V = get_bus_voltage()
            if voltage_V is not None:
                print(f"Bus Voltage: {voltage_V:.3f} V")
            else:
                print("Failed to read INA219 voltage.")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()