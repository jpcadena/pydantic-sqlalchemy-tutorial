"""
A module for base in the pipeline-models-base package.
"""

from typing import TypeVar

from sqlalchemy.orm import DeclarativeBase

from pipeline.models.weather import Weather


class Base(DeclarativeBase):
    pass


U = TypeVar("U", bound="Weather")
