import functions_framework
import json
import secrets
from datetime import datetime
from Translators.WZDx.geospatial_service import getUpstreamAnchor
from Translators.WZDx.request_wrapper import getRsuRequest, getSdwRequest
from Translators.WZDx.utils import calculateDirection, translateRoute

def getDurationTimeMinutes(feature):
    '''Get duration in minutes from a GeoJSON feature object with start_date and end_date properties

    Parameters:
        feature (dict): A GeoJSON feature object. Assumed to have properties 'start_date' and 'end_date'

    Returns:
        duration (int): Duration in minutes. Note 32000 represents infinity'''
    # "start_date": "2022-02-13T16:00:00Z",
    # "end_date": "2022-02-13T16:55:00Z",
    start_date = datetime.strptime(feature.get(
        "properties").get("start_date"), "%Y-%m-%dT%H:%M:%SZ")
    end_date = datetime.strptime(feature.get(
        "properties").get("end_date"), "%Y-%m-%dT%H:%M:%SZ")
    duration = (end_date - start_date).seconds / 60
    return int(duration) if duration < 32000 else 32000


def getAnchor(feature):
    # TODO: calculate anchor from geospatial function call
    # take start point, and go upstream
    coords = feature.get("geometry").get("coordinates")
    route = translateRoute(feature.get("properties").get("core_details").get("road_names"))
    return getUpstreamAnchor(coords, route)


def getItisCodes(feature):
    # TODO: calculate itis codes
    return [
        "1025"  # Road Construction
    ]


def calculateOffsetPath(coords, anchor):
    '''Creates an offset path from passed in coordinates and anchor point
    
    Parameters:
        coords (list): A list of coordinates
        anchor (dict): A coordinate representing the anchor point, or initial point to begin from
        
    Returns:
        offsetPath (dict): A path object with offset ll nodes'''
    # loop through coords and calculate offset path
    startLat = float(anchor.get("latitude"))
    startLon = float(anchor.get("longitude"))
    nodes = []
    coords_len = len(coords)
    if(coords_len == 1):
        # Per J2735, NodeSetLL's must contain at least 2 nodes. ODE will fail to
        # PER-encode TIM if we supply less than 2. If we only have 1 node for the path,
        # include a node with an offset of (0, 0) which is effectively a point that's
        # right on top of the anchor point.
        nodes.append({
            "nodeLat": 0,
            "nodeLon": 0,
            "delta": "node-LL"
        })

    for i in range(coords_len):
        latOffset = float(coords[i][1]) - startLat
        lonOffset = float(coords[i][0]) - startLon
        nodes.append({
            "nodeLat": latOffset,
            "nodeLon": lonOffset,
            "delta": "node-LL"
        })
        startLon = float(coords[i][0])
        startLat = float(coords[i][1])
    path = {
        "scale": 0,
        "nodes": nodes,
        "type": "ll"
    }
    return path


def getRegion(coords, anchor):
    # TODO: update fields, name, directionality
    return {
        "name": "I_I 25_SAT-1CEE1793",
        "anchorPosition": anchor,
        "laneWidth": "50",  # defaulting lane width to 50
        "directionality": "3",  # 0 - unavailable, 1 - forward, 2 - backward, 3 - both
        "closedPath": "false",  # default
        "description": "path",  # default
        "path": calculateOffsetPath(coords, anchor),
        "direction": calculateDirection(coords, anchor)
    }


def getMsgId(anchor):
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
                "latitude": anchor.get("latitude"),
                "longitude": anchor.get("longitude")
            }
        }
    }


def getDataFrame(feature):
    coords = feature.get("geometry").get("coordinates")
    anchor = getAnchor(feature)
    return {
        "startDateTime": feature.get("properties").get("start_date"),
        "durationTime": getDurationTimeMinutes(feature),
        "sspTimRights": "1",  # default value
        "frameType": "advisory",  # TODO: determine frame type
        "msgId": getMsgId(anchor),
        "priority": "5",  # default value
        "sspLocationRights": "1",  # default value
        "regions": [
            getRegion(coords, anchor)
        ],
        "sspMsgTypes": "1",  # default value
        "sspMsgContent": "1",  # default value
        "content": "workzone",  # TODO: determine content, defaulting workzone for now
        "items": getItisCodes(feature),
        "url": "null"
    }


def generateTim(feature):
    tim_body = {
        "msgCnt": "1",
        "timeStamp": "2020-04-30T14:24:11.581Z",  # TODO: determine timestamp
        "packetID": secrets.token_hex(9).upper(),  # "67AEF692F8BB63067D",
        "urlB": "null",
        "dataframes": [
            getDataFrame(feature)
        ]
    }
    return tim_body


def translate(wzdx_geojson):
    tims = []
    # TODO: generate two messages, one for sdx and one for rsu
    # if no RSUs found, drop that one
    for feature in wzdx_geojson.get("features"):
        tim_body = generateTim(feature)
        sdx_tim = {
            "request": getSdwRequest(feature.get("geometry")),
            "tim": tim_body
        }
        rsu_tim = {
            "request": getRsuRequest(feature),
            "tim": tim_body
        }
        tims.append(sdx_tim)
        tims.append(rsu_tim)
    return tims


@functions_framework.http
def translateWzdxTIM(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    tims = translate(request.get_json())
    return (json.dumps(tims), 200, headers)
