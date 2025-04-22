import smbus
import struct
import time

# I2C bus
bus = smbus.SMBus(1)  # 1 for /dev/i2c-1

# Arduino I2C address
arduino_address = 0x08

def send_data(actuator_num, integer_value, float_value):
    """
    Sends actuator number, an integer, and a float to the Arduino via I2C.

    Args:
        actuator_num: The actuator number (1 or 2).
        integer_value: The integer value to send.
        float_value: The float value to send.
    """
    try:
        # Pack the data (Big Endian)
        data = struct.pack('>iif', actuator_num, integer_value, float_value)
        bus.write_i2c_block_data(arduino_address, 0, list(data))
        print(f"Sent: Actuator = {actuator_num}, Integer = {integer_value}, Float = {float_value}")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    try:
        # Example usage:
        send_data(1, 100, 200.22)
        time.sleep(1)

        send_data(2, 500, 1000.55)
        time.sleep(1)

        send_data(1, -200, -300.77)
        time.sleep(1)

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()