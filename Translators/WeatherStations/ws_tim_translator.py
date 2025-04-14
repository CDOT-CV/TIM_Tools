import logging
from pgquery import query_db
from active_tim import active_tim
from ws_tim_generator import get_geometry, get_itis_codes

class WeatherStationFeature:
    def __init__(self, properties, geometry):
        self.id = properties["id"].replace("_", "-")
        self.route = properties["routeName"].replace("_", "-")
        self.geometry = geometry
        self.direction = properties["direction"]
        self.surface_status_sensor = [sensor for sensor in properties["sensors"] \
                                        if sensor["type"] is not None and sensor["type"].lower() == "road surface status"]
        self.wind_gust_sensor = [sensor for sensor in properties["sensors"] \
                                        if sensor["type"] is not None and sensor["type"] == "gust wind speed"]
        self.avg_wind_speed_sensor = [sensor for sensor in properties["sensors"] \
                                        if sensor["type"] is not None and sensor["type"] == "average wind speed"]

    def get_id(self):
        return self.id
    
    def get_client_id(self):
        return self.id.replace("/", "-")
    
    def get_route(self):
        return self.route
    
    def get_geometry(self):
        return self.geometry
    
    def get_direction(self):
        return self.direction
    
    def get_surface_status_sensor(self):
        return self.surface_status_sensor
    
    def get_wind_gust_sensor(self):
        return self.wind_gust_sensor
    
    def get_avg_wind_speed_sensor(self):
        return self.avg_wind_speed_sensor
    
def calculate_direction(direction):
    if (direction.lower() == "n" or direction.lower() == "e"):
        return "I"
    else:
        return "D"

def translate(ws_geojson):
    """Translates weather station GeoJSON data into a TIM-Manager compatible format.

    This function iterates through the features in the input GeoJSON, extracts relevant
    properties and geometry, and transforms them into a TIM record. It calculates
    direction, retrieves route and road codes, determines ITIS codes based on sensor data,
    and formats the geometry. It also checks for active TIM records to avoid duplicates.

    Args:
        ws_geojson (dict): A dictionary representing the weather station data in GeoJSON format.
                            It should contain a "features" key, where each feature is a
                            dictionary with "properties" and "geometry" keys.

    Returns:
        dict: A dictionary containing a list of TIM records under the "timRcList" key.
    """

    tims = {"timRcList": []}

    for feature in ws_geojson["features"]:
        feature = WeatherStationFeature(feature["properties"], feature["geometry"])
        tim_body = {}
        tim_body["clientId"] = feature.get_client_id()
        tim_body["direction"] = calculate_direction(feature.get_direction())
        tim_body["route"] = feature.get_route()
        tim_body["roadCode"] = feature.get_id()
        tim_body["itisCodes"] = get_itis_codes(feature.get_surface_status_sensor(), \
                                                feature.get_wind_gust_sensor(), \
                                                feature.get_avg_wind_speed_sensor())
        tim_body["geometry"] = get_geometry(feature.get_geometry())
        tim_body["advisory"] = []
        active_tim_record = active_tim("RC", tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['clientId']}")
            continue
        tims["timRcList"].append(tim_body)
    return tims