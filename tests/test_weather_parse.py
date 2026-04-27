import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from extract.weather_to_snowflake import parse_record

MOCK_API_RESPONSE = {
    "location": {
        "name": "New York",
        "region": "New York",
        "country": "United States of America",
        "lat": 40.71,
        "lon": -74.01,
        "localtime": "2026-04-26 10:00",
    },
    "current": {
        "temp_c": 15.0,
        "temp_f": 59.0,
        "condition": {"text": "Partly cloudy"},
        "wind_mph": 10.0,
        "wind_kph": 16.1,
        "humidity": 60,
        "feelslike_c": 14.0,
        "feelslike_f": 57.2,
        "uv": 4.0,
    },
}


def test_parse_record_extracts_location_fields():
    rec = parse_record(MOCK_API_RESPONSE)
    assert rec["location_name"] == "New York"
    assert rec["country"] == "United States of America"
    assert rec["lat"] == 40.71
    assert rec["lon"] == -74.01


def test_parse_record_extracts_weather_fields():
    rec = parse_record(MOCK_API_RESPONSE)
    assert rec["temp_c"] == 15.0
    assert rec["temp_f"] == 59.0
    assert rec["humidity"] == 60
    assert rec["condition_text"] == "Partly cloudy"
    assert rec["uv"] == 4.0


def test_parse_record_includes_extracted_at():
    rec = parse_record(MOCK_API_RESPONSE)
    assert "extracted_at" in rec
    assert rec["extracted_at"] is not None
