"""
A module for base settings in the app.core.config package.
"""

import base64
from datetime import date
from functools import lru_cache
from pathlib import Path

from fastapi.openapi.models import Example
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_image_b64(image_path: str) -> str:
    """
    Converts an image to base64 format
    :param image_path: Path to the image file
    :type image_path: str
    :return: The image file in base64 format
    :rtype: str
    """
    return base64.b64encode(Path(image_path).read_bytes()).decode("utf")


img_b64: str = get_image_b64("./assets/images/project.png")
users_b64: str = get_image_b64("./assets/images/users.png")


class InitSettings(BaseSettings):
    """
    Init Settings class based on Pydantic Base Settings
    """

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="allow",
    )

    SALUTE: str = "Salute!"
    ROOT_MSG: str = "Hello, World!"
    SERVER_NAME: str = "FastAPI Server"
    PROJECT_NAME: str = "pydantic-sqlalchemy-tutorial"
    VERSION: str = "1.0"
    ENCODING: str = "UTF-8"
    OPENAPI_FILE_PATH: str = "/openapi.json"
    DATE_FORMAT: str = "%Y-%m-%d"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    FILE_DATE_FORMAT: str = "%d-%b-%Y-%H-%M-%S"
    IMAGES_APP: str = "images"
    IMAGES_PATH: str = "/assets/images"
    IMAGES_DIRECTORY: str = "assets/images"
    LOG_FORMAT: str = (
        "[%(name)s][%(asctime)s][%(levelname)s][%(module)s]"
        "[%(funcName)s][%(lineno)d]: %(message)s"
    )
    PASSWORD_REGEX: str = (
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?" "[#?!@$%^&*-]).{8,14}$"
    )
    SUMMARY: str = """This backend project is a small demo as a use case for
     FastAPI with Pydantic and SQLAlchemy..
    """
    DESCRIPTION: str = f"""**FastAPI**, **Pydantic** and **SQLAlchemy** helps
     you do awesome stuff. 🚀
    \n\n<img src="data:image/png;base64,{img_b64}"/>"""
    LICENSE_INFO: dict[str, str] = {
        "name": "MIT",
        "identifier": "MIT",
    }
    TAGS_METADATA: list[dict[str, str]] = [
        {
            "name": "user",
            "description": f"""Operations with users, such as register, get,
             update and delete.\n\n<img src="data:image/png;base64,
             {users_b64}" width="150" height="100"/>""",
        },
    ]
    USER_CREATE_EXAMPLES: dict[str, Example] = {
        "normal": {
            "summary": "A normal example",
            "description": "A **normal** user create object that works "
            "correctly.",
            "value": {
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U",
                "birthdate": date(2004, 12, 31),
                "phone_number": PhoneNumber("+593987654321"),
            },
        },
        "converted": {
            "summary": "An example with converted data",
            "description": "FastAPI can convert phone number `strings` to "
            "actual `numbers` automatically",
            "value": {
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U",
                "birthdate": date(2004, 12, 31),
                "phone_number": PhoneNumber(593987654321),
            },
        },
        "invalid": {
            "summary": "Invalid data is rejected with an error",
            "value": {
                "username": "username",
                "email": "username",
                "password": "Password123",
                "birthdate": date(95, 12, 31),
                "phone_number": PhoneNumber("5939876a4321"),
            },
        },
    }
    USER_UPDATE_EXAMPLES: dict[str, Example] = {
        "normal": {
            "summary": "A normal example",
            "description": "A **normal** user update object that works "
            "correctly.",
            "value": {
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U",
                "birthdate": date(2004, 12, 31),
                "phone_number": PhoneNumber(593987654321),
            },
        },
        "converted": {
            "summary": "An example with converted data",
            "description": "FastAPI can convert phone numbers `strings` to "
            "actual `numbers` automatically",
            "value": {
                "username": "username",
                "email": "example@mail.com",
                "password": "Hk7pH9*35Fu&3U",
                "birthdate": date(2004, 12, 31),
                "phone_number": PhoneNumber("593987654321"),
            },
        },
        "invalid": {
            "summary": "Invalid data is rejected with an error",
            "value": {
                "username": "username",
                "email": "username",
                "password": "Password123",
                "birthdate": date(95, 12, 31),
                "phone_number": PhoneNumber("59398x54321"),
            },
        },
    }
    LIMIT_EXAMPLES: dict[str, Example] = {
        "normal": {
            "summary": "A normal example",
            "description": "A **normal** limit query parameter that works "
            "correctly.",
            "value": 1,
        },
        "converted": {
            "summary": "An example with converted data",
            "description": "FastAPI can convert limit `strings` to actual"
            " `numbers` automatically",
            "value": "5",
        },
        "invalid": {
            "summary": "Invalid data is rejected with an error",
            "value": -1,
        },
    }
    SKIP_EXAMPLES: dict[str, Example] = {
        "normal": {
            "summary": "A normal example",
            "description": "A **normal** skip query parameter that works "
            "correctly.",
            "value": 0,
        },
        "converted": {
            "summary": "An example with converted data",
            "description": "FastAPI can convert skip `strings` to actual"
            " `numbers` automatically",
            "value": "20",
        },
        "invalid": {
            "summary": "Invalid data is rejected with an error",
            "value": -1,
        },
    }


@lru_cache
def get_init_settings() -> InitSettings:
    """
    Get settings cached
    :return: The settings instance
    :rtype: Settings
    """
    return InitSettings()


init_setting: InitSettings = get_init_settings()
