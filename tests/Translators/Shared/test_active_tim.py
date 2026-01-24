import pytest
from unittest.mock import patch, MagicMock
import Translators.Shared.active_tim as active_tim

@pytest.fixture
def tim_body():
    return {
        "clientId": "incident_1",
        "direction": "N",
        "geometry": [
            {"latitude": 0.0, "longitude": 100.0},
            {"latitude": 1.0, "longitude": 101.0}
        ]
    }


@pytest.fixture
def mock_db_record():
    return {
        "direction": "N",
        "start_latitude": 0.0,
        "start_longitude": 100.0,
        "end_latitude": 1.0,
        "end_longitude": 101.0
    }


@patch('Translators.Shared.active_tim.query_db')
def test_active_tim_found_in_holding_with_geometry_mismatch(mock_query_db, tim_body):
    tim_body["clientId"] = "incident-2"

    mock_query_db.return_value = [{
        "direction": "N",
        "start_latitude": 0.0,
        "start_longitude": 102.0,
        "end_latitude": 1.0,
        "end_longitude": 104.0
    }]

    result = active_tim.active_tim('rc', tim_body)
    assert result is False

@patch('Translators.Shared.active_tim.query_db')
def test_active_tim_not_found_in_db(mock_query_db, tim_body):
    tim_body["clientId"] = "incident_not_found"

    # Both queries return empty
    mock_query_db.return_value = []

    result = active_tim.active_tim('rc', tim_body)
    assert result is False

@patch('Translators.Shared.active_tim.query_db')
def test_active_tim_found_in_holding(mock_query_db, tim_body, mock_db_record):
    # Mock response for active_tim_holding query
    mock_query_db.side_effect = [
        [mock_db_record],
        []
    ]

    result = active_tim.active_tim('rc', tim_body)
    assert result is True
    assert "FROM active_tim_holding" in mock_query_db.call_args_list[0][0][0]
    assert "incident_1" in mock_query_db.call_args_list[0][0][0]

@patch('Translators.Shared.active_tim.query_db')
def test_active_tim_found_in_holding_with_direction_mismatch(mock_query_db, tim_body, mock_db_record):
    mismatched_record = mock_db_record.copy()
    mismatched_record["direction"] = "S" # Mismatch

    mock_query_db.return_value = [mismatched_record]

    result = active_tim.active_tim('rc', tim_body)
    assert result is False

@patch('Translators.Shared.active_tim.query_db')
def test_active_tim_found_in_active_tim(mock_query_db, tim_body, mock_db_record):
    # Mock response for active_tim query (first query returns empty, second returns record)
    mock_query_db.side_effect = [
        [],
        [mock_db_record]
    ]

    result = active_tim.active_tim('i', tim_body)
    assert result is True
    
    # Verify active_tim query contains the correct conditions
    active_tim_query = mock_query_db.call_args_list[1][0][0]
    assert "FROM active_tim" in active_tim_query
    assert "client_id LIKE '%incident_1%'" in active_tim_query
    assert "tim_type_id = (SELECT tim_type_id FROM tim_type WHERE type = 'I')" in active_tim_query
    assert "marked_for_deletion = false" in active_tim_query