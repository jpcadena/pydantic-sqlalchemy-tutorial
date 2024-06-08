"""
A module for base in the pipeline-repository package.
"""

import logging
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from pipeline.core.decorators import benchmark
from pipeline.models.base.base_with_id import U

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
        arg0: Any,
        exc: Any,
    ) -> None:
        """
        Handle the exception raised from SQLAlchemy database operation
        :param arg0: Any argument to add on the exception
        :type arg0: Any
        :param exc: The exception raised
        :type exc: Any
        :return: None
        :rtype: NoneType
        """
        self.session.rollback()
        logger.error(f"{arg0}{exc}")
        raise

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
