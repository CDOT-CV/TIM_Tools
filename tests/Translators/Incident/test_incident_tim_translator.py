import pytest
from unittest.mock import patch
import Translators.Incident.incident_tim_translator as tim_translator

@pytest.fixture
def point_feature():
    return {
        "properties": {
            "id": "incident_1",
            "routeName": "route_1",
            "type": "accident",
            "laneImpacts": [
                {
                    "direction": "north",
                    "laneCount": 1,
                    "laneClosures": "0",
                    "closedLaneTypes": []
                }
            ],
            "additionalImpacts": ["impact1"],
            "travelerInformationMessage": "",
        },
        "geometry": {
            "type": "Point",
            "coordinates": [100.0, 0.0]
        }
    }

@pytest.fixture
def linestring_feature():
    return {
        "properties": {
            "id": "incident_2",
            "routeName": "route_2",
            "type": "construction",
            "laneImpacts": [],
            "additionalImpacts": None,
            "travelerInformationMessage": "",
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [[100.0, 0.0], [101.0, 1.0]]
        }
    }

def wrap_feature(feature):
    return {"features": [feature]}

@patch('Translators.Incident.incident_tim_translator.active_tim')
@patch('Translators.Incident.incident_tim_translator.calculate_direction')
def test_translate_point(mock_calculate_direction, mock_active_tim, point_feature):
    # Arrange
    mock_active_tim.return_value = False
    
    # Act
    result = tim_translator.translate(wrap_feature(point_feature))

    # Assert
    assert len(result["timIncidentList"]) == 1
    tim = result["timIncidentList"][0]
    assert tim["clientId"] == "incident-1"
    assert tim["incidentId"] == "incident-1"
    assert tim["route"] == "route-1"
    assert tim["highway"] == "route-1"
    assert tim["startPoint"] == {"latitude": 0.0, "longitude": 100.0, "valid": True}
    assert tim["endPoint"] == {"latitude": 0.0, "longitude": 100.0, "valid": True}
    assert tim["direction"] == "I"
    assert tim["problem"] == "accident"
    assert tim["effect"] == "impact1."
    assert tim["action"] == ""
    assert tim["itisCodes"] == []

@patch('Translators.Incident.incident_tim_translator.active_tim')
@patch('Translators.Incident.incident_tim_translator.calculate_direction')
def test_translate_linestring(mock_calculate_direction, mock_active_tim, linestring_feature):
    # Arrange
    mock_calculate_direction.return_value = "N"
    mock_active_tim.return_value = False
    
    # Act
    result = tim_translator.translate(wrap_feature(linestring_feature))

    # Assert
    assert len(result["timIncidentList"]) == 1
    tim = result["timIncidentList"][0]
    assert tim["clientId"] == "incident-2"
    assert tim["startPoint"] == {"latitude": 0.0, "longitude": 100.0, "valid": True}
    assert tim["endPoint"] == {"latitude": 1.0, "longitude": 101.0, "valid": True}
    assert tim["direction"] == "N"
    mock_calculate_direction.assert_called_once_with([[100.0, 0.0], [101.0, 1.0]])

def test_translate_empty_features():
    # Act
    result = tim_translator.translate({"features": []})

    # Assert
    assert result == {"timIncidentList": []}