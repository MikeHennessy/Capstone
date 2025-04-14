import smbus
import time
import struct

# I2C bus (0 for older Pi's, 1 for newer)
bus = smbus.SMBus(1)
# Arduino I2C address
arduino_address = 8

def send_command(actuator_num, target_distance_mm):
  try:
    # Pack the data: actuator number (byte), target distance (float)
    data = struct.pack("<Bf", actuator_num, target_distance_mm)
    bus.write_i2c_block_data(arduino_address, 0, list(data))
    print(f"Sent: Actuator = {actuator_num}, Distance = {target_distance_mm}")
  except Exception as e:
    print(f"Error sending data: {e}")

# Example usage
send_command(1, 100.0) # Move actuator 1 by 100mm
time.sleep(1)
send_command(2, -50.0) # Move actuator 2 by -50mm