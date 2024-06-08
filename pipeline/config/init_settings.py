"""
A module for init settings in the pipeline.config package.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class InitSettings(BaseSettings):
    """
    Init Settings class based on Pydantic Base Settings
    """

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="allow",
    )

    PROJECT_NAME: str = "pipeline"
    ENCODING: str = "UTF-8"
    DATE_FORMAT: str = "%Y-%m-%d"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    FILE_DATE_FORMAT: str = "%d-%b-%Y-%H-%M-%S"
    LOG_FORMAT: str = (
        "[%(name)s][%(asctime)s][%(levelname)s][%(module)s]"
        "[%(funcName)s][%(lineno)d]: %(message)s"
    )


@lru_cache
def get_init_settings() -> InitSettings:
    """
    Get init settings cached
    :return: The init settings instance
    :rtype: InitSettings
    """
    return InitSettings()


init_settings: InitSettings = get_init_settings()
