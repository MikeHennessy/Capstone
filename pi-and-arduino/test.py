import smbus
import struct
import time
import os

# I2C bus
bus = smbus.SMBus(1)  # 1 for /dev/i2c-1

# Arduino I2C address
arduino_address = 0x08
# File to store actuator extensions
EXTENSION_FILE = "actuator_extensions.txt"

def read_extensions():
    """Reads the current actuator extensions from the file."""
    extensions = {1: 0.0, 2: 0.0}  # Default values
    if os.path.exists(EXTENSION_FILE):
        try:
            with open(EXTENSION_FILE, "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    try:
                        extensions[1] = float(lines[0].strip())
                        extensions[2] = float(lines[1].strip())
                    except ValueError:
                         print("Error: Invalid data in extension file.  Resetting to 0.")
                         extensions = {1: 0.0, 2: 0.0}
        except Exception as e:
            print(f"Error reading extension file: {e}")
    return extensions

def write_extensions(extensions):
    """Writes the current actuator extensions to the file."""
    try:
        with open(EXTENSION_FILE, "w") as f:
            f.write(str(extensions[1]) + "\n")
            f.write(str(extensions[2]) + "\n")
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
        # Read the initial extensions from the file
        current_extensions = read_extensions()
        print(f"Initial extensions: Actuator 1 = {current_extensions[1]} mm, Actuator 2 = {current_extensions[2]} mm")

        # Example usage:
        move1_mm = 15.5
        send_actuator_data(1, move1_mm)
        time.sleep(1)
        current_extensions[1] += move1_mm
        write_extensions(current_extensions)
        print(f"New extensions: Actuator 1 = {current_extensions[1]} mm, Actuator 2 = {current_extensions[2]} mm")

        move2_mm = -10.2
        send_actuator_data(2, move2_mm)
        time.sleep(1)
        current_extensions[2] += move2_mm
        write_extensions(current_extensions)
        print(f"New extensions: Actuator 1 = {current_extensions[1]} mm, Actuator 2 = {current_extensions[2]} mm")

        move3_mm = 0.0
        send_actuator_data(1, move3_mm)
        time.sleep(1)
        current_extensions[1] += move3_mm
        write_extensions(current_extensions)
        print(f"New extensions: Actuator 1 = {current_extensions[1]} mm, Actuator 2 = {current_extensions[2]} mm")
        
        final_extensions = read_extensions()
        print(f"Final extensions from file: Actuator 1 = {final_extensions[1]} mm, Actuator 2 = {final_extensions[2]} mm")

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        bus.close()