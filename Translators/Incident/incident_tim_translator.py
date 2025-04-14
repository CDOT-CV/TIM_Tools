import logging
from pgquery import query_db
from incident_tim_generator import get_action, get_effect, get_point, get_itis_codes, calculate_direction
from active_tim import active_tim

class IncidentFeature:
    def __init__(self, properties, geometry):
        self.id = properties["id"].replace("_", "-")
        self.route_name = properties["routeName"].replace("_", "-")
        self.problem = properties["type"]
        self.additional_impacts = [] if properties.get("additionalImpacts") == None else properties["additionalImpacts"]
        self.lane_impacts = properties["laneImpacts"]
        self.traveler_information_message = properties["travelerInformationMessage"]
        self.geometry = geometry["coordinates"]
        self.geometry_type = geometry["type"]


    def get_id(self):
        return self.id
    
    def get_route_name(self):
        return self.route_name
    
    def get_problem(self):
        return self.problem
    
    def get_additional_impacts(self):
        return self.additional_impacts
    
    def get_lane_impacts(self):
        return self.lane_impacts
    
    def get_traveler_information_message(self):
        return self.traveler_information_message
    
    def get_geometry(self):
        return self.geometry
    
    def get_geometry_type(self):
        return self.geometry_type
    

def translate(incident_geojson):
    """Translates a GeoJSON representation of incidents into a TIM (Traffic Incident Management) format.

    This function iterates through the features in the input GeoJSON, extracts relevant
    properties and geometry, and transforms them into a TIM-Manager-compliant dictionary.
    It handles both point and linestring geometries, calculates TIM direction,
    and retrieves information such as route, problem, effect, and action from the input GeoJSON. 
    It also checks for active TIM records by clientID to avoid duplicates.

    Args:
        incident_geojson (dict): A GeoJSON dictionary containing incident features.
            Each feature should have 'properties' and 'geometry' keys.

    Returns:
        dict: A dictionary containing a list of TIM incident dictionaries under the key
            'timIncidentList'.  Returns an empty list if no features are processed.
    """
    
    tims = {"timIncidentList": []}

    for feature in incident_geojson["features"]:
        feature = IncidentFeature(feature["properties"], feature["geometry"])
        tim_body = {}
        tim_body["clientId"] = feature.get_id()
        tim_body["incidentId"] = feature.get_id()
        if feature.get_geometry_type() == "Point":
            tim_body["startPoint"] = get_point(feature.get_geometry())
            tim_body["endPoint"] = get_point(feature.get_geometry())
            tim_body["direction"] = "I"
        else:
            tim_body["startPoint"] = get_point(feature.get_geometry()[0])
            tim_body["endPoint"] = get_point(feature.get_geometry()[-1])
            tim_body["direction"] = calculate_direction(feature.get_geometry())
        tim_body["route"] = feature.get_route_name()
        tim_body["highway"] = feature.get_route_name()
        tim_body["problem"] = feature.get_problem()
        tim_body["effect"] = get_effect(feature.get_lane_impacts(), feature.get_additional_impacts())
        tim_body["action"] = get_action(tim_body, feature)
        tim_body["itisCodes"] = get_itis_codes(tim_body)
        active_tim_record = active_tim("I", tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['clientId']}")
            continue
        tims["timIncidentList"].append(tim_body)
    return tims
