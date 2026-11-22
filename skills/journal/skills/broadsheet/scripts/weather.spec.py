#!/usr/bin/env python3
import contextlib
import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weather

GOOD = json.dumps({
    "daily_units": {"temperature_2m_max": "°C"},
    "daily": {
        "time": ["2026-11-21"],
        "weather_code": [61],
        "temperature_2m_max": [18.2],
        "temperature_2m_min": [9.1],
        "precipitation_probability_max": [70],
    },
})


GEO = json.dumps({"results": [{"name": "Brisbane", "latitude": -27.47, "longitude": 153.02}]})


def run(argv, fetch):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = weather.main(argv, fetch)
    return code, json.loads(out.getvalue())


def fails(url):
    raise OSError("no network")


class Weather(unittest.TestCase):
    def test_a_good_response_gives_conditions_high_low_and_rain_chance(self):
        self.assertEqual(run(["-33.87", "151.21"], lambda url: GOOD), (0, {
            "available": True,
            "date": "2026-11-21",
            "conditions": "Slight rain",
            "high": 18.2,
            "low": 9.1,
            "rain_chance": 70,
            "unit": "°C",
        }))

    def test_asks_open_meteo_for_the_place(self):
        urls = []
        run(["-33.87", "151.21"], lambda url: urls.append(url) or GOOD)
        self.assertTrue(urls[0].startswith("https://api.open-meteo.com/v1/forecast?"))
        self.assertIn("latitude=-33.87", urls[0])
        self.assertIn("longitude=151.21", urls[0])

    def test_maps_wmo_codes_to_words(self):
        for code, words in [(0, "Clear sky"), (3, "Overcast"), (45, "Fog"), (95, "Thunderstorm"), (1234, "Unknown")]:
            body = json.loads(GOOD)
            body["daily"]["weather_code"] = [code]
            self.assertEqual(run(["0", "0"], lambda url: json.dumps(body))[1]["conditions"], words)

    def test_a_network_error_is_not_available_and_exits_0(self):
        self.assertEqual(run(["0", "0"], fails), (0, {"available": False}))

    def test_bad_json_is_not_available_and_exits_0(self):
        self.assertEqual(run(["0", "0"], lambda url: "<html>down</html>"), (0, {"available": False}))

    def test_a_response_without_daily_data_is_not_available(self):
        self.assertEqual(run(["0", "0"], lambda url: json.dumps({"daily": {"time": []}})), (0, {"available": False}))

    def test_a_place_name_is_looked_up_then_forecast_at_the_first_match(self):
        urls = []

        def fetch(url):
            urls.append(url)
            return GEO if "geocoding-api" in url else GOOD

        code, out = run(["Mount", "Gravatt"], fetch)
        self.assertEqual((code, out["available"], out["conditions"]), (0, True, "Slight rain"))
        self.assertTrue(urls[0].startswith("https://geocoding-api.open-meteo.com/v1/search?"))
        self.assertIn("name=Mount+Gravatt", urls[0])
        self.assertIn("count=1", urls[0])
        self.assertIn("latitude=-27.47", urls[1])
        self.assertIn("longitude=153.02", urls[1])

    def test_a_place_name_that_finds_nothing_is_not_available(self):
        self.assertEqual(run(["Nowhere"], lambda url: json.dumps({"generationtime_ms": 1})), (0, {"available": False}))

    def test_a_place_lookup_that_fails_is_not_available(self):
        self.assertEqual(run(["Brisbane"], fails), (0, {"available": False}))

    def test_bad_arguments_are_not_available_and_exit_0(self):
        self.assertEqual(run(["north"], lambda url: GOOD), (0, {"available": False}))


if __name__ == "__main__":
    unittest.main()
