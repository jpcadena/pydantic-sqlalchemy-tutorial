"""
A module for user in the app-schemas package.
"""

from datetime import date

from phonenumbers import PhoneNumber
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic.config import JsonDict
from pydantic_extra_types.phone_numbers import (
    PhoneNumber as PydanticPhoneNumber,
)

from app.config.init_settings import init_setting
from app.config.utils import validate_password, validate_phone_number

user_example: JsonDict = {
    "example": {
        "username": "username",
        "email": "example@mail.com",
        "birthdate": date(2004, 1, 1).strftime(init_setting.DATE_FORMAT),
        "phone_number": str(PydanticPhoneNumber("+593987654321")),
        "password": "Hk7pH9*35Fu&3U",
    }
}


class UserBase(BaseModel):
    model_config = ConfigDict(
        json_schema_extra=user_example,
    )

    username: str | None = Field(
        default=None,
        title="Username",
        description="Username to identify the user",
        min_length=4,
        max_length=15,
    )
    email: EmailStr | None = Field(
        default=None,
        title="Email",
        description="Preferred e-mail address of " "the User",
    )
    password: str | None = Field(
        default=None,
        title="Password",
        description="Password of the User",
        min_length=8,
        max_length=14,
    )
    birthdate: date | None = Field(
        default=None, title="Birthdate", description="Birthday of the User"
    )
    phone_number: PhoneNumber | None = Field(
        default=None,
        title="Phone number",
        description="Preferred telephone number of the User",
    )

    @field_validator("phone_number", mode="before")
    def validate_phone_number(
        cls, v: PydanticPhoneNumber | None
    ) -> PydanticPhoneNumber | None:
        """
        Validates the phone number attribute
        :param v: The phone number value to validate
        :type v: Optional[PhoneNumber]
        :return: The validated phone number
        :rtype: Optional[PhoneNumber]
        """
        return validate_phone_number(v)

    @field_validator("password", mode="before")
    def validate_password(cls, v: str | None) -> str:
        """
        Validates the password attribute
        :param v: The password to be validated
        :type v: Optional[str]
        :return: The validated password
        :rtype: str
        """
        return validate_password(v)


class UserCreate(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    username: str
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """
    Schema for updating a User record.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


class User(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    password: str = Field(
        ...,
        title="Hashed Password",
        description="Hashed Password of the User",
        min_length=60,
        max_length=60,
    )


class UsersResponse(BaseModel):
    """
    Class representation for a list of users response
    """

    users: list[User]
