from unittest.mock import patch
import Translators.RoadConditions.rc_tim_translator as tim_translator

def test_calculate_direction_eastbound():
    coordinates = [(0, 0), (1, 0)]
    assert tim_translator.calculate_direction(coordinates) == "I"

def test_calculate_direction_westbound():
    coordinates = [(1, 0), (0, 0)]
    assert tim_translator.calculate_direction(coordinates) == "D"

def test_calculate_direction_northbound():
    coordinates = [(0, 0), (0, 1)]
    assert tim_translator.calculate_direction(coordinates) == "I"

def test_calculate_direction_southbound():
    coordinates = [(0, 1), (0, 0)]
    assert tim_translator.calculate_direction(coordinates) == "D"

@patch('Translators.RoadConditions.rc_tim_translator.get_itis_codes', return_value=[1, 2, 3])
@patch('Translators.RoadConditions.rc_tim_translator.query_db', return_value=[])
def test_translate(mock_query_db, mock_get_itis_codes):
    rc_geojson = {
        "features": [
            {
                "geometry": {
                    "coordinates": [(0, 0), (1, 0), (2, 0)]
                },
                "properties": {
                    "nameId": "test_name",
                    "routeSegmentIndex": 1,
                    "routeName": "test_route",
                    "currentConditions": []
                }
            }
        ]
    }
    expected_output = {
        "timRcList": [
            {
                "clientId": "test-name",
                "direction": "I",
                "segment": 1,
                "route": "test-route",
                "roadCode": "test-name",
                "itisCodes":[1, 2, 3],
                "geometry": [{
                    "latitude": 0,
                    "longitude": 0
                }, {
                    "latitude": 0,
                    "longitude": 1
                }, {
                    "latitude": 0,
                    "longitude": 2
                }],
                "advisory": ["3"]
            }
        ]
    }
    assert tim_translator.translate(rc_geojson) == expected_output