import smbus
import struct
import time

# I2C bus
bus = smbus.SMBus(1)  # 1 for /dev/i2c-1

# TCA9548A address
TCA9548A_ADDRESS = 0x70
TCA9548A_CHANNEL = 7
ARDUINO_I2C_ADDRESS = 0x08

def select_i2c_channel(channel):
    """Selects the I2C channel on the TCA9548A."""
    try:
        bus.write_byte_data(TCA9548A_ADDRESS, 0, 1 << channel)
        time.sleep(0.001)
        return True
    except Exception as e:
        print(f"Error selecting channel {channel}: {e}")
        return False

def send_data_to_arduino(integer_value, float_value):
    """
    Sends an integer and a float to the Arduino through the TCA9548A.
    """
    if not select_i2c_channel(TCA9548A_CHANNEL):
        print("Failed to select TCA9548A channel. Aborting.")
        return

    try:
        # Pack the data (Big Endian, matching Arduino's expected format)
        data = struct.pack('>if', integer_value, float_value)
        bus.write_i2c_block_data(ARDUINO_I2C_ADDRESS, 0, list(data))
        print(f"Sent to Arduino: Integer = {integer_value}, Float = {float_value}")
    except Exception as e:
        print(f"Error sending data to Arduino: {e}")

if __name__ == "__main__":
    try:
        # Send some test data
        test_integer = 12345
        test_float = 3.14159
        send_data_to_arduino(test_integer, test_float)
        time.sleep(1)  # Give Arduino time to process

        test_integer = 54321
        test_float = 2.71828
        send_data_to_arduino(test_integer, test_float)
        time.sleep(1);

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()
