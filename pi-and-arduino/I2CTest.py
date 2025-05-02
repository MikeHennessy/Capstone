from ina219 import INA219
from ina219 import DeviceRangeError
import time

# TCA9548A address
TCA9548A_ADDRESS = 0x70
TCA9548A_CHANNEL = 0  # Change this if your INA219 is on a different channel

# INA219 default address
INA219_ADDRESS = 0x40  # Or 0x41, depending on address select pins

# Shunt resistor value (in Ohms). Adjust if your sensor has a different value.
SHUNT_OHMS = 0.1

def select_i2c_channel(bus, channel):
    """Selects the I2C channel on the TCA9548A."""
    try:
        bus.write_byte_data(TCA9548A_ADDRESS, 0, 1 << channel)
        time.sleep(0.001)
        return True
    except Exception as e:
        print(f"Error selecting channel {channel}: {e}")
        return False

def get_bus_voltage_ina219(bus, channel):
    """Reads the bus voltage from the INA219 using the library."""
    if not select_i2c_channel(bus, channel):
        print("Failed to select TCA9548A channel. Aborting read.")
        return None
    try:
        ina = INA219(SHUNT_OHMS, address=INA219_ADDRESS, bus=bus)
        ina.configure()  # Use default configuration for voltage reading
        return ina.bus_voltage()
    except Exception as e:
        print(f"Error reading INA219 voltage: {e}")
        return None

if __name__ == "__main__":
    try:
        # Initialize I2C bus
        bus = smbus.SMBus(1)

        while True:
            voltage_V = get_bus_voltage_ina219(bus, TCA9548A_CHANNEL)
            if voltage_V is not None:
                print(f"Bus Voltage: {voltage_V:.3f} V")
            else:
                print("Failed to read INA219 voltage.")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()