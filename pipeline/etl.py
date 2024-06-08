"""
A module for etl in the pipeline package.
"""

import logging

from pydantic import FilePath

from pipeline.config.init_settings import init_settings
from pipeline.config.settings import settings
from pipeline.core.decorators import benchmark, with_logging
from pipeline.core.logging_setup import setup_logging
from pipeline.db.session import get_db
from pipeline.engineering.extraction import extract_api_data, extract_csv_data
from pipeline.engineering.loading import load_data
from pipeline.engineering.transformation import transform_data
from pipeline.models.weather import Weather
from pipeline.schemas.api.weather import APIWeather
from pipeline.schemas.files.weather import CSVWeather

setup_logging(init_settings)
logger: logging.Logger = logging.getLogger(__name__)


@with_logging
@benchmark
def main() -> None:
    """
    The main function to execute the pipeline
    :return: None
    :rtype: NoneType
    """
    logger.info("Data extraction")
    api_weather_data: APIWeather = extract_api_data(settings)
    filepath: FilePath = FilePath("data/raw/weatherAUS.csv")
    csv_weather_data: list[CSVWeather] = extract_csv_data(
        filepath, init_settings
    )
    logger.info("Data transformation")
    weather: Weather = transform_data(csv_weather_data[0], api_weather_data)
    with get_db() as session:
        load_data(session, weather)
    logger.info("Loaded data")


if __name__ == "__main__":
    logger.info("Pipeline to be executed")
    main()
    logger.info("Pipeline finished")
