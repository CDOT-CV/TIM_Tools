from Translators.Shared import itis_codes
from Translators.PlannedEvents import pe_tim_generator

############################ getItisCodes ############################
def test_get_itis_codes():
    itisCodes = pe_tim_generator.get_itis_codes()
    assert itisCodes == [itis_codes.ItisCodes.CLOSED_FOR_SEASON.value]


############################ getGeometry ############################

def test_get_geometry_empty():
    geometry = []
    annotated_geometry = pe_tim_generator.get_geometry(geometry)
    assert annotated_geometry == []

def test_get_geometry_single_coordinate():
    geometry = [[-122.403, 37.795]]
    annotated_geometry = pe_tim_generator.get_geometry(geometry)
    assert annotated_geometry == [{'latitude': 37.795, 'longitude': -122.403}]

def test_get_geometry_multiple_coordinates():
    geometry = [[-122.403, 37.795], [-122.403, 37.800]]
    annotated_geometry = pe_tim_generator.get_geometry(geometry)
    assert annotated_geometry == [{'latitude': 37.795, 'longitude': -122.403}, {'latitude': 37.800, 'longitude': -122.403}]
