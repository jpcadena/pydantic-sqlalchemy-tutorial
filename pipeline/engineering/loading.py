"""
A module for loading in the pipeline-engineering package.
"""

from sqlalchemy.orm import Session

from pipeline.core.decorators import with_logging
from pipeline.models.weather import Weather
from pipeline.repository.weather import WeatherRepository


@with_logging
def load_data(session: Session, weather: Weather) -> None:
    """
    Load weather data into the database table.
    :param session: The database session to handle CRUD operations
    :type session: Session
    :param weather: The weather data as a SQLAlchemy model instance
    :type weather: Weather
    """
    weather_repository: WeatherRepository = WeatherRepository(session)
    weather_repository.handle_weather(weather)
