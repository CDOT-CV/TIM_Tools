from unittest.mock import patch
from Translators.WZDx import tim_generator
import tests.Translators.WZDx.data.dataframes_data as dataframes_data


############################ getDurationTimeMinutes ############################
def test_getDurationTimeMinutes():
    feature = {
        'properties': {
            'start_date': '2022-02-13T16:00:00Z',
            'end_date': '2022-02-13T16:55:00Z'
        }
    }
    duration = tim_generator.get_duration_time_minutes(feature)
    assert duration == 55

def test_getDurationTimeMinutes_withLargeTime():
    feature = {
        'properties': {
            'start_date': '2022-02-13T16:00:00Z',
            'end_date': '2022-07-13T16:55:00Z'
        }
    }
    duration = tim_generator.get_duration_time_minutes(feature)
    assert duration == 32000

############################ getAnchor ############################    
@patch('Translators.WZDx.tim_generator.geospatial_service')
def test_getAnchor(mock_geospacial_service):
    mock_geospacial_service.point_to_route_id.return_value = 'route'
    mock_geospacial_service.get_upstream_point.return_value = {'latitude': 37.795, 'longitude': -122.403}
    feature = {
        'geometry': {
            'coordinates': [
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
        'properties': {
            'core_details': {
                'road_names': [
                    'I-80'
                ]
            }
        }
    }
    anchor = tim_generator.get_anchor(feature)
    assert anchor == {
        'latitude': 37.795,
        'longitude': -122.403
    }

############################ getItisCodes ############################
def test_getItisCodes_allLanesClosed():
    feature = {
        'properties': {
            'vehicle_impact': 'all-lanes-closed'
        }
    }
    itisCodes = tim_generator.get_itis_codes(feature)
    assert itisCodes == ['770']  # ItisCodes.CLOSED.value

############################ calculateOffsetPath ############################
def test_calculateOffsetPath():
    coords = [
        [
            -122.401,
            37.750
        ],
        [
            -122.403,
            37.795
        ]
    ]
    anchor = {
        'latitude': 37.700,
        'longitude': -122.400
    }
    offsetPath = tim_generator.calculate_offset_path(coords, anchor)
    assert offsetPath ==  {
        'scale': 0,
        'nodes': [
                {
                    'delta': 'node-LL',
                    'nodeLat': 0.04999999999999716,
                    'nodeLong': -0.000999999999990564
                },
                {
                    'delta': 'node-LL',
                    'nodeLat': 0.045000000000001705,
                    'nodeLong': -0.0020000000000095497
                }
            ],
        'type': 'll'
    }

############################ getDataFrames ############################

# create a pytest for the get_data_frames function
@patch('Translators.WZDx.tim_generator.get_anchor')
@patch('Translators.WZDx.tim_generator.copy.deepcopy')
@patch('Translators.WZDx.tim_generator.get_duration_time_minutes')
@patch('Translators.WZDx.tim_generator.get_msg_id')
@patch('Translators.WZDx.tim_generator.vehicle_impact_supported')
@patch('Translators.WZDx.tim_generator.get_first_road_name')
@patch('Translators.WZDx.tim_generator.get_start_date')
def test_getDataFrames(mockStart, mockRoad, mockSupported, mockMsgId, mockDuration, mockDeepCopy, mockAnchor):

    mockStart.return_value = "2022-02-13T16:00:00Z"
    mockDeepCopy.return_value = dataframes_data.coords
    mockAnchor.return_value = dataframes_data.anchor
    mockDuration.return_value = 0
    mockMsgId.return_value = "some-id"
    mockSupported.return_value = False
    mockRoad.return_value = "some-road"

    feature = {
        'geometry': {
            'coordinates': dataframes_data.coords
        },
        'properties': {
            'start_date': '2022-02-13T16:00:00Z',
            'vehicle_impact': "some-impact",
        }
    }

    dataFrames = tim_generator.get_data_frames(feature)
    assert dataFrames == dataframes_data.expected_dataframes

