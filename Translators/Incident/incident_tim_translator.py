import logging
from pgquery import query_db
from incident_tim_generator import get_action, get_effect, get_point, get_itis_codes, calculate_direction

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
        active_tim_record = active_tim(tim_body)
        if active_tim_record:
            logging.info(f"TIM already active for record: {tim_body['clientId']}")
            continue
        tims["timIncidentList"].append(tim_body)
    return tims

def active_tim(tim_body):
    tim_id = tim_body["clientId"]
    # if TIM has an active TIM holding record that is current & info is the same as the current TIM record, then do not update
    active_tim_holding = query_db(f"SELECT * FROM active_tim_holding WHERE client_id LIKE '%{tim_id}%'")
    if len(active_tim_holding) > 0:
        active_tim_holding = active_tim_holding[0]
        return (active_tim_holding["direction"] == tim_body["direction"] and 
            f"{active_tim_holding['start_latitude']:.8f}" == f"{tim_body['geometry'][0]['latitude']:.8f}" and 
            f"{active_tim_holding['start_longitude']:.8f}" == f"{tim_body['geometry'][0]['longitude']:.8f}" and 
            f"{active_tim_holding['end_latitude']:.8f}" == f"{tim_body['geometry'][-1]['latitude']:.8f}" and 
            f"{active_tim_holding['end_longitude']:.8f}" == f"{tim_body['geometry'][-1]['longitude']:.8f}")

    # if TIM has an active TIM record that is current & info is the same as the current TIM record, then do not update
    active_tim = query_db(f"SELECT * FROM active_tim WHERE client_id LIKE '%{tim_id}%' AND tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = 'I') AND marked_for_deletion = false")
    if len(active_tim) > 0:
        active_tim = active_tim[0]
        return (active_tim["direction"] == tim_body["direction"] and
            f"{active_tim['start_latitude']:.8f}" == f"{tim_body['geometry'][0]['latitude']:.8f}" and
            f"{active_tim['start_longitude']:.8f}" == f"{tim_body['geometry'][0]['longitude']:.8f}" and
            f"{active_tim['end_latitude']:.8f}" == f"{tim_body['geometry'][-1]['latitude']:.8f}" and
            f"{active_tim['end_longitude']:.8f}" == f"{tim_body['geometry'][-1]['longitude']:.8f}")
