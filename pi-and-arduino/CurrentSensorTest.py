import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (default CS pin)
spi.max_speed_hz = 1000000  # 1 MHz (adjust if needed)
spi.mode = 0b01  # Mode 1: CPOL=0, CPHA=1

# MCP3008 channel connected to ACS712 (0-7)
ACS712_CHANNEL = 0

def read_mcp3008(channel):
    """Reads the analog value from the MCP3008 ADC on the specified channel."""
    if channel < 0 or channel > 7:
        raise ValueError("MCP3008 channel must be between 0 and 7")

    # Construct the SPI message to read from the MCP3008
    # Start bit (1), single-ended mode (1), channel (3 bits), dummy bit (0)
    command = 0b00000001  # Start bit
    command |= (1 << 1)     # Single-ended mode
    command |= (channel << 2)  # Channel select
    command |= (0 << 1)
    command_bytes = [command, 0b00000000, 0b00000000] #add 2 zero bytes

    # Send the command and read the response
    response = spi.xfer2(command_bytes)

    # Extract the 10-bit ADC value from the response bytes
    # The first byte is junk, and the next three contain the 10 bits we want
    adc_value = ((response[1] & 0x03) << 8) | response[2]
    return adc_value


def get_current(adc_value):
    """
    Converts the ADC value to a current reading in Amperes using the ACS712's sensitivity.

    Args:
        adc_value: The 10-bit ADC value from the MCP3008.

    Returns:
        The current in Amperes.
    """
    # ACS712 Parameters (CHANGE THESE VALUES TO MATCH YOUR SPECIFIC ACS712!)
    #  These values are from the ACS712 datasheet.  You MUST adjust them.
    VCC = 5.0  # Volts (supply voltage to the ACS712 and MCP3008)
    ZERO_CURRENT_VOLTAGE = VCC / 2.0  # For a 5V supply, this is 2.5V
    SENSITIVITY = 0.066  # Volts per Amp (for the 30A version)  <-- CHANGED THIS
    #  SENSITIVITY = 0.100  # Volts per Amp (for the 100mV/A version)
    #  SENSITIVITY = 0.185 #for 5A

    # Convert ADC value to voltage
    voltage = (adc_value * VCC) / 1023.0  # 10-bit ADC: 0-1023

    # Calculate current
    current = (voltage - ZERO_CURRENT_VOLTAGE) / SENSITIVITY
    return current



if __name__ == "__main__":
    try:
        while True:
            # Read the ADC value from the MCP3008
            adc_value = read_mcp3008(ACS712_CHANNEL)

            # Convert the ADC value to current
            current_amps = get_current(adc_value)

            # Print the results
            print(f"ADC Value: {adc_value}, Current: {current_amps:.3f} A")
            time.sleep(0.5)  # Read every half second

    except KeyboardInterrupt:
        print("Script stopped by user")
    finally:
        spi.close()  # Clean up the SPI connection
