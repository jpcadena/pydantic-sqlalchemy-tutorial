"""
This script handles CRUD (Create, Read, Update, Delete) operations for
 User objects in the database.
"""

import logging
from datetime import UTC, datetime
from typing import Any, Sequence

from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy import Row, RowMapping, select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from app.core.exceptions import DatabaseException
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate

logger: logging.Logger = logging.getLogger(__name__)


class UserRepository:
    """
    This class handles all operations (CRUD) related to a User in the
     database.
    """

    def __init__(
        self,
        session: Session,
    ):
        self.session: Session = session

    def read_by_id(self, _id: PositiveInt) -> User:
        """
        Retrieve a user from the database by its id
        :param _id: The id of the user
        :type _id: IdSpecification
        :return: The user with the specified id, or None if no such
            user exists
        :rtype: User
        """
        with self.session as session:
            stmt: Select[Any]
            stmt = select(User).where(User.id == _id)
            try:
                db_obj: Row[Any] | RowMapping = (session.scalars(stmt)).one()
                if not isinstance(db_obj, User):
                    raise ValueError("Retrieved object is not a User instance")
            except SQLAlchemyError as sa_exc:
                logger.error(sa_exc)
                logger.info("Retrieving row with id: %s", _id)
                raise DatabaseException(str(sa_exc)) from sa_exc
            return db_obj

    def read_users(
        self,
        offset: NonNegativeInt,
        limit: PositiveInt | None,
    ) -> list[UserSchema]:
        """
        Retrieve a list of users from the database, with pagination
        :param offset: The number of users to skip before starting to
         return users
        :type offset: NonNegativeInt
        :param limit: The maximum number of users to return
        :type limit: PositiveInt
        :return: A list of users
        :rtype: list[UserSchema]
        """
        stmt: Select[tuple[User]] = select(User).offset(offset).limit(limit)
        with self.session as session:
            try:
                scalar_result: ScalarResult[User] = session.scalars(stmt)
                all_results: Sequence[Row[User] | RowMapping | Any] = (
                    scalar_result.all()
                )
                users: list[User] = [User(result) for result in all_results]
            except SQLAlchemyError as sa_exc:
                logger.error(sa_exc)
                raise DatabaseException(str(sa_exc)) from sa_exc
            return [UserSchema.model_validate(user) for user in users]

    def create_user(
        self,
        user: UserCreate,
    ) -> User:
        """
        Create a new user in the database.
        :param user: An object containing the information of the user
         to create
        :type user: UserCreate
        :return: The created user object
        :rtype: User
        """
        user_data: dict[str, Any] = user.model_dump()
        user_create: User = User(**user_data)
        with self.session as session:
            try:
                session.add(user_create)
                session.commit()
            except SQLAlchemyError as sa_exc:
                logger.error(sa_exc)
                session.rollback()
                raise DatabaseException(str(sa_exc)) from sa_exc
            if created_user := self.read_by_id(user_create.id):
                return created_user
            else:
                raise DatabaseException("User could not be created")

    def update_user(self, _id: PositiveInt, user: UserUpdate) -> User | None:
        """
        Update the information of a user in the database
        :param _id: The id of the user to update
        :type _id: PositiveInt
        :param user: An object containing the new information of the
         user
        :type user: UserUpdate
        :return: The updated user, or None if no such user exists
        :rtype: Optional[User]
        """
        with self.session as session:
            try:
                found_user: User | None = self.read_by_id(_id)
            except DatabaseException as db_exc:
                logger.error(db_exc)
                raise DatabaseException(str(db_exc)) from db_exc
            if not found_user:
                raise DatabaseException(
                    f"User with ID: {_id} could not be updated"
                )
            update_data: dict[str, Any] = user.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if value is not None:
                    setattr(found_user, field, value)
            found_user.updated_at = datetime.now(UTC)
            session.add(found_user)
            session.commit()
            try:
                updated_user: User | None = self.read_by_id(_id)
            except DatabaseException as db_exc:
                logger.error(db_exc)
                raise DatabaseException(str(db_exc)) from db_exc
            return updated_user

    def delete_user(self, _id: PositiveInt) -> dict[str, Any]:
        """
        Delete a user from the database
        :param _id: The id of the user to delete
        :type _id: PositiveInt
        :return: Data to confirmation info about the delete process
        :rtype: dict[str, Any]
        """
        with self.session as session:
            try:
                exists_query = (
                    session.query(User).filter(User.id == _id).exists()
                )
                if not session.query(exists_query).scalar():
                    raise NoResultFound(f"No user found with ID: {_id}")
                delete_query = (
                    session.query(User).filter(User.id == _id).delete()
                )
                session.commit()
                if delete_query == 0:
                    raise NoResultFound(
                        f"No user found with ID: {_id} to delete"
                    )
                deleted: bool = True
                deleted_at: datetime = datetime.now()
            except (SQLAlchemyError, NoResultFound) as e:
                session.rollback()
                logger.error(
                    f"Failed to delete user with ID: {_id}, Error: {str(e)}"
                )
                raise DatabaseException(
                    f"Could not delete user with ID: {_id}. Error: {str(e)}"
                ) from e
        return {"ok": deleted, "deleted_at": deleted_at}


def get_user_repository() -> UserRepository:
    """
    Create a UserRepository with a database session, an index
     filter, and a unique filter.
    :return: A UserRepository instance
    :rtype: UserRepository
    """
    return UserRepository(
        get_session(),
    )
