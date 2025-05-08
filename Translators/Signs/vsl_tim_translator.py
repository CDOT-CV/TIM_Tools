import logging
from vsl_tim_generator import get_geometry, get_itis_codes
from Translators.Shared.active_tim import active_tim

class VariableSpeedLimitFeature:
    def __init__(self, properties, geometry):
        self.id = properties["id"].replace("_", "-")
        self.route = properties["routeName"].replace("_", "-")
        self.geometry = geometry
        self.direction = properties["direction"]
        self.speed = properties["speed"] if "speed" in properties else None

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
    
    def get_speed(self):
        return self.speed
    
def calculate_direction(direction):
    if direction.lower() == "east" or direction.lower() == "north":
        return "I"
    return "D"

def translate(vsl_geojson):
    tims = {"timVslList": []}

    for feature in vsl_geojson["features"]:
        if feature["properties"]["communicationStatus"].lower() != "operational" \
            or feature["properties"]["displayStatus"].lower() != "on" \
            or "speed" not in feature["properties"]:
            continue
        feature = VariableSpeedLimitFeature(feature["properties"], feature["geometry"])
        tim_body = {}
        tim_body["clientId"] = feature.get_client_id()
        tim_body["deviceId"] = feature.get_client_id()
        tim_body["direction"] = calculate_direction(feature.get_direction())
        tim_body["route"] = feature.get_route()
        tim_body["roadCode"] = feature.get_id()
        tim_body["itisCodes"] = get_itis_codes()
        tim_body["geometry"] = get_geometry(feature.get_geometry())
        tim_body["advisory"] = []
        tim_body["speed"] = feature.get_speed()
        tim_body["buffers"] = [1]
        active_tim_record = active_tim("VSL", tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['clientId']}")
            continue
        tims["timVslList"].append(tim_body)
    return tims
