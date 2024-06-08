"""
A module for extraction in the pipeline-engineering package.
"""

import csv
import json
from typing import Any

from pydantic import FilePath

from pipeline.config.init_settings import InitSettings
from pipeline.config.settings import Settings
from pipeline.core.decorators import benchmark, with_logging
from pipeline.schemas.api.weather import APIWeather
from pipeline.schemas.files.weather import CSVWeather
from pipeline.services.external.api.weather import WeatherApiService


@with_logging
@benchmark
def extract_api_data(settings: Settings) -> APIWeather:
    """
    Extract the weather data from the OpenWeather API
    :param settings: The project settings to handle the service
    :type settings: Settings
    :return: The weather data as a model object
    :rtype: APIWeather
    """
    weather_api_service: WeatherApiService = WeatherApiService(settings)
    api_weather: APIWeather = weather_api_service.get_weather_data()
    return api_weather


@with_logging
@benchmark
def extract_csv_data(
    filepath: FilePath, init_settings: InitSettings
) -> list[CSVWeather]:
    """
    Reads a CSV file and converts it into a list of CSVWeatherModel instances.
    :param filepath: The path to the CSV file.
    :type filepath: FilePath
    :param init_settings: The initial settings
    :type init_settings: InitSettings
    :return: A list of CSVWeatherModel instances representing each row in the
     CSV.
    :rtype: list[CSVWeatherModel]
    """
    data: list[CSVWeather] = []
    with open(
        filepath, encoding=init_settings.ENCODING, newline=""
    ) as text_io_wrapper:
        dict_reader: csv.DictReader[Any] = csv.DictReader(text_io_wrapper)
        for row in dict_reader:
            try:
                parsed_row: dict[str, Any] = {
                    key: json.loads(value) if value.startswith("{") else value
                    for key, value in row.items()
                }
                csv_weather: CSVWeather = CSVWeather(**parsed_row)
                data.append(csv_weather)
            except Exception as e:
                print(f"Error processing row {row}: {e}")
    return data
