import time
import spidev
import smbus
from datetime import datetime
import os  # Import the os module for file operations

# I2C bus for INA219
bus = smbus.SMBus(1)

# TCA9548A address
TCA9548A_ADDRESS = 0x70

# INA219 address
INA219_ADDRESS = 0x40

# INA219 Registers
INA219_CONFIG_REGISTER = 0x00
INA219_BUS_VOLTAGE_REGISTER = 0x02

# SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.mode = 0b01

# MCP3008 Channels
LOAD_CURRENT_CHANNEL = 0
SOLAR_CURRENT_CHANNEL = 2

# TCA9548A Channels for Voltage Sensors
LOAD_VOLTAGE_CHANNEL = 6
SOLAR_VOLTAGE_CHANNEL = 4

# ACS712 Sensitivity (adjust as needed for your sensors)
ACS712_LOAD_SENSITIVITY = 0.066  # For 30A ACS712 connected to load
ACS712_SOLAR_SENSITIVITY = 0.066 # For 30A ACS712 connected to solar
ACS712_VCC = 3.3 # Supply voltage
DATA_DIR = "sensor_data" # Directory to store data

def select_i2c_channel(channel):
    """Selects the I2C channel on the TCA9548A."""
    try:
        bus.write_byte_data(TCA9548A_ADDRESS, 0, 1 << channel)
        time.sleep(0.001)
        return True
    except Exception as e:
        print(f"Error selecting channel {channel}: {e}")
        return False

def read_ina219_register(channel, register):
    """Reads a 16-bit register from the INA219 on the specified TCA9548A channel."""
    if not select_i2c_channel(channel):
        print(f"Failed to select TCA9548A channel {channel}. Aborting INA219 read.")
        return None
    try:
        data = bus.read_i2c_block_data(INA219_ADDRESS, register, 2)
        value = (data[0] << 8) | data[1]
        return value
    except Exception as e:
        print(f"Error reading INA219 register 0x{register:02X} on channel {channel}: {e}")
        return None

def configure_ina219(channel):
    """Configures the INA219 for voltage reading on the specified TCA9548A channel."""
    if not select_i2c_channel(channel):
        print(f"Failed to select TCA9548A channel {channel}. Aborting INA219 config.")
        return False
    try:
        config_value = 0x1800  # Simplified for voltage-only
        bus.write_i2c_block_data(INA219_ADDRESS, INA219_CONFIG_REGISTER,
                                     [(config_value >> 8) & 0xFF, config_value & 0xFF])
        time.sleep(0.001)
        return True
    except Exception as e:
        print(f"Error configuring INA219 on channel {channel}: {e}")
        return False

def get_bus_voltage(channel):
    """Reads the bus voltage from the INA219 on the specified TCA9548A channel in volts."""
    voltage_value = read_ina219_register(channel, INA219_BUS_VOLTAGE_REGISTER)
    if voltage_value is not None:
        voltage_mV = (voltage_value >> 3) * 4
        voltage_V = float(voltage_mV) / 1000.0
        return voltage_V
    else:
        return None

def read_mcp3008(channel):
    """Reads the analog value from the MCP3008 ADC on the specified channel."""
    if channel < 0 or channel > 7:
        raise ValueError("MCP3008 channel must be between 0 and 7")
    command = 0b00000001
    command |= (1 << 1)
    command |= (channel << 2)
    command_bytes = [command, 0b00000000, 0b00000000]
    response = spi.xfer2(command_bytes)
    adc_value = ((response[1] & 0x03) << 8) | response[2]
    return adc_value

def get_current(adc_value, sensitivity):
    """Converts the ADC value to current in Amperes using the specified sensitivity."""
    voltage = (adc_value * ACS712_VCC) / 1023.0
    zero_current_voltage = ACS712_VCC / 2.0
    current = (voltage - zero_current_voltage) / sensitivity
    return current

def get_filename():
    """Generates the filename based on the current date."""
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(DATA_DIR, f"sensor_data_{today}.txt")

if __name__ == "__main__":
    try:
        if not os.path.exists(DATA_DIR): #create directory if it does not exist
            os.makedirs(DATA_DIR)
        if not configure_ina219(LOAD_VOLTAGE_CHANNEL) or not configure_ina219(SOLAR_VOLTAGE_CHANNEL):
            print("INA219 configuration failed on one or more channels.")
            exit(1)

        while True:
            # Get timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Read load voltage
            load_voltage_V = get_bus_voltage(LOAD_VOLTAGE_CHANNEL)
            load_voltage_str = f"{timestamp}, Load Voltage: {load_voltage_V:.3f} V" if load_voltage_V is not None else f"{timestamp}, Failed to read Load Voltage"
            print(load_voltage_str)

            # Read solar voltage
            solar_voltage_V = get_bus_voltage(SOLAR_VOLTAGE_CHANNEL)
            solar_voltage_str = f"{timestamp}, Solar Voltage: {solar_voltage_V:.3f} V" if solar_voltage_V is not None else f"{timestamp}, Failed to read Solar Voltage"
            print(solar_voltage_str)

            # Read load current
            load_current_adc = read_mcp3008(LOAD_CURRENT_CHANNEL)
            load_current_A = get_current(load_current_adc, ACS712_LOAD_SENSITIVITY)
            load_current_str = f"{timestamp}, Load Current: {load_current_A:.3f} A"
            print(load_current_str)

            # Read solar current
            solar_current_adc = read_mcp3008(SOLAR_CURRENT_CHANNEL)
            solar_current_A = get_current(solar_current_adc, ACS712_SOLAR_SENSITIVITY)
            solar_current_str = f"{timestamp}, Solar Current: {solar_current_A:.3f} A"
            print(solar_current_str)

            # Write to file
            filename = get_filename()
            try:
                with open(filename, "a") as f:
                    f.write(load_voltage_str + "\n")
                    f.write(solar_voltage_str + "\n")
                    f.write(load_current_str + "\n")
                    f.write(solar_current_str + "\n")
            except Exception as e:
                print(f"Error writing to file {filename}: {e}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        spi.close()
        bus.close()