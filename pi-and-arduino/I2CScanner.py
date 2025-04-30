import smbus
import time

# I2C bus
bus = smbus.SMBus(1)

# TCA9548A address
TCA9548A_ADDRESS = 0x70
TCA9548A_CHANNEL = 7  # Define the TCA9548A channel

def select_i2c_channel(channel):
    """Selects the I2C channel on the TCA9548A."""
    try:
        bus.write_byte_data(TCA9548A_ADDRESS, 0, 1 << channel)
        time.sleep(0.001)
        return True
    except Exception as e:
        print(f"Error selecting channel {channel}: {e}")
        return False

def scan_i2c_bus(channel):
    """Scans the I2C bus on the specified channel and prints found addresses."""
    if not select_i2c_channel(channel):
        print(f"Failed to select channel {channel}, cannot scan.")
        return

    found_addresses = []
    for address in range(128):
        try:
            bus.read_byte(address)  # Attempt to read from each address
            found_addresses.append(address)
            print(f"Found device at address 0x{address:02x} on channel {channel}")
        except Exception:
            pass  # Ignore errors, as many addresses will not have devices

    if not found_addresses:
        print(f"No devices found on channel {channel}")
    return found_addresses

# Select the TCA9548A channel and scan
scan_i2c_bus(TCA9548A_CHANNEL) # Pass the channel to the function
