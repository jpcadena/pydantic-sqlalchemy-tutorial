"""
A module for user in the app models package.
"""

from datetime import datetime

from pydantic import EmailStr, PastDate, PositiveInt
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import CheckConstraint, Date, Integer, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.config.settings import setting
from app.db.base import Base


class User(Base):  # type: ignore
    """
    User model class representing the "users" table
    """

    __tablename__ = "users"

    id: Mapped[PositiveInt] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        index=True,
        unique=True,
        comment="ID of the User",
    )
    username: Mapped[str] = mapped_column(
        String(15),
        index=True,
        unique=True,
        nullable=False,
        comment="Username to identify the user",
    )
    email: Mapped[EmailStr] = mapped_column(
        String(320),
        index=True,
        unique=True,
        nullable=False,
        comment="Preferred e-mail address of the User",
    )
    password: Mapped[str] = mapped_column(
        String(60), nullable=False, comment="Hashed password of the User"
    )
    birthdate: Mapped[PastDate] = mapped_column(
        Date, nullable=True, comment="Birthday of the User"
    )
    phone_number: Mapped[PhoneNumber] = mapped_column(
        String(20),
        nullable=True,
        comment="Preferred telephone number of the User",
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True, precision=setting.TIMESTAMP_PRECISION),
        default=datetime.now(),
        nullable=False,
        server_default=text("now()"),
        comment="Time the User was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True, precision=setting.TIMESTAMP_PRECISION),
        nullable=True,
        onupdate=text("now()"),
        comment="Time the User was updated",
    )

    __table_args__ = (
        CheckConstraint(
            "char_length(username) >= 4", name="users_username_length"
        ),
        CheckConstraint("char_length(email) >= 3", name="users_email_length"),
        CheckConstraint(setting.DB_EMAIL_CONSTRAINT, name="users_email_format"),
        CheckConstraint("LENGTH(password) = 60", name="users_password_length"),
        CheckConstraint(
            setting.DB_PHONE_NUMBER_CONSTRAINT,
            name="users_phone_number_format",
        ),
    )
