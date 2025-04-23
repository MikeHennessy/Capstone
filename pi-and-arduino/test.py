import smbus
import struct
import time
import os

# I2C bus
bus = smbus.SMBus(1)  # 1 for /dev/i2c-1

# Arduino I2C address
arduino_address = 0x08
# File to store actuator extension
EXTENSION_FILE = "actuator_extension.txt"

def read_extension():
    """Reads the current actuator extension from the file."""
    if os.path.exists(EXTENSION_FILE):
        try:
            with open(EXTENSION_FILE, "r") as f:
                return float(f.read().strip())
        except ValueError:
            print("Error: Invalid data in extension file.  Resetting to 0.")
            return 0.0
    else:
        return 0.0

def write_extension(extension):
    """Writes the current actuator extension to the file."""
    try:
        with open(EXTENSION_FILE, "w") as f:
            f.write(str(extension))
        except Exception as e:
            print(f"Error writing to extension file: {e}")

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
        # Read the initial extension from the file
        current_extension = read_extension()
        print(f"Initial extension: {current_extension} mm")

        # Example usage:
        move1_mm = 15.5
        send_actuator_data(1, move1_mm)
        time.sleep(1)
        current_extension += move1_mm
        write_extension(current_extension)
        print(f"New extension: {current_extension} mm")

        move2_mm = -10.2
        send_actuator_data(2, move2_mm)
        time.sleep(1)
        current_extension += move2_mm
        write_extension(current_extension)
        print(f"New extension: {current_extension} mm")

        move3_mm = 0.0
        send_actuator_data(1, move3_mm)
        time.sleep(1)
        current_extension += move3_mm
        write_extension(current_extension)
        print(f"New extension: {current_extension} mm")
        
        final_extension = read_extension()
        print(f"Final extension from file: {final_extension} mm")

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()
