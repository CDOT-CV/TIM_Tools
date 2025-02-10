import re
from itis_codes import ItisCodes

def get_itis_codes(tim_body):
    itisCodes = []

    speed_reduce_pattern = r"(?i)(reduce speeds?)"
    chains_required_pattern = r"(?i)(chains required)"
    maintenance_pattern = r"(?i)(maintenance operations?)"

    if re.search(speed_reduce_pattern, tim_body["effect"]) or re.search(speed_reduce_pattern, tim_body["action"]):
        itisCodes.append(ItisCodes.REDUCE_YOUR_SPEED.value)
    if re.search(chains_required_pattern, tim_body["effect"]) or re.search(chains_required_pattern, tim_body["action"]):
        itisCodes.append(ItisCodes.SNOW_TIRES_OR_CHAINS_REQUIRED.value)
    if re.search(maintenance_pattern, tim_body["problem"]):
        itisCodes.append(ItisCodes.LOOK_OUT_FOR_WORKERS.value)
    return itisCodes

def get_point(coordinates):
    return {"latitude": coordinates[1], "longitude": coordinates[0], "valid": True}

def get_effect(impacts, addtl_effects=None):
    effect = ""
    for addtl_effect in addtl_effects:
        effect += f"{addtl_effect}. "
    for impact in impacts:
        if impact["laneClosures"] != "0":
            for lane in impact["closedLaneTypes"]:
                effect += f"{impact['direction']}bound {lane} closed. "
    return effect[:-1]

def get_action(tim_body, feature):
    action = ""
    speed_reduce_pattern = r"(?i)(Speeds? reduced|Reduce speed|Speed is reduced|Speed limit reduced|Slower speeds?|Slower speeds? are advised)"
    tires_chains_required_pattern = r"(?i)(Chains required|Snow tires required|Snow chains required|Tires required|Chains or snow tires required|Snow tires or chains required)"
    type_tires_chains_required_pattern = r"(?i)(Traction|Chain)(/Chain)? Law Code (15|18)(\s+and\s+18)?"
    if re.search(speed_reduce_pattern, feature.get_traveler_information_message()) or re.search(speed_reduce_pattern, tim_body["effect"]):
        action += "Reduce Speeds. "
    if re.search(tires_chains_required_pattern, feature.get_traveler_information_message()) or re.search(type_tires_chains_required_pattern, tim_body["problem"]):
        action += "Chains Required."

    return action

def calculate_direction(coordinates):
    
    if (len(coordinates) == 1):
        return "unknown"
    
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