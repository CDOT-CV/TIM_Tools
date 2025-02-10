import pytest
from unittest.mock import patch
import Translators.Incident.incident_tim_translator as tim_translator

@pytest.fixture
def feature_geojson():
    return {
        "features": [
            {
                "properties": {
                    "id": "incident_1",
                    "routeName": "route_1",
                    "type": "accident",
                    "laneImpacts": ["lane1"],
                    "additionalImpacts": ["impact1"],
                    "travelerInformationMessage": "",
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
                    "additionalImpacts": None,
                    "travelerInformationMessage": "",
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[100.0, 0.0], [101.0, 1.0]]
                }
            }
        ]
    }

@patch('Translators.Incident.incident_tim_translator.query_db')
@patch('Translators.Incident.incident_tim_translator.get_action')
@patch('Translators.Incident.incident_tim_translator.get_effect')
@patch('Translators.Incident.incident_tim_translator.get_point')
@patch('Translators.Incident.incident_tim_translator.get_itis_codes')
@patch('Translators.Incident.incident_tim_translator.calculate_direction')
def test_translate(mock_calculate_direction, mock_get_itis_codes, mock_get_point, mock_get_effect, mock_get_action, mock_query_db, feature_geojson):
    mock_get_point.side_effect = lambda x: {"latitude": x[1], "longitude": x[0]}
    mock_get_effect.return_value = "effect"
    mock_get_action.return_value = "action"
    mock_get_itis_codes.return_value = ["itis_code"]
    mock_calculate_direction.return_value = "N"
    mock_query_db.return_value = []

    result = tim_translator.translate(feature_geojson)

    assert len(result["timIncidentList"]) == 2
    assert result["timIncidentList"][0]["clientId"] == "incident-1"
    assert result["timIncidentList"][0]["startPoint"] == {"latitude": 0.0, "longitude": 100.0}
    assert result["timIncidentList"][0]["endPoint"] == {"latitude": 0.0, "longitude": 100.0}
    assert result["timIncidentList"][0]["direction"] == "I"
    assert result["timIncidentList"][1]["clientId"] == "incident-2"
    assert result["timIncidentList"][1]["startPoint"] == {"latitude": 0.0, "longitude": 100.0}
    assert result["timIncidentList"][1]["endPoint"] == {"latitude": 1.0, "longitude": 101.0}
    assert result["timIncidentList"][1]["direction"] == "N"

@patch('Translators.Incident.incident_tim_translator.query_db')
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

    result = tim_translator.active_tim(tim_body)
    assert result is True