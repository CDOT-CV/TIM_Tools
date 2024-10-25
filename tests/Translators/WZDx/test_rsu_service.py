from unittest.mock import patch, MagicMock
import Translators.WZDx.rsu_service as rsu_service
import tests.Translators.WZDx.data.rsu_service_data as rsu_service_data
from pytest import fixture

# This fixture is used to reset the rsu_index_dict after each test
@fixture(autouse=True)
def set_rsu_index_dict(request):
    rsu_service.rsu_index_dict = {}
    def fin():
        rsu_service.rsu_index_dict = {}
    request.addfinalizer(fin)

@patch('Translators.WZDx.rsu_service.pgquery')
def test_get_rsus_intersecting_geometry_no_data(mock_pgquery):
    mock_pgquery.query_db.return_value = {}
    expected_rsu_data = None
    expected_query = "SELECT rsu_id, primary_route, milepost, ipv4_address,  ST_AsText(geography) point FROM rsus WHERE rsu_id not in (SELECT rsu_id FROM rsu_organization as ro JOIN organizations as o on ro.organization_id = o.organization_id WHERE o.name = 'Region 1') AND ST_Intersects('TEST', geography)"
    actual_result = rsu_service.get_rsus_intersecting_geometry('TEST')
    mock_pgquery.query_db.assert_called_with(expected_query)

    assert actual_result == expected_rsu_data


@patch('Translators.WZDx.rsu_service.pgquery')
def test_get_rsus_intersecting_geometry_single_result(mock_pgquery):
    mock_pgquery.query_db.return_value = rsu_service_data.return_value_single_result
    actual_result = rsu_service.get_rsus_intersecting_geometry('TEST')
    mock_pgquery.query_db.assert_called_once()

    assert actual_result == rsu_service_data.expected_rsu_data_single_result


@patch('Translators.WZDx.rsu_service.pgquery')
def test_get_rsus_intersecting_geometry_multiple_results(mock_pgquery):
    mock_pgquery.query_db.return_value = rsu_service_data.return_value_multiple_results
    actual_result = rsu_service.get_rsus_intersecting_geometry('TEST')
    mock_pgquery.query_db.assert_called_once()

    assert actual_result == rsu_service_data.expected_rsu_data_multiple_results
