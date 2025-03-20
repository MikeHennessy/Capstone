import math
import datetime
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# Calculate solar declination angle (in radians)
def calculate_declination(day_of_year):
    return -23.45 * math.cos(math.radians(360/365 * (day_of_year+10)))

def get_utc_offset(lat, lon):
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lat=lat, lng=lon)
    if timezone_name is None:
        return "Time zone not found"
    
    timezone = pytz.timezone(timezone_name)
    now = datetime.datetime.now(timezone)
    utc_offset = now.utcoffset().total_seconds() / 3600
    return utc_offset

# Calculate solar hour angle (in radians)
def calculate_hour_angle(hour, minute, day_of_year, lat, lon):
    LSTM = 15 * get_utc_offset(lat, lon)
    B = 360/365 * (day_of_year - 81)
    EoT = 9.87*math.sin(math.radians(2*B)) - 7.53*math.cos(math.radians(B)) - 1.5*math.sin(math.radians(B))
    TC = 4*(lon - LSTM) + EoT
    LST = hour + (minute/60) + (TC/60)
    HRA = 15*(LST - 12)
    return HRA

# Calculate solar altitude angle (in radians)
def calculate_altitude_angle(lat, dec, HA):
    latitude = math.radians(lat)
    declination = math.radians(dec)
    hour_angle = math.radians(HA)
    return math.degrees(math.asin(math.sin(latitude) * math.sin(declination) +
                     math.cos(latitude) * math.cos(declination) * math.cos(hour_angle)))

# Calculate solar azimuth angle (in radians)
def calculate_azimuth_angle(lat, dec, alt, ha):
    latitude = math.radians(lat)
    declination = math.radians(dec)
    altitude_angle = math.radians(alt)
    HRA = math.radians(ha)
    numerator = math.sin(declination) * math.cos(latitude) - math.cos(declination)*math.sin(latitude)*math.cos(HRA)
    denominator = math.cos(altitude_angle)
    azimuth = math.degrees(math.acos(numerator / denominator))
    # Adjust azimuth angle for hemisphere
    if lat > 0:  # Northern Hemisphere
        if ha > 0:  # Afternoon (sun is in the western sky)
            azimuth = 360 - azimuth  # Reflect angle from north
    else:  # Southern Hemisphere
        if ha < 0:  # Afternoon (sun is in the western sky)
            azimuth = 360 - azimuth  # Reflect angle from north to south
    
    return azimuth

# Get the day of the year from the current date
def get_day_of_year():
    now = datetime.datetime.now()
    return now.timetuple().tm_yday

# Get the Raspberry Pi's current date and time
def get_current_datetime():
    return datetime.datetime.now()

# Get the Raspberry Pi's latitude and longitude using the geopy library
def get_latitude_longitude():
    try:
        # Use an IP geolocation API to determine location
        response = requests.get("http://ip-api.com/json")
        data = response.json()
        if data["status"] == "success":
            return data["lat"], data["lon"]
        else:
            raise Exception("Could not determine location from IP.")
    except Exception as e:
        print(f"Error determining location: {e}")
        return None, None

# Main function
def main():
    # Get current date and time
    now = get_current_datetime()
    hour = now.hour
    minute = now.minute

    # Get the Raspberry Pi's latitude and longitude
    latitude, longitude = get_latitude_longitude()
    if latitude is None or longitude is None:
        print("Unable to determine location. Please provide latitude and longitude manually.")
        return

    # Calculate day of the year
    day_of_year = get_day_of_year()

    # Calculate solar angles
    declination = calculate_declination(day_of_year)
    hour_angle = calculate_hour_angle(hour, minute, day_of_year, latitude, longitude)
    altitude_angle = calculate_altitude_angle(latitude, declination, hour_angle)
    azimuth_angle = calculate_azimuth_angle(latitude, declination, altitude_angle, hour_angle)

    # Calculate optimal E-W and N-S tilts
    corrected_azimuth_angle = 180 - azimuth_angle
    ns_tilt = altitude_angle if -30 <= altitude_angle <= 30 else max(-30, min(30, altitude_angle)) # Clamp N-S tilt to a minimum of 0
    ew_tilt = corrected_azimuth_angle if -40 <= corrected_azimuth_angle <= 40 else max(-40, min(40, corrected_azimuth_angle))

    # Output results
    print(f"Optimal North-South tilt (from horizontal): {ns_tilt:.2f} degrees")
    print(f"Optimal East-West tilt (from center): {ew_tilt:.2f} degrees")

if __name__ == "__main__":
    main()
