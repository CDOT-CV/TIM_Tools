from unittest.mock import patch
import Translators.PlannedEvents.pe_tim_translator as pe_tim_translator
from Translators.Shared.itis_codes import ItisCodes

def test_calculate_direction_eastbound():
    coordinates = [(0, 0), (1, 0)]
    assert pe_tim_translator.calculate_direction(coordinates) == "I"

def test_calculate_direction_westbound():
    coordinates = [(1, 0), (0, 0)]
    assert pe_tim_translator.calculate_direction(coordinates) == "D"

def test_calculate_direction_northbound():
    coordinates = [(0, 0), (0, 1)]
    assert pe_tim_translator.calculate_direction(coordinates) == "I"

def test_calculate_direction_southbound():
    coordinates = [(0, 1), (0, 0)]
    assert pe_tim_translator.calculate_direction(coordinates) == "D"

@patch('Translators.PlannedEvents.pe_tim_translator.active_tim', return_value=False)
def test_translate_no_result(mock_active_tim):
    pe_geojson = {
        "features": [
            {
                "geometry": {
                    "coordinates": [(0, 0), (1, 0), (2, 0)]
                },
                "properties": {
                    "id": "test_id",
                    "type": "Road Work",
                    "additionalImpacts": ["Impacts Both Directions"],
                    "routeName": "test_route",
                }
            }
        ]
    }
    expected_output = {
        "timRcList": []
    }
    assert pe_tim_translator.translate(pe_geojson) == expected_output


@patch('Translators.PlannedEvents.pe_tim_translator.active_tim', return_value=False)
def test_translate_result(mock_active_tim):
    pe_geojson = {
        "features": [
            {
                "geometry": {
                    "coordinates": [(0, 0), (1, 0), (2, 0)]
                },
                "properties": {
                    "id": "test_id",
                    "additionalImpacts": ["Impacts Both Directions"],
                    "routeName": "test_route",
                    "type": "Closed for the Season"
                }
            }
        ]
    }
    expected_output = {
        "timRcList": [
            {
                "clientId": "test-id",
                "direction": "B",
                "route": "test-route",
                "roadCode": "test-id",
                "itisCodes":[ItisCodes.CLOSED_FOR_SEASON.value],
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
                "advisory": []
            }
        ]
    }
    assert pe_tim_translator.translate(pe_geojson) == expected_output

def test_is_both_directions_true():
    additional_impacts = ["Impacts both directions"]
    assert pe_tim_translator.is_both_directions(additional_impacts) == True

def test_is_both_directions_false():
    additional_impacts = ["Impacts one direction"]
    assert pe_tim_translator.is_both_directions(additional_impacts) == False

def test_is_both_directions_mixed_case():
    additional_impacts = ["impacts Both Directions"]
    assert pe_tim_translator.is_both_directions(additional_impacts) == True

def test_is_both_directions_empty_list():
    additional_impacts = []
    assert pe_tim_translator.is_both_directions(additional_impacts) == False
