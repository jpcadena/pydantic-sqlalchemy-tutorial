"""
A module for settings in the app.core.config package.
"""

from functools import lru_cache
from typing import Any

from pydantic import (
    AnyHttpUrl,
    EmailStr,
    IPvAnyAddress,
    PositiveInt,
    PostgresDsn,
    field_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class based on Pydantic Base Settings
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    API_V1_STR: str = "/api/v1"
    SERVER_HOST: IPvAnyAddress
    SERVER_PORT: PositiveInt
    SERVER_RELOAD: bool
    SERVER_LOG_LEVEL: str
    SERVER_DESCRIPTION: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    SERVER_URL: AnyHttpUrl

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """
        Assemble a list of allowed CORS origins.
        :param v: Provided CORS origins, either a string or a list of
        strings
        :type v: Union[str, list[str]]
        :return: List of Backend CORS origins to be accepted
        :rtype: Union[list[str], str]
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, list):
            return v
        raise ValueError(v)

    TIMESTAMP_PRECISION: PositiveInt = 2
    DB_EMAIL_CONSTRAINT: str = (
        "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\" ".[A-Z|a-z]{2,}$'"
    )
    DB_PHONE_NUMBER_CONSTRAINT: str = (
        "phone_number ~ '^tel:\\+\\d{3}-\\d{2}-\\d{3}-\\d{4}$'"
    )
    DB_USER_PASSWORD_CONSTRAINT: str = "[#?!@$%^&*-]"
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
        info: ValidationInfo,  # noqa: argument-unused
    ) -> PostgresDsn:
        """
        Assemble the database connection as URI string
        :param v: Variables to consider
        :type v: str
        :param info: The field validation info
        :type info: ValidationInfo
        :return: SQLAlchemy URI
        :rtype: PostgresDsn
        """
        if info.config is None:
            raise ValueError("info.config cannot be None")
        uri: MultiHostUrl = MultiHostUrl.build(
            scheme=info.data.get("POSTGRES_SCHEME", "postgresql"),
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            port=info.data.get("POSTGRES_PORT"),
            path=info.data.get("POSTGRES_DB"),
        )
        return PostgresDsn(f"{uri}")

    CONTACT_NAME: str | None = None
    CONTACT_URL: AnyHttpUrl | None = None
    CONTACT_EMAIL: EmailStr | None = None
    CONTACT: dict[str, Any] | None = None

    @field_validator("CONTACT", mode="before")
    def assemble_contact(
        cls,
        v: str | None,
        info: ValidationInfo,  # noqa: argument-unused
    ) -> dict[str, str]:
        """
        Assemble contact information
        :param v: Variables to consider
        :type v: str
        :param info: The field validation info
        :type info: ValidationInfo
        :return: The contact attribute
        :rtype: dict[str, str]
        """
        if info.config is None:
            raise ValueError("info.config cannot be None")
        contact: dict[str, Any] = {}
        if info.data.get("CONTACT_NAME"):
            contact["name"] = info.data.get("CONTACT_NAME")
        if info.data.get("CONTACT_URL"):
            contact["url"] = info.data.get("CONTACT_URL")
        if info.data.get("CONTACT_EMAIL"):
            contact["email"] = info.data.get("CONTACT_EMAIL")
        return contact


@lru_cache
def get_settings() -> Settings:
    """
    Get settings cached
    :return: The settings instance
    :rtype: Settings
    """
    return Settings()


setting: Settings = get_settings()
