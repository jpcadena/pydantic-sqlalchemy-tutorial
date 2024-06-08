"""
A module for base in the pipeline-models-base package.
"""

from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


U = TypeVar("U", bound="Weather")  # type: ignore
