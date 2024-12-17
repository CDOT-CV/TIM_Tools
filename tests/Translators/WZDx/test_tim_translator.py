import unittest
from unittest.mock import patch, MagicMock
from Translators.WZDx.tim_translator import update_sat_region_name, update_rsu_region_name, active_tim, translate_old, translate
import tests.Translators.WZDx.data.tim_translator_data as test_data

class TestTimTranslator(unittest.TestCase):

    def setUp(self):
        self.request_sdw = {
            'sdw': {
                'recordId': '12345'
            }
        }
        self.request_rsu = {
            'rsus': [{
                'rsuTarget': '67890'
            }]
        }
        self.tim_body = {
            'dataframes': [{
                'regions': [{
                    'name': 'IDENTIFIER_region'
                }]
            }]
        }
        self.feature = {
            "geometry": {
                "coordinates": [[-105.0, 40.0], [-105.1, 40.1], [-105.2, 40.2]],
            },
            "properties": {
                "core_details": {
                    "direction": "northbound",
                    "road_names": ["road_name"],
                    "name": "road_code"
                },
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-02T00:00:00Z"
            }
        }
        self.maxDiff = None

    def test_update_sat_region_name(self):
        updated_tim = update_sat_region_name(self.request_sdw, self.tim_body)
        self.assertEqual(updated_tim['dataframes'][0]['regions'][0]['name'], 'SAT_12345_region')

    def test_update_rsu_region_name(self):
        updated_tim = update_rsu_region_name(self.request_rsu, self.tim_body)
        self.assertEqual(updated_tim['dataframes'][0]['regions'][0]['name'], 'RSU_67890_region')

    @patch('Translators.WZDx.tim_translator.query_db')
    def test_active_tim(self, mock_query_db):
        mock_query_db.return_value = []
        tim_body = {
            "id": "test_id",
            "direction": "I",
            "geometry": [{"latitude": 40.0, "longitude": -105.0}, {"latitude": 40.1, "longitude": -105.1}]
        }
        result = active_tim(self.feature, tim_body)
        self.assertFalse(result)

    @patch('Translators.WZDx.tim_translator.get_bearing')
    @patch('Translators.WZDx.tim_translator.get_geometry')
    @patch('Translators.WZDx.tim_translator.get_itis_codes')
    @patch('Translators.WZDx.tim_translator.active_tim')
    def test_translate(self, mock_active_tim, mock_get_itis_codes, mock_get_geometry, mock_get_bearing):
        mock_get_bearing.return_value = 90
        mock_get_geometry.return_value = [{"latitude": 40.0, "longitude": -105.0}, {"latitude": 40.1, "longitude": -105.1}]
        mock_get_itis_codes.return_value = [1, 2, 3]
        mock_active_tim.return_value = False

        wzdx_geojson = [self.feature]
        result = translate(wzdx_geojson)
        self.assertEqual(len(result["timRwList"]), 1)
        self.assertEqual(result["timRwList"][0], test_data.expected_translate_result)

    @patch('Translators.WZDx.tim_translator.query_db')
    def test_active_tim_true(self, mock_query_db):
        mock_query_db.side_effect = [
            [{
                "direction": "I",
                "start_latitude": 40.0,
                "start_longitude": -105.0,
                "end_latitude": 40.1,
                "end_longitude": -105.1
            }],
            []
        ]
        tim_body = {
            "id": "test_id",
            "direction": "I",
            "geometry": [{"latitude": 40.0, "longitude": -105.0}, {"latitude": 40.1, "longitude": -105.1}]
        }
        result = active_tim(self.feature, tim_body)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()