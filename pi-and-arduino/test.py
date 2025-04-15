import smbus
import struct
import time

# I2C bus
bus = smbus.SMBus(1)  # 1 for /dev/i2c-1

# Arduino I2C address
arduino_address = 0x08

def send_data(integer_value, float_value):
    """
    Sends an integer and a float to the Arduino via I2C.

    Args:
        integer_value: The integer value to send.
        float_value: The float value to send.
    """
    try:
        # Pack the integer and float into a byte string (BIG ENDIAN)
        data = struct.pack('>if', integer_value, float_value)
        print(f"Packed Data (Bytes): {list(data)}")  # Print the raw bytes
        # Send the data to the Arduino
        bus.write_i2c_block_data(arduino_address, 0, list(data))
        print(f"Sent: Integer = {integer_value}, Float = {float_value}")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    try:
        # Example usage:
        integer_data = 1
        float_data = 1.1003
        send_data(integer_data, float_data)
        time.sleep(1)

        integer_data = 5
        float_data = 10.5
        send_data(integer_data, float_data)
        time.sleep(1)

        integer_data = 100
        float_data = 200.22
        send_data(integer_data, float_data)
        time.sleep(1)

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()

