import os
from Translators.Shared.itis_codes import ItisCodes
from sensor_values import sensor_values, WIND_SPEED_CONSTANT
import re

def get_itis_codes(road_surface_sensor, wind_gust_sensor, avg_wind_speed_sensor):
    itis_codes = []

    # Only set ITIS codes if the road surface sensor is present
    if len(road_surface_sensor) > 0:
        rs_value = sensor_values.get(road_surface_sensor[0]["currentReading"], "None")
        if re.search(r"snow", rs_value, re.IGNORECASE):
            itis_codes.append(ItisCodes.SNOW.value)
        elif re.search(r"rain", rs_value, re.IGNORECASE):
            itis_codes.append(ItisCodes.RAIN.value)
            itis_codes.append(ItisCodes.WET_PAVEMENT.value)
        elif re.search(r"frozen", rs_value, re.IGNORECASE):
            itis_codes.append(ItisCodes.ICE.value)

    # Only set ITIS codes if the average wind speed sensor is over threshold
    if len(avg_wind_speed_sensor) == 1:
        avg_wind_speed_value = avg_wind_speed_sensor[0]["currentReading"]
        mph_wind_speed_value = float(avg_wind_speed_value) * WIND_SPEED_CONSTANT
        mph_wind_speed_threshold = float(os.getenv("HIGH_WIND_THRESHOLD", 20))
        if mph_wind_speed_value >= mph_wind_speed_threshold:
            itis_codes.append(ItisCodes.STRONG_WINDS.value)

    # Set ITIS codes if the wind gust sensor is over threshold and strong winds are not already set
    if len(wind_gust_sensor) == 1 and ItisCodes.STRONG_WINDS.value not in itis_codes:
        wind_gust_value = wind_gust_sensor[0]["currentReading"]
        mph_gust_value = float(wind_gust_value) * WIND_SPEED_CONSTANT
        mph_gust_threshold = float(os.getenv("HIGH_WIND_THRESHOLD", 20))
        if mph_gust_value >= mph_gust_threshold:
            itis_codes.append(ItisCodes.STRONG_WINDS.value)

    return itis_codes

def get_geometry(geometry):
    annotated_geometry = []
    coords = geometry["coordinates"]
    # handle point geometry
    if geometry["type"] == "Point":
        annotated_geometry.append({"latitude": coords[1], "longitude": coords[0]})
        return annotated_geometry
    
    for coord in coords:
        annotated_geometry.append({"latitude": coord[1], "longitude": coord[0]})
    return annotated_geometry
