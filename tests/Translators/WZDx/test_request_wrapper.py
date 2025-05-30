from datetime import datetime
from unittest.mock import patch
from Translators.WZDx import request_wrapper
import tests.Translators.WZDx.data.request_wrapper_data as data

############################ get_bounding_box ############################


def test_get_bounding_box_empty_geometry():
    geometry = {"coordinates": []}
    assert request_wrapper.get_bounding_box(geometry) == (
        {"latitude": -90, "longitude": 180}, {"latitude": 90, "longitude": -180})


def test_get_bounding_box():
    geometry = {"coordinates": [[-100, 40], [-100, 50], [-90, 50], [-90, 40]]}
    assert request_wrapper.get_bounding_box(geometry) == (
        {"latitude": 50, "longitude": -100}, {"latitude": 40, "longitude": -90})


############################ get_sdw_request ############################
@patch('Translators.WZDx.request_wrapper.secrets')
def test_get_sdw_request_empty_geometry(mock_secrets):
    mock_secrets.token_hex.return_value = '12345678'
    geometry = {"coordinates": []}
    assert request_wrapper.get_sdw_request(geometry) == {
        "sdw": {
            "ttl": "oneday",
            "recordId": "12345678",
            "serviceRegion": {
                "nwCorner": {
                    "latitude": -90,
                    "longitude": 180
                },
                "seCorner": {
                    "latitude": 90,
                    "longitude": -180
                }
            }
        }
    }

############################ buffer_geometry ############################


def test_buffer_geometry_empty_coords():
    coords = []
    assert str(request_wrapper.buffer_geometry(coords)) == 'POLYGON EMPTY'


def test_buffer_geometry():
    coords = [[-100, 40], [-100, 50], [-90, 50], [-90, 40]]
    assert str(request_wrapper.buffer_geometry(coords)
               ) == data.expected_buffer_geometry_result


############################ get_rsus_for_message ############################
@patch('Translators.WZDx.request_wrapper.geospatial_service')
@patch('Translators.WZDx.request_wrapper.rsu_service')
def test_get_rsus_for_message_none_found(mock_rsu_service, mock_geospatial_service):
    mock_geospatial_service.point_to_route_id.return_value = '12345678'
    mock_geospatial_service.get_upstream_measures.return_value = {
        'first_point_measure': 15,
        'upstream_measure': 5
    }
    mock_geospatial_service.get_route_between_measures.return_value = []
    mock_rsu_service.get_rsus_intersecting_geometry.return_value = []
    geometry = {"coordinates": [[-100, 40], [-100, 50], [-90, 50], [-90, 40]]}
    assert request_wrapper.get_rsus_for_message(geometry) == []


@patch('Translators.WZDx.request_wrapper.geospatial_service')
@patch('Translators.WZDx.request_wrapper.rsu_service')
def test_get_rsus_for_message_found_rsus(mock_rsu_service, mock_geospatial_service):
    mock_geospatial_service.point_to_route_id.return_value = '12345678'
    mock_geospatial_service.get_upstream_measures.return_value = {
        'first_point_measure': 15,
        'upstream_measure': 5
    }
    mock_geospatial_service.get_route_between_measures.return_value = []
    mock_rsu_service.get_rsus_intersecting_geometry.return_value = data.rsu_intersect_result
    geometry = {"coordinates": [[-100, 40], [-100, 50], [-90, 50], [-90, 40]]}
    assert request_wrapper.get_rsus_for_message(geometry) == data.rsu_intersect_result

############################ get_snmp_settings ############################
@patch('Translators.WZDx.request_wrapper.datetime')
def test_get_snmp_settings(mock_datetime):
    mock_datetime.utcnow.return_value = datetime(2022, 11, 11, 14, 0, 0)
    assert request_wrapper.get_snmp_settings(data.example_feature) == data.expected_snmp_settings


############################ get_rsu_request ############################
@patch('Translators.WZDx.request_wrapper.get_rsus_for_message')
@patch('Translators.WZDx.request_wrapper.get_snmp_info')
@patch('Translators.WZDx.request_wrapper.check_rsu_online', return_value=False)
def test_get_rsu_request_no_rsus(mock_check_online, mock_get_snmp_info, mock_get_rsus_for_message):
    mock_get_snmp_info.return_value = None
    mock_get_rsus_for_message.return_value = None
    assert request_wrapper.get_rsu_request(data.example_feature) == None

@patch('Translators.WZDx.request_wrapper.get_rsus_for_message')
@patch('Translators.WZDx.request_wrapper.get_snmp_settings')
@patch('Translators.WZDx.request_wrapper.get_snmp_info')
@patch('Translators.WZDx.request_wrapper.get_snmp_protocol')
@patch('Translators.WZDx.request_wrapper.clear_index')
@patch('Translators.WZDx.request_wrapper.check_rsu_online', return_value=True)
def test_get_rsu_request_rsus(mock_check_online, mock_clear_index, mock_get_snmp_protocol, mock_get_snmp_info, mock_get_snmp_settings, mock_get_rsus_for_message):
    mock_clear_index.return_value = True
    mock_get_rsus_for_message.return_value = data.rsu_intersect_result
    mock_get_snmp_settings.return_value = data.expected_snmp_settings
    mock_get_snmp_info.return_value = data.expected_snmp_info
    mock_get_snmp_protocol.return_value = data.expected_snmp_protocol
    assert request_wrapper.get_rsu_request(data.example_feature) == data.expected_rsu_request

############################ check_rsu_online ############################
@patch('Translators.WZDx.request_wrapper.query_db')
def test_check_rsu_online_rsu_offline(mock_pgquery):
    mock_pgquery.return_value = data.check_rsu_online_no_result
    rsu = {'rsuId': 1}
    assert request_wrapper.check_rsu_online(rsu) == False

@patch('Translators.WZDx.request_wrapper.query_db')
def test_check_rsu_online_rsu_online(mock_pgquery):
    mock_pgquery.return_value = data.check_rsu_online_result
    rsu = {'rsuId': 1}
    assert request_wrapper.check_rsu_online(rsu) == True