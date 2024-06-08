"""
A module for session in the pipeline.db package.
"""

import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generator, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from pipeline.config.settings import settings

logger: logging.Logger = logging.getLogger(__name__)
url: str = f"{settings.SQLALCHEMY_DATABASE_URI}"

# Create a context variable to store the current user
current_user: ContextVar[Optional[str]] = ContextVar(
    "current_user", default=None
)
engine: Engine = create_engine(
    url,
    pool_pre_ping=True,
    future=True,
    echo=True,
)
session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def set_current_user(
    user_id: str,
) -> None:
    """
    Set the current user in the context.
    This function should be called at the beginning of each request or
     operation.
    :param user_id: The user to set for audit info in the tables
    :type user_id: str
    :return: None
    :rtype: NoneType
    """
    current_user.set(user_id)


def fetch_current_user() -> Optional[str]:
    """
    Fetch the current user from the context.
    This function will be called by the event listeners in the model.
    :return: The current user for audit table section
    :rtype: Optional[str]
    """
    return current_user.get()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Get a database session as a context manager
    :return: Database session and engine
    :rtype: Generator[Session, None, None]
    """
    if username := (
        settings.SQLALCHEMY_DATABASE_URI.hosts()[0]["username"]  # type: ignore
    ):
        set_current_user(username)
    session: Session = session_local()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()
        engine.dispose()
