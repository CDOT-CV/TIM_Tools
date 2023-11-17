import unittest
from unittest.mock import patch, Mock
import Translators.WZDx.snmp_operations as snmp_operations


@patch('snmp_operations.subprocess.run')
def test_clear_index_1218(mock_run):
    rsu = {
        "rsuIndex": "1",
        "snmpProtocol": "NTCIP1218",
        "rsuUsername": "username",
        "rsuPassword": "password",
        "rsuTarget": "target"
    }
    mock_run.return_value = Mock(stdout=b'output\n', stderr=b'', returncode=0)

    snmp_operations.clear_index(rsu)

    mock_run.assert_called_once()
    mock_run.assert_called_with("snmpset -v 3 -u username -a SHA -A password -x AES -X password -l authpriv target 1.3.6.1.4.1.1206.4.2.18.3.2.1.9.1 i 6", shell=True, capture_output=True, check=True)

@patch('snmp_operations.subprocess.run')
def test_clear_index_FOURDOT1(mock_run):
    rsu = {
        "rsuIndex": "1",
        "snmpProtocol": "FOURDOT1",
        "rsuUsername": "username",
        "rsuPassword": "password",
        "rsuTarget": "target"
    }
    mock_run.return_value = Mock(stdout=b'output\n', stderr=b'', returncode=0)

    snmp_operations.clear_index(rsu)

    mock_run.assert_called_once()
    mock_run.assert_called_with("snmpset -v 3 -u username -a SHA -A password -x AES -X password -l authpriv target 1.0.15628.4.1.4.1.11.1 i 6", shell=True, capture_output=True, check=True)