import logging
import os
import requests
import urllib3
urllib3.disable_warnings()
from Schemas import geospatial_schemas as geospatial_schemas
import redis
import json

cache = None

def initialize_redis_connection():
    global cache
    if cache is None:
        cache = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], decode_responses=True, db=0, password=os.environ['REDIS_PASS'])

def check_cache(key):
    global cache
    if cache is None:
        initialize_redis_connection()
    return cache.get(key)

def get_geospatial_endpoint():
    return os.environ['dual_carriageway_endpoint']


def get_map_server_endpoint():
    return os.environ['dual_carriageway_endpoint'].split('/exts', 1)[0]


def measure_at_point(lat, lon, routeId) -> int:
    '''Finds the measure at a given point for a given route

    Parameters:
        lat (float): Latitude of point
        lon (float): Longitude of point
        route (str): Name of route

    Returns:
        measure (int): Measure of point on route'''
    global cache
    key = f'measure_at_point:{lat}:{lon}:{routeId}'

    cache_val = check_cache(key)
    if cache_val != None:
        return int(cache_val)
    else:
        r = requests.get(
            f'{get_geospatial_endpoint()}/MeasureAtPoint?x={lon}&y={lat}&inSR=4326&routeId={routeId}&tolerance=&outSR=4326&f=pjson', verify=False)
        if (r.status_code != 200):
            logging.warning(r.text)
            return -1

        data = r.json()
        schema = geospatial_schemas.MeasureAtPointReturnSchema()
        errors = schema.validate(data)
        if errors:
            logging.warning(str(errors))
            return -1
        
        cache.set(key, str(int(data["features"][0]["attributes"]["Measure"])))

        return int(data["features"][0]["attributes"]["Measure"])


def point_at_measure(measure, routeId):
    '''Finds the coordinate at a given measure for a given route

    Parameters:
        measure (int): Measure to translate to point 
        route (str): Name of route

    Returns:
        point (dict): Coordinate of point on route'''
    global cache
    key = f'point_at_measure:{measure}:{routeId}'

    cache_val = check_cache(key)
    if cache_val != None:
        return json.loads(cache_val)
    else:
        r = requests.get(
            f'{get_geospatial_endpoint()}/PointAtMeasure?routeId={routeId}&measure={measure}&inSR=4326&outSR=4326&f=pjson', verify=False)
        data = r.json()
        if 'error' in data:
            logging.info(data)
            return None
        res = {
            "longitude": data['features'][0]['geometry']['x'],
            "latitude": data['features'][0]['geometry']['y']
        }
        cache.set(key, json.dumps(res))
        return res


def get_ten_meter_extent(lon, lat):
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


def point_to_route_id(lon, lat):
    '''Finds the route ID for a given coordinate

    Parameters:
        lat (float): Latitude of point
        lon (float): Longitude of point

    Returns:
        route (str): Route ID'''
    # colorado_extent = "-109.081667,37.002220,-102.028444,40.979583"
    # NOTE: currently failing to find proper routes on occasion...
    global cache
    key = f'point_to_route_id:{lon}:{lat}'
    cache_val = check_cache(key)
    if cache_val != None:
        return cache_val
    else:
        r = requests.get(
            f'{get_map_server_endpoint()}/identify?geometry={lon},{lat}&geometryType=esriGeometryPoint&sr=4326&tolerance=50&mapExtent={get_ten_meter_extent(lon,lat)}&imageDisplay=600,550,96&returnGeometry=false&returnZ=false&returnM=false&returnUnformattedValues=false&returnFieldName=false&f=json', verify=False)
        data = r.json()
        if (len(data['results']) > 1):
            str_results = [*map(lambda x: x['attributes']
                                ['RouteId_Legacy'], data['results'])]
            logging.info('Multiple routes found: ' + ', '.join(str_results))
        if data["results"] == []:
            return None
        cache.set(key, data["results"][0]["attributes"]["RouteId_Legacy"])
        return data["results"][0]["attributes"]["RouteId_Legacy"]


def get_direction_of_travel(coords, routeId):
    '''Finds the direction of travel for a given route and coordinate list

    Parameters:
        coords (list): A list of coordinates
        route (str): A route ID

    Returns:
        direction (str): A string representing the direction of travel'''
    # get measure at point for first coord & 2nd coord to determine measure direction

    if len(coords) == 1:
        return None

    start_measure = measure_at_point(coords[0][1], coords[0][0], routeId)
    end_index = len(coords) - 1
    end_measure = measure_at_point(
        coords[end_index][1], coords[end_index][0], routeId)

    return {
        'start_measure': start_measure,
        'direction': 'increasing' if end_measure > start_measure else 'decreasing'
    }


def get_upstream_measures(coords, routeId, distance):
    '''Finds the first point measure and upstream measure for a given route and coordinate list

    Parameters:
        coords (list): A list of coordinates
        route (str): A route ID

    Returns:
        measures (dict): An object representing measures for first point and upstream point from beginning coordinate'''
    # get measure at point for first coord & 2nd coord to determine measure direction
    # then go opposite direction and use point at measure

    travel = get_direction_of_travel(coords, routeId)
    if travel is None:
        return None

    new_measure = travel['start_measure'] - \
        distance if travel['direction'] == 'increasing' else travel['start_measure'] + distance
    return {
        'first_point_measure': travel['start_measure'],
        'upstream_measure': new_measure
    }


def get_upstream_point(coords, routeId, distance):
    '''Finds the upstream anchor point for a given route and coordinate list

    Parameters:
        coords (list): A list of coordinates
        route (str): A route ID

    Returns:
        anchor (dict): A coordinate object representing the anchor point, or upstream point from beginning coordinate'''
    # get measure at point for first coord & 2nd coord to determine measure direction
    # then go opposite direction and use point at measure

    travel = get_direction_of_travel(coords, routeId)
    if travel is None:
        return None

    new_measure = travel['start_measure'] - \
        distance if travel['direction'] == 'increasing' else travel['start_measure'] + distance
    anchor = point_at_measure(new_measure, routeId)
    return anchor


def get_route_between_measures(routeId, startMeasure, endMeasure):
    '''Finds the lat/lon points between two measures for a given route

    Parameters:
        routeId (str): A route ID
        startMeasure (int): The starting measure
        endMeasure (int): The ending measure

    Returns:
        route (list): A list of coordinates representing the route'''
    r = requests.get(
        f'{get_geospatial_endpoint()}/RouteBetweenMeasures?routeId={routeId}&fromMeasure={startMeasure}&toMeasure={endMeasure}&inSR=4326&outSR=4326&f=pjson', verify=False)
    data = r.json()

    linestring = []
    for feature in data.get('features', []):
        for path in feature.get('geometry', {}).get('paths', []):
            linestring.extend(path)
    return linestring
