import smbus
import time
import struct

# I2C bus (0 for older Pi's, 1 for newer)
bus = smbus.SMBus(1)
arduino_address = 8


def send_command(actuator_num, target_distance_mm):
    try:
        data = struct.pack("<Bf", actuator_num, target_distance_mm)
        bus.write_i2c_block_data(arduino_address, 0, list(data))
        time.sleep(0.05)  # Add a small delay here (50 milliseconds)
        print(
            f"Sent: Actuator = {actuator_num}, Distance = {target_distance_mm} to Arduino at address 0x{arduino_address:02X}"
        )
        bus.close()
    except OSError as e:
        print(f"Error sending data: {e}")
        print(
            "Possible causes: ... (as before)"
        )
        bus.close()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        bus.close()



def test_llc():
    print("Testing LLC and I2C communication...")
    try:
        send_command(1, 100.0)
        time.sleep(0.1)
        bus.read_byte(arduino_address)
        time.sleep(0.05)  # Add a delay before closing.
        print("LLC and I2C communication test successful!  Arduino responded.")
        bus.close()
    except OSError as e:
        print(f"LLC and I2C communication test failed: {e}")
        print("    - Check Arduino code for correct acknowledgement.")
        print("    - Check delays")
        bus.close()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        bus.close()
    finally:
        bus.close()



if __name__ == "__main__":
    test_llc()
    send_command(2, -50.0)