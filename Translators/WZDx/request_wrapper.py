import secrets
from shapely.geometry import LineString
import rsu_service
import geospatial_service


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
    line_string = LineString(coords)
    # ~ 10m buffer. 0.0001 degrees = 11.1m at equator
    return line_string.buffer(0.0001)


def get_rsus_for_message(geometry):
    route_id = geospatial_service.point_to_route_id(
        geometry["coordinates"][0][0], geometry["coordinates"][0][1])
    measures = geospatial_service.get_upstream_measures(geometry["coordinates"], route_id, 20)
    extendedGeometry = geospatial_service.get_route_between_measures(
        route_id, measures["upstream_measure"], measures["first_point_measure"])
    extendedGeometry.extend(geometry["coordinates"])

    # create buffer around geometry so we get a "fat" line
    bufferedPolygon = buffer_geometry(extendedGeometry)
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
        "channel": 178,
        "interval": 2,
        "deliverystart": feature["properties"]["start_date"],
        "deliverystop": feature["properties"]["end_date"],
        "enable": 1,
        "status": 4
    }


def get_rsu_request(feature):
    rsus = get_rsus_for_message(feature['geometry'])
    if rsus is None:
        return None

    tim_req = {
        "rsus": rsus,
        "snmp": get_snmp_settings(feature)
    }
    return tim_req
