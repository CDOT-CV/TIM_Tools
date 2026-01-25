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

@pytest.fixture
def minimal_feature():
    return {
        "properties": {
            "id": "min_1",
            "routeName": "US-6",
            "type": "other",
            "laneImpacts": [],
            "additionalImpacts": None,
            "travelerInformationMessage": "",
        },
        "geometry": {
            "type": "Point",
            "coordinates": [0.0, 0.0]
        }
    }

@pytest.fixture
def multipoint_feature():
    return {
        "properties": {
            "id": "incident_3",
            "routeName": "route_3",
            "type": "accident",
            "laneImpacts": [],
            "additionalImpacts": [],
            "travelerInformationMessage": "",
        },
        "geometry": {
            "type": "MultiPoint",
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

@patch('Translators.Incident.incident_tim_translator.active_tim')
@patch('Translators.Incident.incident_tim_translator.calculate_direction')
def test_translate_already_active_should_not_generate(mock_calculate_direction, mock_active_tim, point_feature):
    # Arrange
    mock_active_tim.return_value = True

    # Act
    result = tim_translator.translate(wrap_feature(point_feature))

    # Assert
    assert len(result["timIncidentList"]) == 0

@patch('Translators.Incident.incident_tim_translator.active_tim')
def test_translate_minimal_properties(mock_active_tim, minimal_feature):
    # Arrange
    mock_active_tim.return_value = False

    # Act
    result = tim_translator.translate(wrap_feature(minimal_feature))

    # Assert
    assert len(result["timIncidentList"]) == 1
    tim = result["timIncidentList"][0]
    assert tim["clientId"] == "min-1"
    assert tim["incidentId"] == "min-1"
    assert tim["route"] == "US-6"
    assert tim["highway"] == "US-6"
    assert tim["effect"] == ""
    assert tim["action"] == ""
    assert tim["itisCodes"] == []

@patch('Translators.Incident.incident_tim_translator.active_tim')
@patch('Translators.Incident.incident_tim_translator.calculate_direction')
def test_translate_unknown_geometry_type(mock_calculate_direction, mock_active_tim, multipoint_feature):
    # Arrange
    mock_active_tim.return_value = False
    mock_calculate_direction.return_value = "unknown"

    # Act
    result = tim_translator.translate(wrap_feature(multipoint_feature))

    # Assert
    assert len(result["timIncidentList"]) == 1
    tim = result["timIncidentList"][0]
    assert tim["startPoint"] == {"latitude": 0.0, "longitude": 100.0, "valid": True}
    assert tim["endPoint"] == {"latitude": 1.0, "longitude": 101.0, "valid": True}
    assert tim["direction"] == "unknown"