import smbus
import time
import struct

# I2C bus
bus = None
# Arduino I2C address
arduino_address = 8


def get_bus():
    """
    Gets the I2C bus instance, initializing it only once.
    """
    global bus
    if bus is None:
        try:
            bus = smbus.SMBus(1)
        except Exception as e:
            print(f"Error initializing I2C bus: {e}")
            raise
    return bus


def send_command(actuator_num, target_distance_mm):
    """
    Sends a command to the Arduino over I2C and waits for a response.

    Args:
        actuator_num (int): The actuator number (1 or 2).
        target_distance_mm (float): The target distance in mm.
    """
    i2c_bus = get_bus()
    try:
        # Pack the data: Command byte, integer, and float (big-endian)
        integer_data = 12345  # Example integer value
        data = struct.pack(">Bif", actuator_num, integer_data, target_distance_mm)
        i2c_bus.write_i2c_block_data(arduino_address, 0, list(data))
        print(
            f"Sent: Actuator = {actuator_num}, Integer = {integer_data}, Distance = {target_distance_mm} to Arduino at address 0x{arduino_address:02X}"
        )

        # Wait for the Arduino's response ("OK")
        start_time = time.time()
        while time.time() - start_time < 1.0:  # Timeout after 1 second
            try:
                response = i2c_bus.read_i2c_block_data(arduino_address, 0, 2)
                if response == [ord('O'), ord('K')]:  # Check for "OK"
                    print("Arduino acknowledged command completion.")
                    return  # Exit the function upon successful response
            except OSError:
                # Ignore this error, as it might occur if the Arduino isn't quite ready.
                pass
            time.sleep(0.01)  # Small delay to prevent excessive looping

        print("Error: Timeout waiting for Arduino response.")

    except OSError as e:
        print(f"Error sending data: {e}")
        print(
            "Possible causes: \n"
            "    - Check your wiring to the LLC.\n"
            "    - Ensure the Arduino is powered and running the correct code.\n"
            "    - Verify the Arduino I2C address.\n"
            "    - Check for any other devices on the I2C bus that may be interfering.\n"
            "    - Check that I2C is enabled in raspi-config.\n"
            "    - Reboot your Raspberry Pi.\n"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def test_llc():
    """
    Tests the LLC and I2C communication with the Arduino.
    """
    i2c_bus = get_bus()
    print("Testing LLC and I2C communication...")
    try:
        # Send a test command
        send_command(1, 100.0)  # This now includes waiting for "OK"

        print("LLC and I2C communication test successful! Arduino acknowledged.")


    except OSError as e:
        print(f"LLC and I2C communication test failed: {e}")
        print(
            "    - Check your wiring to the LLC.\n"
            "    - Ensure the Arduino is powered and running the correct code.\n"
            "    - Verify the Arduino I2C address.\n"
            "    - Check that the Arduino is acknowledging I2C commands and sending a correct response.\n"
            "    - Check that I2C is enabled in raspi-config.\n"
            "    - Reboot your Raspberry Pi.\n"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        i2c_bus.close()



if __name__ == "__main__":
    test_llc()
    # Example usage
    send_command(2, -50.0)  # This will now wait for the Arduino to finish.
    print("Actuator 2 movement complete.") #This will print after the arduino is done
