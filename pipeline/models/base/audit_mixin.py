"""
A module for audit mixin in the pipeline.models.base package.
"""

from datetime import datetime

from sqlalchemy import CheckConstraint, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class AuditMixin:
    """
    Mixin class for audit information on SQL tables in the STG layer
    """

    created_by: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        server_default=func.current_user(),
        comment="User that created the record",
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        comment="Datetime when the record was created",
    )
    updated_by: Mapped[str | None] = mapped_column(
        VARCHAR(50),
        nullable=True,
        onupdate=func.current_user(),
        comment="Last user that updated the record",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=func.current_timestamp(),
        comment="Last timestamp when the record was updated",
    )

    @classmethod
    def __declare_last__(cls) -> None:
        """
        Hook to dynamically add constraints with the table name after the table
         is created.
        :return: None
        :rtype: NoneType
        """
        table_name: str = cls.__tablename__
        constraints: list[CheckConstraint] = [
            CheckConstraint(
                "created_at <= CURRENT_TIMESTAMP",
                name=f"{table_name}_created_by_check",
            ),
            CheckConstraint(
                "updated_by IS NULL OR" " updated_by <= CURRENT_TIMESTAMP",
                name=f"{table_name}_updated_by_check",
            ),
        ]
        cls.__table__.append_constraint(constraints[0])
        cls.__table__.append_constraint(constraints[1])
