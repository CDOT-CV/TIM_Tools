from Translators.RoadConditions import tim_generator, itis_codes
from Translators.RoadConditions.tim_translator import RCFeature

############################ getItisCodes ############################
def test_get_itis_codes_no_conditions():
    properties = {
        'currentConditions': [],
        'nameId': "I-80",
        'routeSegmentIndex': 1,
        "routeName": "I-80"
    }
    geometry = {
        'coordinates': [[-122.403, 37.795], [-122.403, 37.800]]
    }
    feature = RCFeature(properties, geometry)
    itisCodes = tim_generator.get_itis_codes(feature)
    assert itisCodes == []

def test_get_itis_codes_single_condition():
    properties = {
        'currentConditions': [
            {'conditionDescription': 'accident on right portion of road'}
        ],
        'nameId': "I-80",
        'routeSegmentIndex': 1,
        "routeName": "I-80"
    }
    geometry = {
        'coordinates': [[-122.403, 37.795], [-122.403, 37.800]]
    }
    feature = RCFeature(properties, geometry)
    itisCodes = tim_generator.get_itis_codes(feature)
    assert itisCodes == [itis_codes.ItisCodes.ACCIDENT.value]

def test_get_itis_codes_multiple_conditions():
    properties = {
        'currentConditions': [
            {'conditionDescription': 'Width limit in effect, accident on right portion of road. Keep to right.'}
        ],
        'nameId': "I-80",
        'routeSegmentIndex': 1,
        "routeName": "I-80"
    }
    geometry = {
        'coordinates': [[-122.403, 37.795], [-122.403, 37.800]]
    }
    feature = RCFeature(properties, geometry)

    itisCodes = tim_generator.get_itis_codes(feature)
    for code in itisCodes:
        assert code in [ 
            itis_codes.ItisCodes.ACCIDENT.value, 
            itis_codes.ItisCodes.WIDTH_LIMIT.value, 
            itis_codes.ItisCodes.KEEP_TO_RIGHT.value
            ]

def test_get_itis_codes_forecast_text_included():
    properties = {
        'currentConditions': [
            {'conditionDescription': 'forecast text included, accident on right portion of road'}
        ],
        'nameId': "I-80",
        'routeSegmentIndex': 1,
        "routeName": "I-80"
    }
    geometry = {
        'coordinates': [[-122.403, 37.795], [-122.403, 37.800]]
    }
    feature = RCFeature(properties, geometry)
    itisCodes = tim_generator.get_itis_codes(feature)
    assert itisCodes == [itis_codes.ItisCodes.ACCIDENT.value]

############################ getGeometry ############################
def test_get_geometry_empty():
    geometry = []
    annotated_geometry = tim_generator.get_geometry(geometry)
    assert annotated_geometry == []

def test_get_geometry_single_coordinate():
    geometry = [[-122.403, 37.795]]
    annotated_geometry = tim_generator.get_geometry(geometry)
    assert annotated_geometry == [{'latitude': 37.795, 'longitude': -122.403}]

def test_get_geometry_multiple_coordinates():
    geometry = [[-122.403, 37.795], [-122.403, 37.800]]
    annotated_geometry = tim_generator.get_geometry(geometry)
    assert annotated_geometry == [{'latitude': 37.795, 'longitude': -122.403}, {'latitude': 37.800, 'longitude': -122.403}]
