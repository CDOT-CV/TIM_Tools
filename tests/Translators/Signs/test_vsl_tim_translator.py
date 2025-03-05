from unittest.mock import patch
import Translators.Signs.vsl_tim_translator as vsl_tim_translator
from Translators.Shared.itis_codes import ItisCodes

def test_calculate_direction_increasing():
    assert vsl_tim_translator.calculate_direction("east") == "I"
    assert vsl_tim_translator.calculate_direction("north") == "I"
    

def test_calculate_direction_decreasing():
    assert vsl_tim_translator.calculate_direction("west") == "D"
    assert vsl_tim_translator.calculate_direction("south") == "D"

@patch('Translators.Signs.vsl_tim_translator.active_tim', return_value=False)
def test_translate_feature(mock_active_tim):
    vsl_geojson = {
        "features": [
            {
                "geometry": {
                    "coordinates": [[1, 2]]
                },
                "properties": {
                    "id": "test_id",
                    "additionalImpacts": ["Impacts Both Directions"],
                    "routeName": "test_route",
                    "direction": "east",
                    "speed": 65,
                    "communicationStatus": "operational",
                    "displayStatus": "on"
                }
            }
        ]
    }
    expected_output = {
        "timVslList": [
            {
                "clientId": "test-id",
                "deviceId": "test-id",
                "direction": "I",
                "route": "test-route",
                "roadCode": "test-id",
                "itisCodes":[ItisCodes.SPEED_LIMIT.value],
                "geometry": [{
                    "latitude": 2,
                    "longitude": 1
                }],
                "advisory": [],
                "speed": 65,
                "buffers": [1]
            }
        ]
    }

    assert vsl_tim_translator.translate(vsl_geojson) == expected_output

@patch('Translators.Signs.vsl_tim_translator.query_db', return_value=[])
def test_translate_no_feature(mock_query_db):
    vsl_geojson = {
        "features": [
            {
                "geometry": {
                    "coordinates": [1, 2]
                },
                "properties": {
                    "id": "test_id",
                    "type": "Road Work",
                    "additionalImpacts": ["Impacts Both Directions"],
                    "routeName": "test_route",
                    "direction": "north",
                    "speed": 65,
                    "communicationStatus": "non-operational",
                }
            }
        ]
    }
    expected_output = {
        "timVslList": []
    }
    assert vsl_tim_translator.translate(vsl_geojson) == expected_output