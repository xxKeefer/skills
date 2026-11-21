#!/usr/bin/env python3
import json
import sys
import urllib.parse
import urllib.request

API = "https://api.open-meteo.com/v1/forecast"
WMO = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    56: "Light freezing drizzle", 57: "Freezing drizzle",
    61: "Slight rain", 63: "Rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Freezing rain",
    71: "Slight snow", 73: "Snow", 75: "Heavy snow", 77: "Snow grains",
    80: "Slight showers", 81: "Showers", 82: "Violent showers",
    85: "Slight snow showers", 86: "Snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


def fetch_url(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.read().decode("utf-8")


def url_for(lat, lon):
    return API + "?" + urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 1,
    })


def forecast(lat, lon, fetch):
    body = json.loads(fetch(url_for(lat, lon)))
    daily = body["daily"]
    return {
        "available": True,
        "date": daily["time"][0],
        "conditions": WMO.get(daily["weather_code"][0], "Unknown"),
        "high": daily["temperature_2m_max"][0],
        "low": daily["temperature_2m_min"][0],
        "rain_chance": daily["precipitation_probability_max"][0],
        "unit": body.get("daily_units", {}).get("temperature_2m_max", "°C"),
    }


def main(argv, fetch=fetch_url):
    try:
        lat, lon = (float(a) for a in argv)
        out = forecast(lat, lon, fetch)
    except Exception:
        out = {"available": False}
    json.dump(out, sys.stdout, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
