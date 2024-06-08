"""
A module for base in the pipeline-repository package.
"""

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from pipeline.core.decorators import benchmark
from pipeline.exceptions.exceptions import DatabaseException
from pipeline.models.base.base import U

logger: logging.Logger = logging.getLogger(__name__)


class BaseRepository:
    """
    Base class for repository in the database schemas.
    """

    def __init__(
        self,
        session: Session,
    ):
        self.session: Session = session

    @benchmark
    def handle_sql_exception(
        self,
        message: str,
        exc: SQLAlchemyError,
    ) -> None:
        """
        Handle the exception raised from SQLAlchemy database operation
        :param message: Custom message for the exception
        :type message: str
        :param exc: The exception raised
        :type exc: SQLAlchemyError
        :return: None
        :rtype: NoneType
        """
        self.session.rollback()
        logger.error(f"{message}{exc}")
        raise DatabaseException(f"{message}{exc}")

    @benchmark
    def add(
        self,
        entity: U,
    ) -> None:
        """
        Add a new entity to the database and commit the transaction.
        :param entity: The entity instance to be added to the database.
        :type entity: U
        :return: None
        :rtype: NoneType
        """
        try:
            self.session.add(
                entity,
            )
            self.session.commit()
        except SQLAlchemyError as exc:
            self.handle_sql_exception("Failed to add entity: ", exc)

    @benchmark
    def update(
        self,
        entity: U,
    ) -> U:
        """
        Update an existing entity in the database and commit the transaction.
        :param entity: The entity instance with updated fields to be saved to
         the database.
        :type entity: U
        :return: The updated entity.
        :rtype: U
        """
        try:
            self.session.commit()
        except SQLAlchemyError as exc:
            self.handle_sql_exception("Failed to update entity: ", exc)
        return entity
