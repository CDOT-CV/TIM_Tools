from unittest.mock import MagicMock, patch, Mock
from Translators.WZDx import tim_generator


############################ getDurationTimeMinutes ############################
def test_getDurationTimeMinutes():
    feature = {
        "properties": {
            "start_date": "2022-02-13T16:00:00Z",
            "end_date": "2022-02-13T16:55:00Z"
        }
    }
    duration = tim_generator.getDurationTimeMinutes(feature)
    assert duration == 55

def test_getDurationTimeMinutes_withLargeTime():
    feature = {
        "properties": {
            "start_date": "2022-02-13T16:00:00Z",
            "end_date": "2022-07-13T16:55:00Z"
        }
    }
    duration = tim_generator.getDurationTimeMinutes(feature)
    assert duration == 32000

############################ getAnchor ############################    
@patch('Translators.WZDx.tim_generator.translateRoute')
@patch('Translators.WZDx.tim_generator.geospatial_service.getUpstreamAnchor')
def test_getAnchor(mock_upstreamAnchor, mock_translateRoute):
    mock_translateRoute.return_value = 'I-80'
    mock_upstreamAnchor.return_value = {'latitude': 37.795, 'longitude': -122.403}
    feature = {
        "geometry": {
            "coordinates": [
                [
                    -122.403,
                    37.795
                ],
                [
                    -122.403,
                    37.795
                ]
            ]
        },
        "properties": {
            "core_details": {
                "road_names": [
                    "I-80"
                ]
            }
        }
    }
    anchor = tim_generator.getAnchor(feature)
    assert anchor == {
        "latitude": 37.795,
        "longitude": -122.403
    }

############################ getItisCodes ############################
def test_getItisCodes_allLanesClosed():
    feature = {
        "properties": {
            "vehicle_impact": "all-lanes-closed"
        }
    }
    itisCodes = tim_generator.getItisCodes(feature)
    assert itisCodes == ['770']  # ItisCodes.CLOSED.value

############################ calculateOffsetPath ############################
def test_calculateOffsetPath():
    coords = [
        [
            -122.403,
            37.795
        ],
        [
            -122.403,
            37.795
        ]
    ]
    anchor = {
        "latitude": 37.795,
        "longitude": -122.403
    }
    offsetPath = tim_generator.calculateOffsetPath(coords, anchor)
    assert offsetPath == {
        "offsetLL": {
            "latOffset": 0,
            "longOffset": 0
        },
        "path": {
            "nodes": [
                {
                    "delta": 0,
                    "lat": 37.795,
                    "long": -122.403
                },
                {
                    "delta": 0,
                    "lat": 37.795,
                    "long": -122.403
                }
            ]
        }
    }    