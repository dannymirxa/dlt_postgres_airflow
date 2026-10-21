import dlt
import requests

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=3.1412"
    "&longitude=101.6865"
    "&hourly=rain"
    "&models=jma_seamless"
    "&forecast_days=11"
)


@dlt.resource(
    name="weather_hourly",
    primary_key="forecast_timestamp",
    write_disposition="merge"
)
def weather_hourly():

    response = requests.get(URL, timeout=30)

    response.raise_for_status()

    payload = response.json()

    times = payload["hourly"]["time"]
    rains = payload["hourly"]["rain"]

    for ts, rain in zip(times, rains):

        yield {
            "forecast_timestamp": ts,
            "rain_mm": rain,
            "latitude": payload["latitude"],
            "longitude": payload["longitude"],
            "timezone": payload["timezone"]
        }