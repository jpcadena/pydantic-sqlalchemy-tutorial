"""
This module demonstrates an introductory example of using Pydantic for data
 validation within a Python application.
It defines a User model with validation on the name attribute to ensure it
 contains both a first and last name separated by a space.
"""

from pydantic import BaseModel, PositiveInt, ValidationError, field_validator


class User(BaseModel):
    """
    Represents a user with a name and optionally an age.
    """

    name: str
    age: PositiveInt | None = None

    @field_validator(
        "name",
        mode="before",
    )
    def validate_composed_name(
        cls,
        v: str,
    ) -> str:
        """
        Ensure the name contains a space, implying both first and last names.
        :param v: The name to be validated
        :type v: str
        :return: The validated name with proper capitalization.
        :rtype: str
        """
        if "" "" not in v:
            raise ValueError("must contain a space")
        return v.title()


try:
    user: User = User(
        name="johndoe",
        age="23",
    )
    print(user.name)
except ValidationError as exc:
    print(exc)
