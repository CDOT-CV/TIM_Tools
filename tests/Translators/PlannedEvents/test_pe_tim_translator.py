from unittest.mock import patch

import pytest

import Translators.PlannedEvents.pe_tim_translator as pe_tim_translator
from Translators.Shared.itis_codes import ItisCodes


@pytest.mark.parametrize("coordinates, expected_direction", [
    ([(0, 0), (1, 0)], "I"),
    ([(1, 0), (0, 0)], "D"),
    ([(0, 0), (0, 1)], "I"),
    ([(0, 1), (0, 0)], "D")
])
def test_calculate_direction(coordinates, expected_direction):
    direction = pe_tim_translator.calculate_direction(coordinates)
    assert direction == expected_direction


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

@pytest.mark.parametrize("additional_impacts, result", [
    (["Impacts Both Directions"], True),
    (["Impacts one direction"], False),
    (["impacts Both Directions"], True),
    ([], False)
])
def test_is_both_directions(additional_impacts, result):
    assert pe_tim_translator.is_both_directions(additional_impacts) == result
