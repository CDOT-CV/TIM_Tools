import os
import requests

def getGeospatialEndpoint(): 
    return os.environ['dual_carriageway_endpoint']

def measureAtPoint(lat, lon, route) -> int:
    '''Finds the measure at a given point for a given route

    Parameters:
        lat (float): Latitude of point
        lon (float): Longitude of point
        route (str): Name of route

    Returns:
        measure (int): Measure of point on route'''
    r = requests.get(
        f'{getGeospatialEndpoint()}/MeasureAtPoint?x={lon}&y={lat}&inSR=4326&routeId={route}&tolerance=&outSR=4326&f=pjson', verify=False)
    data = r.json()
    return int(data["features"][0]["attributes"]["Measure"])


def pointAtMeasure(measure, route):
    '''Finds the coordinate at a given measure for a given route

    Parameters:
        measure (int): Measure to translate to point 
        route (str): Name of route

    Returns:
        point (dict): Coordinate of point on route'''
    r = requests.get(
        f'{getGeospatialEndpoint()}/PointAtMeasure?routeId={route}&measure={measure}&inSR=4326&outSR=4326&f=pjson', verify=False)
    data = r.json()
    return{
        "longitude": data['features'][0]['geometry']['x'],
        "latitude": data['features'][0]['geometry']['y']
    }


def getUpstreamAnchor(coords, route):
    '''Finds the upstream anchor point for a given route and coordinate list

    Parameters:
        coords (list): A list of coordinates
        route (str): A route ID

    Returns:
        anchor (dict): A coordinate object representing the anchor point, or upstream point from beginning coordinate'''
    # get measure at point for first coord & 2nd coord to determine measure direction
    # then go opposite direction and use point at measure

    if len(coords) == 1:
        return None

    start_measure = measureAtPoint(coords[0][1], coords[0][0], route)
    end_measure = measureAtPoint(coords[1][1], coords[1][0], route)

    new_measure = start_measure - \
        0.25 if end_measure > start_measure else start_measure + 0.25
    anchor = pointAtMeasure(new_measure, route)
    return anchor
