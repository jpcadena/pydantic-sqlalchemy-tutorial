"""
A module for transformation in the pipeline-engineering package.
"""

from pipeline.core.decorators import benchmark, with_logging
from pipeline.exceptions.exceptions import DataQualityException
from pipeline.models.weather import Weather
from pipeline.schemas.api.weather import APIWeather, CurrentWeather
from pipeline.schemas.files.weather import CSVWeather


@with_logging
@benchmark
def transform_data(csv_weather: CSVWeather, api_weather: APIWeather) -> Weather:
    """
    Transform and combine data from CSV and API into a unified structure.
    :param csv_weather: Weather data from the CSV.
    :type csv_weather: CSVWeather
    :param api_weather: Current weather data from the API.
    :type api_weather: APIWeather
    :return: Combined weather data
    :rtype: Weather
    """
    current_weather: CurrentWeather = api_weather.current
    if not (
        csv_weather.min_temp <= current_weather.temp <= csv_weather.max_temp
    ):
        raise DataQualityException(
            f"Current temperature {current_weather.temp} is outside the range"
            f" of min_temp {csv_weather.min_temp} and max_temp"
            f" {csv_weather.max_temp}"
        )
    weather: Weather = Weather(
        date=csv_weather.date,
        min_temp=csv_weather.min_temp,
        max_temp=csv_weather.max_temp,
        rainfall=csv_weather.rainfall,
        humidity_9am=csv_weather.humidity_9am,
        humidity_3pm=csv_weather.humidity_3pm,
        temp_9am=csv_weather.temp_9am,
        temp_3pm=csv_weather.temp_3pm,
        current_temp=current_weather.temp,
        current_humidity=current_weather.humidity,
        current_weather_description=(
            current_weather.weather[0].description
            if current_weather.weather
            else "No description"
        ),
    )
    return weather
