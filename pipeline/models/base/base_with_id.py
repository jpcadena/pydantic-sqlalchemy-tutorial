"""
A module for base with id in the pipeline.models.base package.
"""

from sqlalchemy import Connection
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, Mapper, mapped_column

from pipeline.db.session import fetch_current_user
from pipeline.models.base.base import Base, U


class BaseWithID(Base):
    """
    Base model class to handle ID comment dynamically in schemas representation.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        autoincrement="auto",
        index=True,
        unique=True,
        comment="ID of the table ",
    )

    @staticmethod
    def _extract_entity_name(table_name: str) -> str:
        parts: list[str] = table_name.split("_")
        return "_".join(parts[3:-1]) if len(parts) > 4 else table_name

    @classmethod
    def update_column_comments(cls) -> None:
        """
        Update the ID column comment dynamically with table names
        :return: None
        :rtype: NoneType
        """
        table_name: str = cls.__tablename__
        entity_name: str = cls._extract_entity_name(table_name)
        for column in cls.__table__.columns:
            if column.comment:
                column.comment = column.comment + entity_name  # type: ignore


@listens_for(
    BaseWithID,
    "before_insert",
    propagate=True,
)
def set_created_by(
    mapper: Mapper[U],
    connection: Connection,
    target: U,
) -> None:
    """
    Event listener function to set 'created_by' field before inserting a
     new record. This function is triggered automatically into the database.
    :param mapper: The mapper handling the object instance being inserted.
    :type mapper: Mapper[U]
    :param connection: The database connection being used for the operation.
    :type connection: Connection
    :param target: The actual instance of the object being inserted into the
     database.
    :type target: U
    """
    current_user = fetch_current_user()
    if isinstance(current_user, str):
        target.created_by = current_user


@listens_for(
    Base,
    "before_update",
    propagate=True,
)
def set_updated_by(
    mapper: Mapper[U],
    connection: Connection,
    target: U,
) -> None:
    """
    Event listener function to set 'updated_by' field before updating a
     new record. This function is triggered automatically into the database.
    :param mapper: The mapper handling the object instance being inserted.
    :type mapper: Mapper[U]
    :param connection: The database connection being used for the operation.
    :type connection: Connection
    :param target: The actual instance of the object being updated into the
     database.
    :type target: U
    """
    current_user = fetch_current_user()
    if isinstance(current_user, str):
        target.updated_by = current_user
