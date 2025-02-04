from datetime import datetime
import logging
from pgquery import query_db
from active_tim import active_tim
from pe_tim_generator import get_geometry, get_itis_codes

class PlannedEventsFeature:
    def __init__(self, properties, geometry):
        self.id = properties["id"].replace("_", "-")
        self.route = properties["routeName"].replace("_", "-")
        self.geometry = geometry
        self.additional_impacts = properties["additionalImpacts"]

    # need additional impacts for direction

    def get_id(self):
        return self.id
    
    def get_client_id(self):
        return self.id.replace("/", "-")
    
    def get_route(self):
        return self.route
    
    def get_geometry(self):
        return self.geometry
    
    def get_additional_impacts(self):
        return self.additional_impacts
    
def calculate_direction(coordinates):
    try:
        long_dif = coordinates[-1][0] - coordinates[0][0]
        lat_dif = coordinates[-1][1] - coordinates[0][1]
    except ValueError as e:
        return "unknown"
    except IndexError as e:
        return "unknown"

    if abs(long_dif) > abs(lat_dif):
        if long_dif > 0:
            # eastbound
            direction = "I"
        else:
            # westbound
            direction = "D"
    elif lat_dif > 0:
        # northbound
        direction = "I"
    else:
        # southbound
        direction = "D"
    return direction

def is_both_directions(additional_impacts):
    for entry in additional_impacts:
        if entry.lower() == "impacts both directions":
            return True
    return False

def translate(rc_geojson):
    tims = {"timRcList": []}

    for feature in rc_geojson["features"]:
        if feature["properties"]["type"].lower() != "closed for the season":
            continue
        feature = PlannedEventsFeature(feature["properties"], feature["geometry"]["coordinates"])
        tim_body = {}
        tim_body["clientId"] = feature.get_client_id()
        tim_body["direction"] = "B" if is_both_directions(feature.get_additional_impacts()) else calculate_direction(feature.get_geometry())
        tim_body["route"] = feature.get_route()
        tim_body["roadCode"] = feature.get_id()
        tim_body["itisCodes"] = get_itis_codes()
        tim_body["geometry"] = get_geometry(feature.get_geometry())
        tim_body["advisory"] = []
        active_tim_record = active_tim("RC", tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['clientId']}")
            continue
        tims["timRcList"].append(tim_body)
    return tims