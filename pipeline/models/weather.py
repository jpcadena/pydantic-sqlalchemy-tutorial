"""
A module for weather in the pipeline-models package.
"""

from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import DATE, FLOAT, INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from pipeline.config.settings import settings
from pipeline.models.base.audit_mixin import AuditMixin
from pipeline.models.base.base_with_id import BaseWithID


class Weather(AuditMixin, BaseWithID):
    __tablename__ = "weather"

    date: Mapped[date] = mapped_column(
        DATE,
        index=True,
        nullable=False,
        unique=True,
        comment="Date for the record about the weather",
    )
    min_temp: Mapped[float] = mapped_column(
        FLOAT,
        comment="Minimum temperature of the day",
    )
    max_temp: Mapped[float] = mapped_column(
        FLOAT,
        comment="Maximum temperature of the day",
    )
    rainfall: Mapped[float] = mapped_column(
        FLOAT,
        comment="Rainfall in millimeters",
    )
    humidity_9am: Mapped[int] = mapped_column(
        INTEGER,
        comment="Humidity percentage at 9 AM",
    )
    humidity_3pm: Mapped[int] = mapped_column(
        INTEGER,
        comment="Humidity percentage at 3 PM",
    )
    temp_9am: Mapped[float] = mapped_column(
        FLOAT,
        comment="Temperature at 9 AM",
    )
    temp_3pm: Mapped[float] = mapped_column(
        FLOAT,
        comment="Temperature at 3 PM",
    )
    current_temp: Mapped[float] = mapped_column(
        FLOAT,
        comment="Current temperature from the API",
    )
    current_humidity: Mapped[int] = mapped_column(
        INTEGER,
        comment="Current humidity percentage from the API",
    )
    current_weather_description: Mapped[str] = mapped_column(
        VARCHAR,
        comment="Current weather description from the API",
    )

    __table_args__ = (
        CheckConstraint(
            "date <= CURRENT_DATE",
            name="weather_date_check",
        ),
        CheckConstraint(
            f"min_temp BETWEEN {settings.LOWEST_TEMP} AND"
            f" {settings.HIGHEST_TEMP}",
            name="weather_min_temp_range_check",
        ),
        CheckConstraint(
            f"max_temp BETWEEN {settings.LOWEST_TEMP} AND"
            f" {settings.HIGHEST_TEMP}",
            name="weather_max_temp_range_check",
        ),
        CheckConstraint(
            f"rainfall <= {settings.HIGHEST_RAIN_DEPTH}",
            name="weather_max_rainfall_check",
        ),
        CheckConstraint(
            f"humidity_9am BETWEEN {settings.LOWEST_HUMIDITY} AND"
            f" {settings.HIGHEST_HUMIDITY}",
            name="weather_humidity_9am_check",
        ),
        CheckConstraint(
            f"humidity_3pm BETWEEN {settings.LOWEST_HUMIDITY} AND"
            f" {settings.HIGHEST_HUMIDITY}",
            name="weather_humidity_3pm_check",
        ),
        CheckConstraint(
            f"current_humidity BETWEEN {settings.LOWEST_HUMIDITY} AND"
            f" {settings.HIGHEST_HUMIDITY}",
            name="weather_current_humidity_check",
        ),
        CheckConstraint(
            "min_temp <= max_temp",
            name="weather_min_max_temp_check",
        ),
        CheckConstraint(
            "temp_9am BETWEEN min_temp AND max_temp",
            name="weather_temp_9am_range_check",
        ),
        CheckConstraint(
            "temp_3pm BETWEEN min_temp AND max_temp",
            name="weather_temp_3pm_range_check",
        ),
        CheckConstraint(
            "current_temp BETWEEN min_temp AND max_temp",
            name="weather_current_temp_range_check",
        ),
    )
