import unittest
from unittest.mock import patch, Mock
import Translators.WZDx.snmp_operations as snmp_operations

@patch('Translators.WZDx.snmp_operations.requests.delete')
def test_clear_index_1218(mock_delete):
    rsu = {
        "rsuIndex": "1",
        "snmpProtocol": "NTCIP1218",
        "rsuUsername": "username",
        "rsuPassword": "password",
        "rsuTarget": "target",
        "rsuRetries": 3,
        "rsuTimeout": 10
    }
    mock_delete.return_value.status_code = 200

    snmp_operations.clear_index(rsu)

    mock_delete.assert_called_once_with(
        'http://localhost:8080/tim',
        data='{"rsuTarget": "target", "rsuRetries": 3, "rsuTimeout": 10, "rsuIndex": "1", "snmpProtocol": "NTCIP1218", "rsuUsername": "username", "rsuPassword": "password"}',
        headers={'Content-Type': 'application/json'},
        params={'index': '1'}
    )

@patch('Translators.WZDx.snmp_operations.requests.delete')
def test_clear_index_FOURDOT1(mock_delete):
    rsu = {
        "rsuIndex": "1",
        "snmpProtocol": "FOURDOT1",
        "rsuUsername": "username",
        "rsuPassword": "password",
        "rsuTarget": "target",
        "rsuRetries": 3,
        "rsuTimeout": 10
    }
    mock_delete.return_value.status_code = 200

    res = snmp_operations.clear_index(rsu)

    mock_delete.assert_called_once_with(
        'http://localhost:8080/tim',
        data='{"rsuTarget": "target", "rsuRetries": 3, "rsuTimeout": 10, "rsuIndex": "1", "snmpProtocol": "FOURDOT1", "rsuUsername": "username", "rsuPassword": "password"}',
        headers={'Content-Type': 'application/json'},
        params={'index': '1'}
    )

