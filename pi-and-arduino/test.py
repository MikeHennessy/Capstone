import smbus
import struct
import time

# I2C bus
bus = smbus.SMBus(1)  # 1 for /dev/i2c-1

# Arduino I2C address
arduino_address = 0x08


def send_actuator_data(actuator_num, mm_value):
    """
    Sends actuator number and a millimeter value to the Arduino via I2C.

    Args:
        actuator_num: The actuator number (1 or 2).
        mm_value: The millimeter value (float, between -20 and 20).
    """
    try:
        # Pack the data (Big Endian)
        data = struct.pack('>if', actuator_num, mm_value)  # '>if' for int, float
        bus.write_i2c_block_data(arduino_address, 0, list(data))
        print(f"Sent: Actuator = {actuator_num}, MM = {mm_value}")
    except Exception as e:
        print(f"Error sending data: {e}")



if __name__ == "__main__":
    try:
        # Example usage:
        send_actuator_data(1, 15.5)
        time.sleep(1)
        send_actuator_data(2, -10.2)
        time.sleep(1)
        send_actuator_data(1, 0.0)
        time.sleep(1)

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()
