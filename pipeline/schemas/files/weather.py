"""
A module for weather in the pipeline.schemas.files package.
"""

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PastDate,
    PositiveFloat,
    PositiveInt,
)

from pipeline.config.settings import settings


class CSVWeather(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    date: PastDate = Field(
        ...,
        alias="Date",
        title="Date",
        description="Date for the weather record",
    )
    location: str = Field(
        ...,
        alias="Location",
        title="Location",
        description="Location of the weather station",
    )
    min_temp: float = Field(
        ...,
        alias="MinTemp",
        title="Minimum Temperature",
        description="Minimum temperature of the day",
        ge=settings.LOWEST_TEMP,
        le=settings.HIGHEST_TEMP,
    )
    max_temp: float = Field(
        ...,
        alias="MaxTemp",
        title="Maximum Temperature",
        description="Maximum temperature of the day",
        ge=settings.LOWEST_TEMP,
        le=settings.HIGHEST_TEMP,
    )
    rainfall: NonNegativeFloat = Field(
        ...,
        alias="Rainfall",
        title="Rainfall",
        description="Rainfall in millimeters",
        le=settings.HIGHEST_RAIN_DEPTH,
    )
    evaporation: NonNegativeFloat = Field(
        ...,
        alias="Evaporation",
        title="Evaporation",
        description="Evaporation in millimeters",
        le=settings.HIGHEST_EVAPORATION,
    )
    sunshine: NonNegativeFloat = Field(
        ...,
        alias="Sunshine",
        title="Sunshine",
        description="Sunshine in hours",
        le=settings.HIGHEST_SUNSHINE,
    )
    wind_gust_dir: str = Field(
        ...,
        title="Wind Gust Direction",
        description="Direction of the wind gust",
        alias="WindGustDir",
    )
    wind_gust_speed: PositiveInt = Field(
        ...,
        alias="WindGustSpeed",
        title="Wind Gust Speed",
        description="Speed of the wind gust in km/h",
        le=settings.HIGHEST_WIND_SPEED,
    )
    wind_dir_9am: str = Field(
        ...,
        title="Wind Direction at 9 AM",
        description="Direction of the wind at 9 AM",
        alias="WindDir9am",
    )
    wind_dir_3pm: str = Field(
        ...,
        title="Wind Direction at 3 PM",
        description="Direction of the wind at 3 PM",
        alias="WindDir3pm",
    )
    wind_speed_9am: NonNegativeInt = Field(
        ...,
        alias="WindSpeed9am",
        title="Wind Speed at 9 AM",
        description="Speed of the wind at 9 AM in km/h",
        le=settings.HIGHEST_WIND_SPEED,
    )
    wind_speed_3pm: NonNegativeInt = Field(
        ...,
        alias="WindSpeed3pm",
        title="Wind Speed at 3 PM",
        description="Speed of the wind at 3 PM in km/h",
        le=settings.HIGHEST_WIND_SPEED,
    )
    humidity_9am: NonNegativeInt = Field(
        ...,
        alias="Humidity9am",
        title="Humidity at 9 AM",
        description="Humidity percentage at 9 AM",
        le=settings.LOWEST_HUMIDITY,
        ge=settings.HIGHEST_HUMIDITY,
    )
    humidity_3pm: NonNegativeInt = Field(
        ...,
        alias="Humidity3pm",
        title="Humidity at 3 PM",
        description="Humidity percentage at 3 PM",
        le=settings.LOWEST_HUMIDITY,
        ge=settings.HIGHEST_HUMIDITY,
    )
    pressure_9am: PositiveFloat = Field(
        ...,
        alias="Pressure9am",
        title="Pressure at 9 AM",
        description="Atmospheric pressure at 9 AM in hPa",
        ge=settings.LOWEST_PRESSURE,
        le=settings.HIGHEST_PRESSURE,
    )
    pressure_3pm: PositiveFloat = Field(
        ...,
        alias="Pressure3pm",
        title="Pressure at 3 PM",
        description="Atmospheric pressure at 3 PM in hPa",
        ge=settings.LOWEST_PRESSURE,
        le=settings.HIGHEST_PRESSURE,
    )
    cloud_9am: NonNegativeInt = Field(
        ...,
        alias="Cloud9am",
        title="Cloud Cover at 9 AM",
        description="Cloud cover at 9 AM as an octal fraction",
        le=settings.HIGHEST_CLOUD_SCALE,
    )
    cloud_3pm: NonNegativeInt = Field(
        ...,
        alias="Cloud3pm",
        title="Cloud Cover at 3 PM",
        description="Cloud cover at 3 PM as an octal fraction",
        le=settings.HIGHEST_CLOUD_SCALE,
    )
    temp_9am: float = Field(
        ...,
        alias="Temp9am",
        title="Temperature at 9 AM",
        description="Temperature at 9 AM in degrees Celsius",
        ge=settings.LOWEST_TEMP,
        le=settings.HIGHEST_TEMP,
    )
    temp_3pm: float = Field(
        ...,
        alias="Temp3pm",
        title="Temperature at 3 PM",
        description="Temperature at 3 PM in degrees Celsius",
        ge=settings.LOWEST_TEMP,
        le=settings.HIGHEST_TEMP,
    )
    rain_today: str = Field(
        ...,
        title="Rain Today",
        description="Indicator if it rained today (Yes/No)",
        alias="RainToday",
    )
    rain_tomorrow: str = Field(
        ...,
        title="Rain Tomorrow",
        description="Indicator if it is expected to rain tomorrow (Yes/No)",
        alias="RainTomorrow",
    )
