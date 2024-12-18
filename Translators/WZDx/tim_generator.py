import math
import copy
import os
import secrets
from datetime import datetime
import geospatial_service
from itis_codes import ItisCodes, ItisCodeExtraKeywords
from utils import calculate_direction


# calculate anchor point 15 meters from start of path
def calculate_anchor(p1, p2):
    # assumes (lat, long) tuples
    if p1 == p2:
        return {"latitude": p1[0], "longitude": p1[1]}

    # calculate difference between latitude and longitude
    dlat = p1[0] - p2[0]
    dlon = p1[1] - p2[1]

    # convert from degrees of lat/lon to meters
    D0lat = 111195 * dlat
    D0lon = 111195 * math.cos(math.radians(p1[0])) * dlon

    # calculate total distance between two points (in meters)
    D0 = math.sqrt(math.pow(D0lat, 2) + math.pow(D0lon, 2))

    # calculate how far 15 meters is (given total distance between two points above)
    md = 15 / D0

    # convert back to lat/lon (uses difference calculated above to determine anchor point)
    palat = p1[0] + (md * dlat)
    palon = p1[1] + (md * dlon)

    return {"latitude": palat, "longitude": palon}


def get_anchor(feature):
    coords = feature["geometry"]["coordinates"]
    return calculate_anchor((coords[0][1], coords[0][0]), (coords[1][1], coords[1][0]))


def get_itis_codes(feature):
    itisCodes = []

    # Check for vehicle_impact ITIS code
    vehicleImpact = feature["properties"]["vehicle_impact"]
    if vehicleImpact == "all-lanes-closed":
        itisCodes.append(ItisCodes.CLOSED.value)

    # Check for types_of_work ITIS codes
    properties = feature["properties"]
    if "types_of_work" in properties:
        for entry in properties["types_of_work"]:
            if entry == {
                "type_name": "roadway-creation",
                "is_architectural_change": True,
            }:
                itisCodes.append(ItisCodes.ROAD_CONSTRUCTION.value)

    # Check for ITIS codes present in description
    description = feature["properties"]["core_details"]["description"]
    for key in ItisCodes:
        searchKey = key.name.replace("_", " ").lower()
        if searchKey in description.lower() and key.value not in itisCodes:
            itisCodes.append(key.value)
        elif searchKey in ItisCodeExtraKeywords:
            if (
                ItisCodeExtraKeywords[searchKey] in description.lower()
                and key.value not in itisCodes
            ):
                itisCodes.append(key.value)

    return itisCodes


def calculate_offset_path(coords, anchor):
    """Creates an offset path from passed in coordinates and anchor point

    Parameters:
        coords (list): A list of coordinates
        anchor (dict): A coordinate representing the anchor point, or initial point to begin from

    Returns:
        offsetPath (dict): A path object with offset ll nodes"""
    # loop through coords and calculate offset path
    startLat = float(anchor["latitude"])
    startLon = float(anchor["longitude"])
    nodes = []
    coords_len = len(coords)
    if coords_len == 1:
        # Per J2735, NodeSetLL's must contain at least 2 nodes. ODE will fail to
        # PER-encode TIM if we supply less than 2. If we only have 1 node for the path,
        # include a node with an offset of (0, 0) which is effectively a point that's
        # right on top of the anchor point.
        nodes.append({"delta": "node-LL", "nodeLat": 0, "nodeLong": 0})

    for i in range(coords_len):
        latOffset = float(coords[i][1]) - startLat
        lonOffset = float(coords[i][0]) - startLon
        nodes.append({"delta": "node-LL", "nodeLat": latOffset, "nodeLong": lonOffset})
        startLon = float(coords[i][0])
        startLat = float(coords[i][1])
    path = {"scale": 0, "nodes": nodes, "type": "ll"}
    return path


def get_region(coords, anchor, roadName):
    # TODO: update fields, name (for directionality)
    return {
        "name": f"I_{roadName}_IDENTIFIER",
        "anchorPosition": anchor,
        "laneWidth": "50",  # defaulting lane width to 50
        "directionality": "3",  # 0 - unavailable, 1 - forward, 2 - backward, 3 - both
        "closedPath": "false",  # default
        "description": "path",  # default
        "path": calculate_offset_path(coords, anchor),
        "direction": calculate_direction(coords, anchor),
    }


def get_msg_id(anchor):
    """Generates a MsgId object, with roadSignID

    Parameters:
        anchor (dict): A coordinate representing the anchor point to display the message at

    Returns:
        MsgId (dict): A MsgId object"""

    return {
        "roadSignID": {
            # if speed limit or road signage, then "regulatory" else "warning"
            "mutcdCode": "warning",
            "viewAngle": "1111111111111111",  # default view angle
            "position": {
                "latitude": anchor["latitude"],
                "longitude": anchor["longitude"],
            },
        }
    }


def get_work_zone_data_frame(start_date, duration, msgId, regions):
    return {
        "startDateTime": start_date,
        "durationTime": duration,
        "sspTimRights": "1",  # default value
        "frameType": "advisory",  # TODO: determine frame type
        "msgId": msgId,
        "priority": "5",  # default value
        "sspLocationRights": "1",  # default value
        "regions": regions,
        "sspMsgTypes": "1",  # default value
        "sspMsgContent": "1",  # default value
        "content": "workZone",
        "items": [ItisCodes.ROAD_CONSTRUCTION.value],
        "url": "null",
    }


def get_content_type(feature):
    # TODO: determine content type
    return "advisory"


def get_vehicle_impact_data_frame(feature, start_date, duration, msgId, regions):
    dframe = {
        "startDateTime": start_date,
        "durationTime": duration,
        "sspTimRights": "1",  # default value
        "frameType": "advisory",  # TODO: determine frame type
        "msgId": msgId,
        "priority": "5",  # default value
        "sspLocationRights": "1",  # default value
        "regions": regions,
        "sspMsgTypes": "1",  # default value
        "sspMsgContent": "1",  # default value
        "content": get_content_type(feature),
        "items": get_itis_codes(feature),
        "url": "null",
    }
    return dframe


def vehicle_impact_supported(vehicle_impact):
    if vehicle_impact == "all-lanes-closed":
        return True
    return False


def get_first_road_name(feature):
    return feature["properties"]["core_details"]["road_names"][0]


def get_start_date(feature):
    # if utcnow > start_date, then set time to be utcnow
    # else if utcnow < start_date, then set time to be start_date
    if (
        datetime.utcnow()
        - datetime.strptime(feature["properties"]["start_date"], "%Y-%m-%dT%H:%M:%SZ")
    ).total_seconds() >= 0:
        return (datetime.utcnow()).isoformat()[:-3] + "Z"
    else:
        return feature["properties"]["start_date"]


def get_data_frames(feature):
    coords = copy.deepcopy(feature["geometry"]["coordinates"])
    # ensure we have the minimum 3 nodes to create a path
    # 2 is valid per spec and may be accepted later, however in the WZDx case if we have only two points it is just the start/end point and may not be on the same road
    # for now, skip these cases
    if len(coords) <= 2:
        return None
    anchor = get_anchor(feature)
    if anchor is None:
        return None
    start_date = get_start_date(feature)
    duration = os.getenv("DURATION_TIME", 30)
    msgId = get_msg_id(anchor)

    # In here need to calculate if size of path is greater than 63
    # then generate regions accordingly
    maxLength = 62
    msgLength = len(feature["geometry"]["coordinates"])
    regions = []
    if msgLength > maxLength:
        numPaths = math.ceil(msgLength / maxLength)
        pathLength = (int)(msgLength / numPaths)
        remainder = msgLength % pathLength

        for index in range(0, numPaths):
            rangeEnd = pathLength + 1 if index < remainder else pathLength
            regionCoords = coords[0:rangeEnd]
            anchor = get_anchor(feature)
            regions.append(
                get_region(regionCoords, anchor, roadName=get_first_road_name(feature))
            )
            del coords[0:rangeEnd]
    else:
        regions = [get_region(coords, anchor, roadName=get_first_road_name(feature))]

    data_frames = [get_work_zone_data_frame(start_date, duration, msgId, regions)]

    # TODO: add additional data frames as appropriate
    vehicle_Impact = feature["properties"]["vehicle_impact"]
    if vehicle_impact_supported(vehicle_Impact):
        vehicle_impact_dataFrame = get_vehicle_impact_data_frame(
            feature, start_date, duration, msgId, regions
        )
        data_frames.append(vehicle_impact_dataFrame)

    return data_frames


def generate_tim(feature):
    data_frames = get_data_frames(feature)
    if data_frames is None:
        return None

    tim_body = {
        "msgCnt": "1",
        "timeStamp": feature["properties"]["core_details"]["update_date"],
        "packetID": secrets.token_hex(9).upper(),  # "67AEF692F8BB63067D",
        "urlB": "null",
        "dataframes": data_frames,
    }
    return tim_body

def get_bearing(feature):
    direction = feature["properties"]["core_details"]["direction"].lower()
    if direction == "northbound":
        return 0
    elif direction == "eastbound":
        return 270
    elif direction == "southbound":
        return 180
    elif direction == "westbound":
        return 90
    
def get_geometry(geometry):
    annotated_geometry = []
    for coord in geometry:
        annotated_geometry.append({"latitude": coord[1], "longitude": coord[0]})
    return annotated_geometry
