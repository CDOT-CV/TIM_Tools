import pytest
from Translators.Incident import incident_tim_generator as tim_generator
from Translators.Incident.incident_tim_translator import IncidentFeature
import Translators.Shared.itis_codes as itis_codes

@pytest.fixture
def sample_incident_feature():
    def _create_feature(traveler_info="", problem="Incident", lane_impacts=None, additional_impacts=None):
        properties = {
            "travelerInformationMessage": traveler_info,
            "id": "1",
            "routeName": "I-70",
            "type": problem,
            "laneImpacts": lane_impacts or [],
            "additionalImpacts": additional_impacts or []
        }
        geometry = {
            "coordinates": [-122.403, 37.795],
            "type": "Point"
        }
        return IncidentFeature(properties, geometry)
    return _create_feature

############################ get_itis_codes ############################

@pytest.mark.parametrize("tim_body, expected_codes", [
    (
        {"effect": "Speeds reduced due to construction", "action": "Reduce speed.", "problem": ""},
        [itis_codes.ItisCodes.REDUCE_YOUR_SPEED.value]
    ),
    (
        {"effect": "Chains required due to snow", "action": "", "problem": ""},
        [itis_codes.ItisCodes.SNOW_TIRES_OR_CHAINS_REQUIRED.value]
    ),
    (
        {"effect": "", "action": "", "problem": "Maintenance operations ongoing"},
        [itis_codes.ItisCodes.LOOK_OUT_FOR_WORKERS.value]
    ),
    (
        {"effect": "", "action": "Reduce speeds. Chains required.", "problem": "Maintenance Operations"},
        [
            itis_codes.ItisCodes.REDUCE_YOUR_SPEED.value,
            itis_codes.ItisCodes.SNOW_TIRES_OR_CHAINS_REQUIRED.value,
            itis_codes.ItisCodes.LOOK_OUT_FOR_WORKERS.value
        ]
    ),
    (
        {"effect": "Normal traffic", "action": "None", "problem": ""},
        []
    ),
])
def test_get_itis_codes(tim_body, expected_codes):
    itisCodes = tim_generator.get_itis_codes(tim_body)
    assert itisCodes == expected_codes

############################ get_point ############################
def test_get_point():
    coordinates = [-122.403, 37.795]
    point = tim_generator.get_point(coordinates)
    assert point == {"latitude": 37.795, "longitude": -122.403, "valid": True}

############################ get_effect ############################

@pytest.mark.parametrize("impacts, addtl_effects, expected_effect", [
    (
        [{"laneClosures": "1", "closedLaneTypes": ["left lane"], "direction": "north"}],
        ["Accident"],
        "Accident. northbound left lane closed."
    ),
    (
        [
            {"laneClosures": "1", "closedLaneTypes": ["left lane"], "direction": "north"},
            {"laneClosures": "1", "closedLaneTypes": ["right lane"], "direction": "south"}
        ],
        ["Construction"],
        "Construction. northbound left lane closed. southbound right lane closed."
    ),
    (
        [{"laneClosures": "0", "closedLaneTypes": ["left lane"], "direction": "north"}],
        ["Maintenance"],
        "Maintenance."
    ),
    (
        [],
        ["Hazard"],
        "Hazard."
    ),
    (
        [{"laneClosures": "1", "closedLaneTypes": ["left lane", "center lane"], "direction": "north"}],
        [],
        "northbound left lane closed. northbound center lane closed."
    ),
])
def test_get_effect(impacts, addtl_effects, expected_effect):
    effect = tim_generator.get_effect(impacts, addtl_effects)
    assert effect == expected_effect

############################ get_action ############################

@pytest.mark.parametrize("tim_body, traveler_info, problem, expected_action", [
    (
        {"effect": "Speeds reduced", "action": "", "problem": ""},
        "Speeds reduced",
        "Incident",
        "Reduce Speeds."
    ),
    (
        {"effect": "", "action": "", "problem": "Traction Law Code 15"},
        "",
        "Incident",
        "Chains Required."
    ),
    (
        {"effect": "", "action": "", "problem": "Chain Law Code 18"},
        "",
        "Incident",
        "Chains Required."
    ),
    (
        {"effect": "", "action": "", "problem": ""},
        "Slower speeds are advised",
        "Incident",
        "Reduce Speeds."
    ),
    (
        {"effect": "Speeds reduced", "action": "", "problem": "Traction Law Code 15"},
        "Slower speeds are advised",
        "Incident",
        "Reduce Speeds.Chains Required."
    ),
])
def test_get_action(sample_incident_feature, tim_body, traveler_info, problem, expected_action):
    feature = sample_incident_feature(traveler_info=traveler_info, problem=problem)
    action = tim_generator.get_action(tim_body, feature)
    assert action == expected_action

############################ calculate_direction ############################

@pytest.mark.parametrize("coordinates, expected_direction", [
    ([[-122.403, 37.795], [-122.400, 37.795]], "I"),
    ([[-122.400, 37.795], [-122.403, 37.795]], "D"),
    ([[-122.403, 37.795], [-122.403, 37.800]], "I"),
    ([[-122.403, 37.800], [-122.403, 37.795]], "D"),
    ([[-122.403, 37.795]], "unknown"),
    ([[-122.403, 37.795], [-122.403, 37.795]], "unknown"),
])
def test_calculate_direction(coordinates, expected_direction):
    direction = tim_generator.calculate_direction(coordinates)
    assert direction == expected_direction