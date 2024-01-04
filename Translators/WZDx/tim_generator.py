import math
import copy
import secrets
from datetime import datetime
import geospatial_service
from itis_codes import ItisCodes
from utils import calculate_direction
import logging


def get_duration_time_minutes(feature):
    '''Get duration in minutes from a GeoJSON feature object with start_date and end_date properties

    Parameters:
        feature (dict): A GeoJSON feature object. Assumed to have properties 'start_date' and 'end_date'

    Returns:
        duration (int): Duration in minutes. Note 32000 represents infinity'''
    # "start_date": "2022-02-13T16:00:00Z",
    # "end_date": "2022-02-13T16:55:00Z",
    start_date = datetime.strptime(feature[
        "properties"]["start_date"], "%Y-%m-%dT%H:%M:%SZ")
    end_date = datetime.strptime(feature[
        "properties"]["end_date"], "%Y-%m-%dT%H:%M:%SZ")
    duration = (end_date - start_date).total_seconds() / 60
    return int(duration) if duration < 32000 else 32000


def get_anchor(feature):
    coords = feature["geometry"]["coordinates"]
    route = geospatial_service.point_to_route_id(
        feature["geometry"]["coordinates"][0][0], feature["geometry"]["coordinates"][0][1])
    # route = translateRoute(feature["properties"]["core_details"]["road_names"])
    if route is None:
        return None
    logging.info('found route ' + route)
    return geospatial_service.get_upstream_point(coords, route, 0.25)


def get_itis_codes(feature):
    # TODO: calculate itis codes
    itisCodes = []

    vehicleImpact = feature["properties"]["vehicle_impact"]
    if vehicleImpact == "all-lanes-closed":
        itisCodes.append(ItisCodes.CLOSED.value)

    return itisCodes


def calculate_offset_path(coords, anchor):
    '''Creates an offset path from passed in coordinates and anchor point

    Parameters:
        coords (list): A list of coordinates
        anchor (dict): A coordinate representing the anchor point, or initial point to begin from

    Returns:
        offsetPath (dict): A path object with offset ll nodes'''
    # loop through coords and calculate offset path
    startLat = float(anchor["latitude"])
    startLon = float(anchor["longitude"])
    nodes = []
    coords_len = len(coords)
    if (coords_len == 1):
        # Per J2735, NodeSetLL's must contain at least 2 nodes. ODE will fail to
        # PER-encode TIM if we supply less than 2. If we only have 1 node for the path,
        # include a node with an offset of (0, 0) which is effectively a point that's
        # right on top of the anchor point.
        nodes.append({
            "delta": "node-LL",
            "nodeLat": 0,
            "nodeLong": 0
        })

    for i in range(coords_len):
        latOffset = float(coords[i][1]) - startLat
        lonOffset = float(coords[i][0]) - startLon
        nodes.append({
            "delta": "node-LL",
            "nodeLat": latOffset,
            "nodeLong": lonOffset
        })
        startLon = float(coords[i][0])
        startLat = float(coords[i][1])
    path = {
        "scale": 0,
        "nodes": nodes,
        "type": "ll"
    }
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
        "direction": calculate_direction(coords, anchor)
    }


def get_msg_id(anchor):
    '''Generates a MsgId object, with roadSignID

    Parameters:
        anchor (dict): A coordinate representing the anchor point to display the message at

    Returns:
        MsgId (dict): A MsgId object'''

    return {
        "roadSignID": {
            # if speed limit or road signage, then "regulatory" else "warning"
            "mutcdCode": "warning",
            "viewAngle": "1111111111111111",  # default view angle
            "position": {
                "latitude": anchor["latitude"],
                "longitude": anchor["longitude"]
            }
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
        "url": "null"
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
        "url": "null"
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
    if (datetime.utcnow() - datetime.strptime(feature["properties"]["start_date"], "%Y-%m-%dT%H:%M:%SZ")).total_seconds() >= 0:
        return (datetime.utcnow()).isoformat()[:-3] + "Z"
    else:
        return feature["properties"]["start_date"]


def get_data_frames(feature):
    coords = copy.deepcopy(feature["geometry"]["coordinates"])
    anchor = get_anchor(feature)
    if anchor is None:
        return None
    start_date = get_start_date(feature)
    duration = get_duration_time_minutes(feature)
    msgId = get_msg_id(anchor)

    # In here need to calculate if size of path is greater than 63
    # then generate regions accordingly
    maxLength = 62
    msgLength = len(feature['geometry']['coordinates'])
    regions = []
    if (msgLength > maxLength):
        numPaths = math.ceil(msgLength / maxLength)
        pathLength = (int) (msgLength / numPaths)
        remainder = msgLength % pathLength

        for index in range(0, numPaths):
            rangeEnd = pathLength + 1 if index < remainder else pathLength
            regionCoords = coords[0 : rangeEnd]
            anchor = get_anchor(feature)
            regions.append(get_region(regionCoords, anchor, roadName=get_first_road_name(feature)))
            del coords[0 : rangeEnd]
    else: 
        regions = [get_region(
            coords, anchor, roadName=get_first_road_name(feature))]

    data_frames = [get_work_zone_data_frame(
        start_date, duration, msgId, regions)]

    # TODO: add additional data frames as appropriate
    vehicle_Impact = feature["properties"]["vehicle_impact"]
    if vehicle_impact_supported(vehicle_Impact):
        vehicle_impact_dataFrame = get_vehicle_impact_data_frame(
            feature, start_date, duration, msgId, regions)
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
        "dataframes": data_frames
    }
    return tim_body
