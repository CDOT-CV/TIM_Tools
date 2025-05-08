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
            },
            {
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
        ]
    }

@patch('Translators.Incident.incident_tim_translator.active_tim')
@patch('Translators.Incident.incident_tim_translator.calculate_direction')
def test_translate(mock_calculate_direction, mock_active_tim, feature_geojson):
    mock_calculate_direction.return_value = "N"
    mock_active_tim.return_value = False

    result = tim_translator.translate(feature_geojson)

    assert len(result["timIncidentList"]) == 2
    assert result["timIncidentList"][0]["clientId"] == "incident-1"
    assert result["timIncidentList"][0]["startPoint"] == {"latitude": 0.0, "longitude": 100.0, "valid": True}
    assert result["timIncidentList"][0]["endPoint"] == {"latitude": 0.0, "longitude": 100.0, "valid": True}
    assert result["timIncidentList"][0]["direction"] == "I"
    assert result["timIncidentList"][1]["clientId"] == "incident-2"
    assert result["timIncidentList"][1]["startPoint"] == {"latitude": 0.0, "longitude": 100.0, "valid": True}
    assert result["timIncidentList"][1]["endPoint"] == {"latitude": 1.0, "longitude": 101.0, "valid": True}
    assert result["timIncidentList"][1]["direction"] == "N"