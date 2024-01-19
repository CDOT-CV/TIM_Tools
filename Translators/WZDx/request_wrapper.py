import secrets
from shapely.geometry import LineString
import rsu_service
import geospatial_service
from pgquery import query_db
import re
import os


def get_bounding_box(geometry):
    '''Calculates bounding box by iterating over the provided coordinates and finding the extreme values

    Parameters:
        geometry (dict): A GeoJSON geometry object

    Returns:
        nwCorner (dict), seCorner (dict): bounding box composed of the NW and SE corners of the geometry'''

    nwCorner = {"latitude": -90, "longitude": 180}
    seCorner = {"latitude": 90, "longitude": -180}
    # loop through coordinates and calculate max corners
    # coordinates are stored longitude, latitude
    for coords in geometry["coordinates"]:
        if coords[0] < nwCorner["longitude"]:
            nwCorner["longitude"] = coords[0]
        if coords[1] > nwCorner["latitude"]:
            nwCorner["latitude"] = coords[1]
        if coords[0] > seCorner["longitude"]:
            seCorner["longitude"] = coords[0]
        if coords[1] < seCorner["latitude"]:
            seCorner["latitude"] = coords[1]
    return nwCorner, seCorner


def get_sdw_request(geometry):
    '''Creates an SDW request object for the provided geometry

    Parameters:
        geometry (dict): A GeoJSON geometry object

    Returns:
        sdwRequest (dict): SDW request object'''
    nwCorner, seCorner = get_bounding_box(geometry)
    sdwRequest = {
        "sdw": {
            "ttl": "oneday",
            "recordId": secrets.token_hex(4).upper(),
            "serviceRegion": {
                "nwCorner": {
                    "latitude": nwCorner["latitude"],
                    "longitude": nwCorner["longitude"]
                },
                "seCorner": {
                    "latitude": seCorner["latitude"],
                    "longitude": seCorner["longitude"]
                }
            }
        }
    }
    return sdwRequest

# takes in a linestring and buffers by 0.0001 degrees


def buffer_geometry(coords):
    '''Creates a buffer around the provided geometry

    Parameters:
        coords (list): A list of coordinates

    Returns:
        bufferedPolygon (dict): A GeoJSON polygon object'''
    line_string = LineString(coords)

    # 1 degree is approximately 69 miles at 38 degrees North
    buffer_distance = os.getenv("BUFFER_DISTANCE_MILES", 1) / 69
    return line_string.buffer(buffer_distance)


def get_rsus_for_message(geometry):
    # create buffer around geometry so we get a "fat" line
    bufferedPolygon = buffer_geometry(geometry["coordinates"])
    rsus = rsu_service.get_rsus_intersecting_geometry(bufferedPolygon)
    return rsus


def get_snmp_settings(feature):
    '''Creates an SNMP settings object for the provided feature

    Parameters:
        feature (dict): A GeoJSON feature object

    Returns:
        snmpSettings (dict): SNMP settings object'''

    return {
        "rsuid": "83",
        "msgid": 31,
        "mode": 1,
        "channel": 183,
        "interval": 1000,
        "deliverystart": feature["properties"]["start_date"],
        "deliverystop": feature["properties"]["end_date"],
        "enable": 1,
        "status": 4
    }

def get_snmp_info(rsuTarget):
    query = f"SELECT nickname, username, password FROM snmp_credentials WHERE snmp_credential_id = (SELECT snmp_credential_id FROM rsus WHERE ipv4_address = '{rsuTarget}')"
    return query_db(query)

def get_rsu_request(feature):
    rsus = get_rsus_for_message(feature['geometry'])
    if rsus is None:
        return None
    
    # remove any region 1 RSUs from the list for the time being
    rsus = [rsu for rsu in rsus if re.match(r"^10\.11\.81", rsu["rsuTarget"]) == None]
    
    for rsu in rsus:
    # get snmp protocol, username, password for each rsu
        snmp_info = get_snmp_info(rsu["rsuTarget"])
        if snmp_info is not None:
            rsu["snmpProtocol"] = "NTCIP1218" if snmp_info[0]["nickname"] == "Yunex BUILD" else "FOURDOT1"
            rsu["rsuUsername"] = snmp_info[0]["username"]
            rsu["rsuPassword"] = snmp_info[0]["password"]

    if rsus != []:
        tim_req = {
            "rsus": rsus,
            "snmp": get_snmp_settings(feature)
        }
        return tim_req
    else:
        return None
