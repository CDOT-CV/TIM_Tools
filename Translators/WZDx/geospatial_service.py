import os
import requests
import urllib3
urllib3.disable_warnings()


def getGeospatialEndpoint():
    return os.environ['dual_carriageway_endpoint']


def getMapServerEndpoint():
    return os.environ['dual_carriageway_endpoint'].split('/exts', 1)[0]


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
    if 'error' in data:
        print(data)
        return None
    return {
        "longitude": data['features'][0]['geometry']['x'],
        "latitude": data['features'][0]['geometry']['y']
    }


def getTenMeterExtent(lon, lat):
    '''Finds the extent approximately 10 meter each direction around a given coordinate

    Parameters:
        lat (float): Latitude of point
        lon (float): Longitude of point

    Returns:
        extent (str): A string representing the extent of the 10 meter square'''
    maxLon = lon + 0.0001
    minLon = lon - 0.0001
    maxLat = lat + 0.0001
    minLat = lat - 0.0001
    return f'{minLon},{minLat},{maxLon},{maxLat}'


def pointToRouteId(lon, lat):
    '''Finds the route ID for a given coordinate

    Parameters:
        lat (float): Latitude of point
        lon (float): Longitude of point

    Returns:
        route (str): Route ID'''
    # colorado_extent = "-109.081667,37.002220,-102.028444,40.979583"
    # NOTE: currently failing to find proper routes on occasion...
    r = requests.get(
        f'{getMapServerEndpoint()}/identify?geometry={lon},{lat}&geometryType=esriGeometryPoint&sr=4326&tolerance=50&mapExtent={getTenMeterExtent(lon,lat)}&imageDisplay=600,550,96&returnGeometry=false&returnZ=false&returnM=false&returnUnformattedValues=false&returnFieldName=false&f=json', verify=False)
    data = r.json()
    if (len(data['results']) > 1):
        str_results = [*map(lambda x: x['attributes']['RouteId_Legacy'], data['results'])]
        print('Multiple routes found: ' + ', '.join(str_results))
    return data["results"][0]["attributes"]["RouteId_Legacy"]


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
