import smbus
import time
import struct

# I2C expander address (default for PCA9548A is 0x70)
expander_address = 0x70
# The channel on the expander connected to your Arduino (SDA/SCL7 in your case is channel 7, 0-indexed)
arduino_channel = 7
# Arduino I2C address
arduino_address = 8

def send_command(actuator_num, target_distance_mm):
    """
    Sends a command to the Arduino over I2C to move an actuator, using an I2C expander.

    Args:
        actuator_num (int): The number of the actuator to move (1 or 2).
        target_distance_mm (float): The target distance in millimeters.
    """
    try:
        # I2C bus (0 for older Pi's, 1 for newer)
        bus = smbus.SMBus(1)

        # Select the Arduino's channel on the expander.  Important!
        bus.write_byte_data(expander_address, 0, 1 << arduino_channel)

        # Pack the data: actuator number (byte), target distance (float)
        data = struct.pack("<Bf", actuator_num, target_distance_mm)
        bus.write_i2c_block_data(arduino_address, 0, list(data))
        print(f"Sent: Actuator = {actuator_num}, Distance = {target_distance_mm}")
        bus.close()
    except FileNotFoundError:
        print("Error: smbus module not found. Please install it and enable I2C.")
        print("   1.  Open a terminal on your Raspberry Pi.")
        print("   2.  Install the smbus library: sudo apt-get update && sudo apt-get install python3-smbus")
        print("   3.  Enable I2C: sudo raspi-config")
        print("       -   Select 'Interfacing Options'.")
        print("       -   Select 'I2C'.")
        print("       -   Enable I2C.")
        print("       -   Reboot your Raspberry Pi.")
    except IOError as e:
        print(f"Error communicating with I2C device: {e}")
        print("   Please check the following:")
        print("   1.  Ensure the I2C expander (TCA9548A) is correctly wired.")
        print("   2.  Verify the I2C expander address (expander_address) is correct (default is 0x70, but check your device's datasheet).")
        print("   3.  Confirm the Arduino I2C address (arduino_address) is correct (set in Arduino's Wire.begin()).")
        print("   4.  Check for any other devices on the I2C bus that might be interfering.")
        print("   5.  Make sure the I2C bus is enabled on your Raspberry Pi (using raspi-config).")
        print("   6.  Try adding pull-up resistors (4.7kΩ) to the SDA and SCL lines.")
        bus.close()
    except Exception as e:
        print(f"Error sending data: {e}")
        bus.close()

if __name__ == "__main__":
    # Example usage
    send_command(1, 100.0)
    time.sleep(1)
    send_command(2, -50.0)

