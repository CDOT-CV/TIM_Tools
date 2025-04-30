from Translators.Incident import incident_tim_generator as tim_generator
from Translators.Incident.incident_tim_translator import IncidentFeature
import Translators.Shared.itis_codes as itis_codes

############################ get_itis_codes ############################
def test_get_itis_codes_speed_reduce():
    tim_body = {
        "effect": "Speeds reduced due to construction",
        "action": "Reduce speed.",
        "problem": ""
    }
    itisCodes = tim_generator.get_itis_codes(tim_body)
    assert itisCodes == [itis_codes.ItisCodes.REDUCE_YOUR_SPEED.value]

def test_get_itis_codes_chains_required():
    tim_body = {
        "effect": "Chains required due to snow",
        "action": "",
        "problem": ""
    }
    itisCodes = tim_generator.get_itis_codes(tim_body)
    assert itisCodes == [itis_codes.ItisCodes.SNOW_TIRES_OR_CHAINS_REQUIRED.value]

def test_get_itis_codes_maintenance():
    tim_body = {
        "effect": "",
        "action": "",
        "problem": "Maintenance operations ongoing"
    }
    itisCodes = tim_generator.get_itis_codes(tim_body)
    assert itisCodes == [itis_codes.ItisCodes.LOOK_OUT_FOR_WORKERS.value]

def test_get_itis_codes_multiple_conditions():
    tim_body = {
        "effect": "",
        "action": "Reduce speeds. Chains required.",
        "problem": "Maintenance Operations"
    }
    itisCodes = tim_generator.get_itis_codes(tim_body)
    assert itisCodes == [
        itis_codes.ItisCodes.REDUCE_YOUR_SPEED.value,
        itis_codes.ItisCodes.SNOW_TIRES_OR_CHAINS_REQUIRED.value,
        itis_codes.ItisCodes.LOOK_OUT_FOR_WORKERS.value
    ]

############################ get_point ############################
def test_get_point():
    coordinates = [-122.403, 37.795]
    point = tim_generator.get_point(coordinates)
    assert point == {"latitude": 37.795, "longitude": -122.403, "valid": True}

############################ get_effect ############################
def test_get_effect():
    impacts = [
        {"laneClosures": "1", "closedLaneTypes": ["left lane"], "direction": "north"}
    ]
    addtl_effects = ["Accident"]
    effect = tim_generator.get_effect(impacts, addtl_effects)
    assert effect == "Accident. northbound left lane closed."

############################ get_action ############################
def test_get_action_speed_reduce():
    tim_body = {
        "effect": "Speeds reduced",
        "action": "",
        "problem": ""
    }
    properties = {
        "travelerInformationMessage": "Speeds reduced",
        "id": "1",
        "routeName": "I-70",
        "type": "Incident",
        "laneImpacts": [],
        "additionalImpacts": []
    }
    geometry = {
        "coordinates": [-122.403, 37.795],
        "type": "Point"
    }
    feature = IncidentFeature(properties, geometry)
    
    {
        "properties": {
            "travelerInformationMessage": ""
        }
    }
    action = tim_generator.get_action(tim_body, feature)
    assert action == "Reduce Speeds. "

def test_get_action_chains_required():
    tim_body = {
        "effect": "",
        "action": "",
        "problem": "Traction Law Code 15"
    }
    properties = {
        "travelerInformationMessage": "",
        "id": "1",
        "routeName": "I-70",
        "type": "Incident",
        "laneImpacts": [],
        "additionalImpacts": []
    }
    geometry = {
        "coordinates": [-122.403, 37.795],
        "type": "Point"
    }
    feature = IncidentFeature(properties, geometry)
    action = tim_generator.get_action(tim_body, feature)
    assert action == "Chains Required."

############################ calculate_direction ############################
def test_calculate_direction_eastbound():
    coordinates = [[-122.403, 37.795], [-122.400, 37.795]]
    direction = tim_generator.calculate_direction(coordinates)
    assert direction == "I"

def test_calculate_direction_westbound():
    coordinates = [[-122.400, 37.795], [-122.403, 37.795]]
    direction = tim_generator.calculate_direction(coordinates)
    assert direction == "D"

def test_calculate_direction_northbound():
    coordinates = [[-122.403, 37.795], [-122.403, 37.800]]
    direction = tim_generator.calculate_direction(coordinates)
    assert direction == "I"

def test_calculate_direction_southbound():
    coordinates = [[-122.403, 37.800], [-122.403, 37.795]]
    direction = tim_generator.calculate_direction(coordinates)
    assert direction == "D"

def test_calculate_direction_unknown():
    coordinates = [[-122.403, 37.795]]
    direction = tim_generator.calculate_direction(coordinates)
    assert direction == "unknown"

def test_calculate_direction_duplicate_coordinates():
    coordinates = [[-122.403, 37.795], [-122.403, 37.795]]
    direction = tim_generator.calculate_direction(coordinates)
    assert direction == "unknown"