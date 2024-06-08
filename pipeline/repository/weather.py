"""
A module for weather in the pipeline-repository package.
"""

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from pipeline.core.decorators import with_logging
from pipeline.models.weather import Weather
from pipeline.repository.base import BaseRepository

logger: logging.Logger = logging.getLogger(__name__)


class WeatherRepository(BaseRepository):
    """
    Repository class for Weather-specific CRUD operations.
    """

    def __init__(self, session: Session):
        super().__init__(session)

    @with_logging
    def handle_weather(self, weather: Weather) -> None:
        """
        Handle insert or update logic for a Weather instance.
        :param weather: The Weather instance to be inserted or updated.
        :type weather: Weather
        :return: None
        :rtype: NoneType
        """
        try:
            if existing_weather := (
                self.session.query(Weather).filter_by(date=weather.date).first()
            ):
                self.update(Weather(**existing_weather.__dict__))
            else:
                self.add(weather)
        except SQLAlchemyError as exc:
            self.handle_sql_exception("Failed to handle weather data: ", exc)