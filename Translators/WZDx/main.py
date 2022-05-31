import sys
import functions_framework
import json
import secrets
from datetime import datetime


def getBoundingBox(geometry):
    # TODO: calculate bounding box and return
    nwCorner = {"latitude": -90, "longitude": 180}
    seCorner = {"latitude": 90, "longitude": -180}
    # loop through coordinates and calculate max corners
    # coordinates are stored longitude, latitude
    for coords in geometry.get("coordinates"):
        if coords[0] < nwCorner.get("longitude"):
            nwCorner["longitude"] = coords[0]
        if coords[1] > nwCorner.get("latitude"):
            nwCorner["latitude"] = coords[1]
        if coords[0] > seCorner.get("longitude"):
            seCorner["longitude"] = coords[0]
        if coords[1] < seCorner.get("latitude"):
            seCorner["latitude"] = coords[1]
    return nwCorner, seCorner


def getSdwRequest(geometry):
    nwCorner, seCorner = getBoundingBox(geometry)
    sdx_req = {
        "sdw": {
            "ttl": "oneday",
            "recordId": secrets.token_hex(4).upper(),
            "serviceRegion": {
                "nwCorner": {
                    "latitude": nwCorner.get("latitude"),
                    "longitude": nwCorner.get("longitude")
                },
                "seCorner": {
                    "latitude": seCorner.get("latitude"),
                    "longitude": seCorner.get("longitude")
                }
            }
        }
    }
    return sdx_req


def getRsusForMessage():
    return [
        {
            "latitude": 40.0000000,
            "longitude": -106.0000000,
            "rsuId": 1,
            "route": "Route",
            "milepost": 100,
            "rsuTarget": "10.10.10.10",
            "rsuRetries": 3,
            "rsuTimeout": 5000,
            "rsuIndex": 2
        }
    ]


def getDefaultSnmpSettings(feature):
    return {
        "rsuid": "83",
        "msgid": 31,
        "mode": 1,
        "channel": 178,
        "interval": 2,
        "deliverystart": feature.get("properties").get("start_date"),
        "deliverystop": feature.get("properties").get("end_date"),
        "enable": 1,
        "status": 4
    }


def getRsuRequest(feature):
    tim_req = {
        "rsus": getRsusForMessage(),
        "snmp": getDefaultSnmpSettings(feature)
    }
    return tim_req

def getDurationTimeMinutes(feature):
    # "start_date": "2022-02-13T16:00:00Z",
    # "end_date": "2022-02-13T16:55:00Z",
    start_date = datetime.strptime(feature.get("properties").get("start_date"), "%Y-%m-%dT%H:%M:%SZ")
    end_date = datetime.strptime(feature.get("properties").get("end_date"), "%Y-%m-%dT%H:%M:%SZ")
    duration = (end_date - start_date).seconds / 60
    return int(duration) if duration < 32000 else 32000


def generateTim(feature):
    tim_body = {
        "msgCnt": "1",
        "timeStamp": "2020-04-30T14:24:11.581Z",# TODO: determine timestamp
        "packetID": secrets.token_hex(9).upper(),#"67AEF692F8BB63067D",
        "urlB": "null",
        "dataframes": [
            {
                "startDateTime": feature.get("properties").get("start_date"),
                "durationTime": getDurationTimeMinutes(feature),
                "sspTimRights": "1",
                "frameType": "advisory",
                "msgId": {
                    "roadSignID": {
                        "mutcdCode": "warning",
                        "viewAngle": "1111111111111111",
                        "position": {
                            "latitude": 40.60476,
                            "longitude": -105.00139
                        }
                    }
                },
                "priority": "5",
                "sspLocationRights": "1",
                "regions": [
                    {
                        "name": "I_I 25_SAT-1CEE1793",
                        "anchorPosition": {
                            "latitude": 40.60476,
                            "longitude": -105.00139
                        },
                        "laneWidth": "327",
                        "directionality": "3",
                        "closedPath": "false",
                        "description": "path",
                        "path": {
                            "nodes": [
                                {
                                    "nodeLong": "-105.00128",
                                    "nodeLat": "40.61901",
                                    "delta": "node-LatLon"
                                },
                                {
                                    "nodeLong": "-105.00097",
                                    "nodeLat": "40.63349",
                                    "delta": "node-LatLon"
                                },
                                {
                                    "nodeLong": "-105.00086",
                                    "nodeLat": "40.64806",
                                    "delta": "node-LatLon"
                                },
                                {
                                    "nodeLong": "-105.00092",
                                    "nodeLat": "40.66257",
                                    "delta": "node-LatLon"
                                },
                                {
                                    "nodeLong": "-105.0008",
                                    "nodeLat": "40.67695",
                                    "delta": "node-LatLon"
                                }
                            ],
                            "type": "xy"
                        },
                        "direction": "1000000000000001"
                    }
                ],
                "sspMsgTypes": "1",
                "sspMsgContent": "1",
                "content": "advisory",
                "items": [
                    "5127"
                ],
                "url": "null"
            }
        ]
    }
    return tim_body


def translate(wzdx_geojson):
    tims = []
    # TODO: generate two messages, one for sdx and one for rsu
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
