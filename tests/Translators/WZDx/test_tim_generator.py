from unittest.mock import MagicMock, patch, Mock
from Translators.WZDx import tim_generator

def test_getDurationTimeMinutes():
    feature = {
        "properties": {
            "start_date": "2022-02-13T16:00:00Z",
            "end_date": "2022-02-13T16:55:00Z"
        }
    }
    duration = tim_generator.getDurationTimeMinutes(feature)
    assert duration == 55

def test_getDurationTimeMinutes_withLargeTime():
    feature = {
        "properties": {
            "start_date": "2022-02-13T16:00:00Z",
            "end_date": "2022-07-13T16:55:00Z"
        }
    }
    duration = tim_generator.getDurationTimeMinutes(feature)
    assert duration == 32000