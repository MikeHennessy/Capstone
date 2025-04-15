import smbus
import time
import struct

# I2C bus (0 for older Pi's, 1 for newer)
bus = smbus.SMBus(1)
# Arduino I2C address (default in the Arduino code is 8)
arduino_address = 8


def send_command(actuator_num, target_distance_mm):
    """
    Sends a command to the Arduino over I2C to move an actuator.
    This function assumes the Arduino is directly connected to the
    Raspberry Pi through the LLC.

    Args:
        actuator_num (int): The number of the actuator to move (1 or 2).
        target_distance_mm (float): The target distance in millimeters.
    """
    try:
        # Pack the data: actuator number (byte), target distance (float)
        data = struct.pack("<Bf", actuator_num, target_distance_mm)
        bus.write_i2c_block_data(arduino_address, 0, list(data))
        print(
            f"Sent: Actuator = {actuator_num}, Distance = {target_distance_mm} to Arduino at address 0x{arduino_address:02X}"
        )
        bus.close()
    except OSError as e:
        print(f"Error sending data: {e}")
        print(
            "Possible causes: \n"
            "    - Check your wiring to the LLC.\n"
            "    - Ensure the Arduino is powered and running the correct code.\n"
            "    - Verify the Arduino I2C address.\n"
            "    - Check for any other devices on the I2C bus that may be interfering.\n"
            "    - If the error is related to the bus being busy, try adding a small delay before bus.close()"
        )
        bus.close()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        bus.close()



def test_llc():
    """
    Tests the LLC by sending a command to the Arduino and checking for a response.
    This function assumes the Arduino is directly connected to the
    Raspberry Pi through the LLC.
    """
    print("Testing LLC and I2C communication...")
    try:
        # Send a test command (e.g., move actuator 1 by 100mm)
        send_command(1, 100.0)
        time.sleep(0.1)  # Give the Arduino time to process

        # Attempt to read a byte from the Arduino to check for a response.
        # If the Arduino is set up correctly and the LLC is working, this should succeed.
        # Note:  This is a *very* basic check.  A more robust test would involve
        # the Arduino sending meaningful data back.
        bus.read_byte(arduino_address)
        print("LLC and I2C communication test successful!  Arduino responded.")
        bus.close()

    except OSError as e:
        print(f"LLC and I2C communication test failed: {e}")
        print(
            "    - Check your wiring to the LLC.\n"
            "    - Ensure the Arduino is powered and running the correct code.\n"
            "    - Verify the Arduino I2C address.\n"
            "    - Check that the Arduino is acknowledging I2C commands."
        )
        bus.close()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        bus.close()
    finally:
        bus.close()


if __name__ == "__main__":
    test_llc()
    # Example usage: Send a command after the test
    send_command(2, -50.0)  # Move actuator 2 by -50mm
