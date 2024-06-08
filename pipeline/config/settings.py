"""
A module for settings in the pipeline.config package.
"""

from functools import lru_cache

from pydantic import (
    AnyHttpUrl,
    NegativeFloat,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    PostgresDsn,
    field_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import ValidationInfo
from pydantic_extra_types.coordinate import Latitude, Longitude
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class based on Pydantic Base Settings for environment variables
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    API_URL: AnyHttpUrl
    PATH_PARAMETER: str
    ID_PATH_PARAMETER: str
    API_KEY: str
    DEFAULT_LAT: Latitude
    DEFAULT_LNG: Longitude
    RATE_LIMIT_THRESHOLD: PositiveInt = 120  # requests per minute
    RATE_LIMIT_RESET_TIME: PositiveInt = 60  # seconds
    PREFIX: str = "https://"  # prefix used for mounting the HTTP session
    MAX_RETRIES: PositiveInt = 3
    POOL_CONNECTIONS: PositiveInt = 10  # connections pools to cache in terms
    # of endpoints
    POOL_MAXSIZE: PositiveInt = 20  # max connections to cache in the pool
    RETRY_BACKOFF_FACTOR: PositiveFloat = 0.5  # delay between retries [seconds]
    BACKOFF_MAX: PositiveInt = 60  # maximum delay between retries [seconds]
    RETRY_STATUS_FORCE_LIST: list[PositiveInt] = [
        429,
        502,
        503,
        504,
    ]

    POSTGRES_SCHEME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: PositiveInt
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_postgresql_connection(
        cls,
        v: str | None,
        info: ValidationInfo,
    ) -> PostgresDsn:
        """
        Assemble the database connection as URI string
        :param v: Variables to consider
        :type v: str | NoneType
        :param info: The field validation info
        :type info: ValidationInfo
        :return: SQLAlchemy URI
        :rtype: PostgresDsn
        """
        if info.config is None:
            raise ValueError("info.config cannot be None")
        uri: MultiHostUrl = MultiHostUrl.build(
            scheme=info.data.get("POSTGRES_SCHEME", "postgres"),
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            port=info.data.get("POSTGRES_PORT"),
            path=info.data.get("POSTGRES_DB"),
        )
        return PostgresDsn(f"{uri}")

    LOWEST_TEMP: NegativeFloat
    HIGHEST_TEMP: PositiveFloat
    HIGHEST_RAIN_DEPTH: PositiveFloat
    LOWEST_HUMIDITY: NonNegativeInt
    HIGHEST_HUMIDITY: PositiveInt
    HIGHEST_EVAPORATION: PositiveFloat
    HIGHEST_SUNSHINE: PositiveFloat
    HIGHEST_WIND_SPEED: PositiveInt
    LOWEST_PRESSURE: PositiveFloat
    HIGHEST_PRESSURE: PositiveFloat
    HIGHEST_CLOUD_SCALE: PositiveInt

    HIGHEST_CLOUDINESS_PCT: PositiveFloat
    HIGHEST_WIND_DEGREES: PositiveInt


@lru_cache
def get_settings() -> Settings:
    """
    Get settings cached
    :return: The settings instance
    :rtype: Settings
    """
    return Settings()


settings: Settings = get_settings()
