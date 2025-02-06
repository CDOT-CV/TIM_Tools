from Translators.Shared import itis_codes
from Translators.WeatherStations import ws_tim_generator

############################ getItisCodes ############################
def test_get_itis_codes_surface_value_snow():
    road_surface_sensor = [{"currentReading": "9"}]
    wind_gust_sensor = [{"currentReading": 0}]
    avg_wind_speed_sensor = [{"currentReading": 0}]
    itisCodes = ws_tim_generator.get_itis_codes(road_surface_sensor, wind_gust_sensor, avg_wind_speed_sensor)
    assert itisCodes == [itis_codes.ItisCodes.SNOW.value]

def test_get_itis_codes_surface_value_rain():
    road_surface_sensor = [{"currentReading": "11"}]
    wind_gust_sensor = [{"currentReading": 0}]
    avg_wind_speed_sensor = [{"currentReading": 0}]
    itisCodes = ws_tim_generator.get_itis_codes(road_surface_sensor, wind_gust_sensor, avg_wind_speed_sensor)
    assert itisCodes == [itis_codes.ItisCodes.RAIN.value, itis_codes.ItisCodes.WET_PAVEMENT.value]

def test_get_itis_codes_surface_value_ice():
    road_surface_sensor = [{"currentReading": "15"}]
    wind_gust_sensor = [{"currentReading": 0}]
    avg_wind_speed_sensor = [{"currentReading": 0}]
    itisCodes = ws_tim_generator.get_itis_codes(road_surface_sensor, wind_gust_sensor, avg_wind_speed_sensor)
    assert itisCodes == [itis_codes.ItisCodes.ICE.value]

def test_get_itis_codes_wind_speed_value():
    road_surface_sensor = [{"currentReading": "0"}]
    wind_gust_sensor = [{"currentReading": 10}]
    avg_wind_speed_sensor = [{"currentReading": 10}]
    itisCodes = ws_tim_generator.get_itis_codes(road_surface_sensor, wind_gust_sensor, avg_wind_speed_sensor)
    assert itisCodes == [itis_codes.ItisCodes.STRONG_WINDS.value]


def test_get_itis_codes_wind_gust_value():
    road_surface_sensor = [{"currentReading": "3"}]
    wind_gust_sensor = [{"currentReading": 10}]
    avg_wind_speed_sensor = [{"currentReading": 0}]
    itisCodes = ws_tim_generator.get_itis_codes(road_surface_sensor, wind_gust_sensor, avg_wind_speed_sensor)
    assert itisCodes == [itis_codes.ItisCodes.STRONG_WINDS.value]

def test_get_itis_codes_no_value():
    road_surface_sensor = [{"currentReading": "3"}]
    wind_gust_sensor = [{"currentReading": 0}]
    avg_wind_speed_sensor = [{"currentReading": 0}]
    itisCodes = ws_tim_generator.get_itis_codes(road_surface_sensor, wind_gust_sensor, avg_wind_speed_sensor)
    assert itisCodes == []


############################ getGeometry ############################

def test_get_geometry_single_coordinate():
    geometry = [[-122.403, 37.795]]
    annotated_geometry = ws_tim_generator.get_geometry(geometry)
    assert annotated_geometry == [{'latitude': 37.795, 'longitude': -122.403}]
