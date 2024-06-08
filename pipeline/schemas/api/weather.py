"""
A module for weather in the pipeline.schemas.api package.
"""

from typing import Optional, TypeVar

from pydantic import (
    BaseModel,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
)
from pydantic_extra_types.coordinate import Latitude, Longitude

from pipeline.config.settings import settings

T = TypeVar("T", bound="BaseModel")


class WeatherDescription(BaseModel):
    id: PositiveInt
    main: str
    description: str
    icon: str


class Main(BaseModel):
    temp: PositiveFloat
    feels_like: PositiveFloat
    pressure: NonNegativeInt
    humidity: NonNegativeInt
    temp_min: Optional[PositiveFloat] = None
    temp_max: Optional[PositiveFloat] = None


class Rain(BaseModel):
    one_hour: Optional[NonNegativeFloat] = None


class Snow(BaseModel):
    one_hour: Optional[NonNegativeFloat] = None


class CurrentWeather(BaseModel):
    dt: NonNegativeInt
    sunrise: Optional[NonNegativeInt] = None
    sunset: Optional[NonNegativeInt] = None
    temp: PositiveFloat = Field(
        ...,
        title="Temp",
        description="Temperature",
        ge=settings.LOWEST_TEMP,
        le=settings.HIGHEST_TEMP,
    )
    feels_like: PositiveFloat
    pressure: NonNegativeInt
    humidity: NonNegativeInt = Field(
        ...,
        title="Humidity",
        description="Humidity %",
        ge=settings.LOWEST_HUMIDITY,
        le=settings.HIGHEST_HUMIDITY,
    )
    dew_point: PositiveFloat
    uvi: NonNegativeFloat
    clouds: NonNegativeInt = Field(
        ...,
        title="Clouds",
        description="Cloudiness %",
        le=settings.HIGHEST_CLOUDINESS_PCT,
    )
    visibility: NonNegativeInt
    wind_speed: NonNegativeFloat
    wind_deg: NonNegativeInt = Field(
        ...,
        title="Wind Deg",
        description="Wind direction, degrees (meteorological)",
        le=settings.HIGHEST_WIND_DEGREES,
    )
    wind_gust: Optional[NonNegativeFloat] = None
    weather: list[WeatherDescription]
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None


class MinutelyWeather(BaseModel):
    dt: NonNegativeInt
    precipitation: NonNegativeFloat


class HourlyWeather(CurrentWeather):
    pop: NonNegativeFloat = Field(
        ...,
        title="Pop",
        description="Pop",
        le=1,
    )


class DailyTemp(BaseModel):
    morn: PositiveFloat
    day: PositiveFloat
    eve: PositiveFloat
    night: PositiveFloat
    min: PositiveFloat
    max: PositiveFloat


class DailyFeelsLike(BaseModel):
    morn: PositiveFloat
    day: PositiveFloat
    eve: PositiveFloat
    night: PositiveFloat


class DailyWeather(BaseModel):
    dt: NonNegativeInt
    sunrise: Optional[NonNegativeInt] = None
    sunset: Optional[NonNegativeInt] = None
    moonrise: Optional[NonNegativeInt] = None
    moonset: Optional[NonNegativeInt] = None
    moon_phase: NonNegativeFloat = Field(
        ...,
        title="Moon Phase",
        description="Moon Phase",
        le=1,
    )
    summary: str
    temp: DailyTemp
    feels_like: DailyFeelsLike
    pressure: NonNegativeInt
    humidity: NonNegativeInt
    dew_point: PositiveFloat
    wind_speed: NonNegativeFloat
    wind_deg: NonNegativeInt = Field(
        ...,
        title="Wind Deg",
        description="Wind Degrees",
        le=settings.HIGHEST_WIND_DEGREES,
    )
    wind_gust: Optional[NonNegativeFloat] = None
    weather: list[WeatherDescription]
    clouds: NonNegativeInt = Field(
        ...,
        title="Clouds",
        description="Clouds",
        le=settings.HIGHEST_CLOUDINESS_PCT,
    )
    pop: NonNegativeFloat = Field(
        ...,
        title="Pop",
        description="Pop",
        le=1,
    )
    rain: Optional[NonNegativeFloat] = None
    snow: Optional[NonNegativeFloat] = None
    uvi: NonNegativeFloat


class Alert(BaseModel):
    sender_name: str
    event: str
    start: NonNegativeInt
    end: NonNegativeInt
    description: str
    tags: list[str]


class APIWeather(BaseModel):
    lat: Latitude
    lon: Longitude
    timezone: str
    timezone_offset: int
    current: CurrentWeather
    minutely: Optional[list[MinutelyWeather]] = None
    hourly: Optional[list[HourlyWeather]] = None
    daily: Optional[list[DailyWeather]] = None
    alerts: Optional[list[Alert]] = None
