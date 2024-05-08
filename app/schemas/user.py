"""
A module for user in the app-schemas package.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    pass
