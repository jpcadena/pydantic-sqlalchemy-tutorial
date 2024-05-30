"""
A module for lifecycle in the app-core package.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from app.config.init_settings import get_init_settings
from app.config.settings import get_settings
from app.crud.user import get_user_repository

logger: logging.Logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[Any, None]:
    """
    The lifespan of the application
    :param application: The FastAPI application
    :type application: FastAPI
    :return: An asynchronous generator for the application
    :rtype: AsyncGenerator[Any, None]
    """
    logger.info("Starting API...")
    try:
        application.state.settings = get_settings()
        application.state.init_settings = get_init_settings()
        application.state.user_repository = get_user_repository()
        logger.info("Configuration settings loaded.")
        yield
    except Exception as exc:
        logger.error(f"Error during application startup: {exc}")
        raise
    finally:
        logger.info("Application shutdown completed.")
