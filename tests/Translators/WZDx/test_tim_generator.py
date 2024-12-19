from unittest.mock import patch
from Translators.WZDx import tim_generator
import tests.Translators.WZDx.data.dataframes_data as dataframes_data


############################ getAnchor ############################    
@patch('Translators.WZDx.tim_generator.geospatial_service')
def test_getAnchor(mock_geospacial_service):
    mock_geospacial_service.point_to_route_id.return_value = 'route'
    mock_geospacial_service.get_upstream_point.return_value = {'latitude': 37.795, 'longitude': -122.403}
    # get_anchor assumes that the tuples are in (long, lat) tuples as are given in the WZDx feed data
    feature = {
        'geometry': {
            'coordinates': [
                [
                    -122.403,
                    37.795
                ],
                [
                    -122.403,
                    37.800
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
        'latitude': 37.7948651018481,
        'longitude': -122.403
    }

############################ getItisCodes ############################
def test_getItisCodes_allLanesClosed():
    feature = {
        'properties': {
            'vehicle_impact': 'all-lanes-closed',
            'core_details': {
                'description': ''
            }
        }
    }
    itisCodes = tim_generator.get_itis_codes(feature)
    assert itisCodes == ['770']  # ItisCodes.CLOSED.value

def test_getItisCodes_typesOfWork():
    feature = {
        'properties': {
            'vehicle_impact': '',
            'core_details': {
                'description': 'description'
            },
            'types_of_work': [{'type_name': 'roadway-creation', 'is_architectural_change': True}]
        }
    }
    itisCodes = tim_generator.get_itis_codes(feature)
    assert itisCodes == ['1025']  # ItisCodes.ROAD_CONSTRUCTION.value

def test_getItisCodes_multipleCodes():
    feature = {
        'properties': {
            'vehicle_impact': '',
            'core_details': {
                'description': 'Width limit in effect, accident on right portion of road. Keep to right.'
            }
        }
    }
    itisCodes = tim_generator.get_itis_codes(feature)
    assert itisCodes == ['513', '2573', '7425']  # ItisCodes.WIDTH_LIMIT.value, ItisCodes.ACCIDENT.value, ItisCodes.KEEP_RIGHT.value

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
@patch('Translators.WZDx.tim_generator.get_msg_id')
@patch('Translators.WZDx.tim_generator.vehicle_impact_supported')
@patch('Translators.WZDx.tim_generator.get_first_road_name')
@patch('Translators.WZDx.tim_generator.get_start_date')
def test_getDataFrames(mockStart, mockRoad, mockSupported, mockMsgId, mockDeepCopy, mockAnchor):

    mockStart.return_value = "2022-02-13T16:00:00Z"
    mockDeepCopy.return_value = dataframes_data.coords
    mockAnchor.return_value = dataframes_data.anchor
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

def test_getDataFrames_notEnoughNodes():
    feature = {
        'geometry': {
            'coordinates': [
                [
                    -122.403,
                    37.795
                ]
            ]
        }
    }
    dataFrames = tim_generator.get_data_frames(feature)
    assert dataFrames == None


def test_getDataFrames_edgeCase_twoNode():
    """
    Test case for the `get_data_frames` function in the `tim_generator` module.

    This test checks the edge case where the feature has exactly two nodes.
    It verifies that the function returns None when given this input.

    The feature dictionary contains:
    - 'geometry': A dictionary with:
        - 'coordinates': A list of two coordinate pairs (longitude, latitude).

    The test asserts that the `get_data_frames` function returns None for this input.

    Returns:
            None
    """
    feature = {
        'geometry': {
            'coordinates': [
                [
                    -122.403,
                    37.795
                ],
                [
                    -122.403,
                    37.800
                ]
            ]
        }
    }
    dataFrames = tim_generator.get_data_frames(feature)
    assert dataFrames == None

def test_get_bearing_northbound():
    feature = {
        'properties': {
            'core_details': {
                'direction': 'northbound'
            }
        }
    }
    bearing = tim_generator.get_bearing(feature)
    assert bearing == 0

def test_get_bearing_eastbound():
    feature = {
        'properties': {
            'core_details': {
                'direction': 'eastbound'
            }
        }
    }
    bearing = tim_generator.get_bearing(feature)
    assert bearing == 270

def test_get_bearing_southbound():
    feature = {
        'properties': {
            'core_details': {
                'direction': 'southbound'
            }
        }
    }
    bearing = tim_generator.get_bearing(feature)
    assert bearing == 180

def test_get_bearing_westbound():
    feature = {
        'properties': {
            'core_details': {
                'direction': 'westbound'
            }
        }
    }
    bearing = tim_generator.get_bearing(feature)
    assert bearing == 90

def test_get_geometry():
    geometry = [
        [-122.403, 37.795],
        [-122.403, 37.800]
    ]
    annotated_geometry = tim_generator.get_geometry(geometry)
    assert annotated_geometry == [
        {"latitude": 37.795, "longitude": -122.403},
        {"latitude": 37.800, "longitude": -122.403}
    ]
