import re
from Translators.Shared.itis_codes import ItisCodes

def get_itis_codes(tim_body):
    """Extracts relevant ITIS codes based on keywords found in the incident's description.
        
    Args:
        tim_body (dict): A dictionary containing incident details, including 'effect', 'action', and 'problem' fields.
        
    Returns:
        list: A list of ITIS codes (strings) that match the keywords found in the incident details.
                Returns an empty list if no matching keywords are found.
    """

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

def get_effect(impacts, additional_effects=None):
    effect = ""
    for additional_effect in additional_effects:
        effect += f"{additional_effect}. "
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
        action += "Reduce Speeds."
    if re.search(tires_chains_required_pattern, feature.get_traveler_information_message()) or re.search(type_tires_chains_required_pattern, tim_body["problem"]):
        action += "Chains Required."

    return action

def calculate_direction(coordinates):
    """Calculates the general direction of travel based on a list of coordinates.
    
    Args:
        coordinates (list of tuples): A list of (longitude, latitude) tuples representing the path of travel.
    Returns:
        str: A string representing the direction of travel.  "I" for increasing, "D" for decreasing, 
            or "unknown" if the direction cannot be determined.
            Direction is determined based on the greatest difference between the first and last coordinates.
            If only one coordinate is provided, returns "unknown".
            If a ValueError or IndexError occurs during calculation, returns "unknown".
            If two identical coordinates are provided, returns "unknown".
    """
    
    direction = "unknown"
    if (len(coordinates) == 1):
        return direction
    
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
    elif lat_dif < 0:
        # southbound
        direction = "D"
    return direction