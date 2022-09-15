import secrets

def getBoundingBox(geometry):
    '''Calculates bounding box by iterating over the provided coordinates and finding the extreme values

    Parameters:
        geometry (dict): A GeoJSON geometry object

    Returns:
        nwCorner (dict), seCorner (dict): bounding box composed of the NW and SE corners of the geometry'''

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
    '''Creates an SDW request object for the provided geometry

    Parameters:
        geometry (dict): A GeoJSON geometry object

    Returns:
        sdwRequest (dict): SDW request object'''
    nwCorner, seCorner = getBoundingBox(geometry)
    sdwRequest = {
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
    return sdwRequest

def getRsusForMessage():
    # TODO: calculate actual RSUs along path
    # we have start/end points, get path between and all RSUs along it
    # also rsus upstream 20 miles
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


def getSnmpSettings(feature):
    '''Creates an SNMP settings object for the provided feature

    Parameters:
        feature (dict): A GeoJSON feature object

    Returns:
        snmpSettings (dict): SNMP settings object'''

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
        "snmp": getSnmpSettings(feature)
    }
    return tim_req    