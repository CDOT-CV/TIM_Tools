from unittest.mock import MagicMock, patch, Mock
from Translators.WZDx import utils
import tests.Translators.WZDx.data.utils_data as utils_data

############################ get_direction_from_bearing ############################


def test_get_direction_from_bearing_1():
    for bearing, direction in utils_data.expected_direction_bearing:
        assert utils.get_direction_from_bearing(bearing) == direction

############################ calculate_direction ############################


def test_calculate_direction_y():
    coords = utils_data.coords_y_change
    anchor = utils_data.anchor
    assert utils.calculate_direction(
        coords, anchor) == utils_data.expected_direction_y


def test_calculate_direction_x():
    coords = utils_data.coords_x_change
    anchor = utils_data.anchor
    assert utils.calculate_direction(
        coords, anchor) == utils_data.expected_direction_x

def test_calculate_direction_all():
    coords = utils_data.coords_all
    anchor = utils_data.anchor
    assert utils.calculate_direction(
        coords, anchor) == utils_data.expected_direction_all