import pytest
from unittest.mock import patch, MagicMock
import Translators.Shared.active_tim as active_tim

@pytest.fixture
def sample_geojson():
    return {
        "features": [
            {
                "properties": {
                    "id": "incident_1",
                    "routeName": "route_1",
                    "type": "accident",
                    "laneImpacts": ["lane1"],
                    "additionalImpacts": ["impact1"]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [100.0, 0.0]
                }
            },
            {
                "properties": {
                    "id": "incident_2",
                    "routeName": "route_2",
                    "type": "construction",
                    "laneImpacts": ["lane2"],
                    "additionalImpacts": None
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[100.0, 0.0], [101.0, 1.0]]
                }
            }
        ]
    }


@patch('Translators.Shared.active_tim.query_db')
def test_active_tim_active(mock_query_db):
    tim_body = {
        "clientId": "incident-1",
        "direction": "N",
        "geometry": [
            {"latitude": 0.0, "longitude": 100.0},
            {"latitude": 1.0, "longitude": 101.0}
        ]
    }

    mock_query_db.return_value = [{
        "direction": "N",
        "start_latitude": 0.0,
        "start_longitude": 100.0,
        "end_latitude": 1.0,
        "end_longitude": 101.0
    }]

    result = active_tim.active_tim('rc', tim_body)
    assert result is True

@patch('Translators.Shared.active_tim.query_db')
def test_active_tim_inactive(mock_query_db):
    tim_body = {
        "clientId": "incident-2",
        "direction": "N",
        "geometry": [
            {"latitude": 0.0, "longitude": 100.0},
            {"latitude": 1.0, "longitude": 101.0}
        ]
    }

    mock_query_db.return_value = [{
        "direction": "N",
        "start_latitude": 0.0,
        "start_longitude": 102.0,
        "end_latitude": 1.0,
        "end_longitude": 104.0
    }]

    result = active_tim.active_tim('rc', tim_body)
    assert result is False