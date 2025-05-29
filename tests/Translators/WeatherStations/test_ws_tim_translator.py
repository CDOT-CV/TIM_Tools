from unittest.mock import patch
import Translators.WeatherStations.ws_tim_translator as ws_tim_translator

def test_calculate_direction_increasing():
    assert ws_tim_translator.calculate_direction("e") == "I"

def test_calculate_direction_decreasing():
    assert ws_tim_translator.calculate_direction("s") == "D"

@patch('Translators.WeatherStations.ws_tim_translator.active_tim', return_value=False)
def test_translate(mock_active_tim):
    ws_geojson = {
        "features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [1.0, 0.0]
                },
                "properties": {
                    "id": "test_id",
                    "routeName": "test_route",
                    "type": "Closed for the Season",
                    "direction": "S",
                    "sensors": [
                        {
                            "type": "Road Surface Status",
                            "currentReading": "0"
                        },
                        {
                            "type": "Gust Wind Speed",
                            "currentReading": "0"
                        },
                        {
                            "type": "Average Wind Speed",
                            "currentReading": "0"
                        }
                    ]
                }
            }
        ]
    }
    expected_output = {
        "timRcList": [
            {
                "clientId": "test-id",
                "direction": "D",
                "route": "test-route",
                "roadCode": "test-id",
                "itisCodes":[],
                "geometry": [{
                    "latitude": 0.0,
                    "longitude": 1.0
                }],
                "advisory": []
            }
        ]
    }
    assert ws_tim_translator.translate(ws_geojson) == expected_output