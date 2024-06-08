"""
User API Router
This module provides CRUD (Create, Retrieve, Update, Delete) operations
 for users.
"""

import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.params import Path, Query
from pydantic import NonNegativeInt, PositiveInt

from app.config.init_settings import init_setting
from app.core.exceptions import (
    DatabaseException,
    NotFoundException,
    ServiceException,
)
from app.crud.user import UserRepository, get_user_repository
from app.schemas.user import User, UserCreate, UserUpdate, UsersResponse

logger: logging.Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix="/user", tags=["user"])


@router.get("", response_model=UsersResponse)
def get_users(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    skip: Annotated[
        NonNegativeInt,
        Query(
            annotation=Optional[NonNegativeInt],
            title="Skip",
            description="Skip users",
            example=0,
            openapi_examples=init_setting.SKIP_EXAMPLES,
        ),
    ] = 0,
    limit: Annotated[
        PositiveInt | None,
        Query(
            annotation=Optional[PositiveInt],
            title="Limit",
            description="Limit pagination",
            ge=1,
            le=100,
            example=100,
            openapi_examples=init_setting.LIMIT_EXAMPLES,
        ),
    ] = 100,
) -> UsersResponse:
    """
    Retrieve all users' basic information from the system using
     pagination.
    ## Parameters:
    - `:param skip:` **Offset from where to start returning users**
    - `:type skip:` **NonNegativeInt**
    - `:param limit:` **Limit the number of results from query**
    - `:type limit:` **PositiveInt**
    ## Response:
    - `:return:` **List of Users retrieved from database**
    - `:rtype:` **UsersResponse**
    \f
    :param user_repository: Dependency method for user service layer
    :type user_repository: UserRepository
    """
    try:
        found_users: list[User] = user_repository.read_users(skip, limit)
    except ServiceException as exc:
        logger.error(exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    users: UsersResponse = UsersResponse(users=found_users)
    return users


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: Annotated[
        UserCreate,
        Body(
            ...,
            title="User data",
            description="User data to create",
            openapi_examples=init_setting.USER_CREATE_EXAMPLES,
        ),
    ],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """
    Register new user into the system.
    ## Parameter:
    - `:param user:` **Body Object for user creation.**
    - `:type user:` **UserCreate**
    ## Response:
    - `:return:` **User created with its data**
    - `:rtype:` **User**
    \f
    :param user_repository: Dependency method for user service layer
    :type user_repository: UserRepository
    """
    try:
        new_user: User | None = user_repository.create_user(user)
    except ServiceException as exc:
        detail: str = "Error at creating user."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        ) from exc
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User could not be created",
        )
    return new_user


@router.get("/{user_id}", response_model=User)
def get_user_by_id(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_id: Annotated[
        PositiveInt,
        Path(
            ...,
            title="User ID",
            annotation=PositiveInt,
            description="ID of the User to be searched",
            example=1,
        ),
    ],
) -> User:
    """
    Retrieve an existing user's information given their user ID.
    ## Parameter:
    - `:param user_id:` **Unique identifier of the user to be retrieved**
    - `:type user_id:` **PositiveInt**
    ## Response:
    - `:return:` **Found user with the given ID.**
    - `:rtype:` **User**
    \f
    :param user_repository: Dependency method for user service layer
    :type user_repository: UserRepository
    """
    try:
        user: User = user_repository.read_by_id(user_id)
    except ServiceException as exc:
        detail: str = f"User with id {user_id} not found in the system."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail
        ) from exc
    except NotFoundException as not_found_exc:
        logger.error(not_found_exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(not_found_exc)
        ) from not_found_exc
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_id: Annotated[
        PositiveInt,
        Path(
            ...,
            title="User ID",
            annotation=PositiveInt,
            description="ID of the User to be searched",
            example=1,
        ),
    ],
    user_in: Annotated[
        UserUpdate,
        Body(
            ...,
            title="User data",
            description="New user data to update",
            openapi_examples=init_setting.USER_UPDATE_EXAMPLES,
        ),
    ],
) -> User | None:
    """
    Update an existing user's information given their user ID and new
     information.
    ## Parameters:
    - `:param user_id:` **Unique identifier of the user to be updated**
    - `:type user_id:` **PositiveInt**
    - `:param user_in:` **New user data to update that can include:
     username, email, first_name, middle_name, last_name, password,
      gender, birthdate, phone_number, city and country.**
    - `:type user_in:` **UserUpdate**
    ## Response:
    - `:return:` **Updated user with the given ID and its data**
    - `:rtype:` **User**
    \f
    :param user_repository: Dependency method for user service layer
    :type user_repository: UserRepository
    """
    try:
        user: User | None = user_repository.update_user(user_id, user_in)
    except ServiceException as exc:
        detail: str = f"User with id {user_id} not found in the system."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        ) from exc
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_id: Annotated[
        PositiveInt,
        Path(
            ...,
            title="User ID",
            annotation=PositiveInt,
            description="ID of the User to be searched",
            example=1,
        ),
    ],
) -> Response:
    """
    Delete an existing user given their user ID.
    ## Parameter:
    - `:param user_id:` **Unique identifier of the user to be deleted**
    - `:type user_id:` **PositiveInt**
    ## Response:
    - `:return:` **Json Response object with the deleted information**
    - `:rtype:` **Response**
    \f
    :param user_repository: Dependency method for user service layer
    :type user_repository: UserRepository
    """
    try:
        delete_result = user_repository.delete_user(user_id)
    except DatabaseException as exc:
        logger.error(f"Failed to delete user with ID {user_id}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        ) from exc
    response: Response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.headers["deleted"] = delete_result["deleted"].lower()
    response.headers["deleted_at"] = (
        delete_result["deleted_at"].isoformat()
        if delete_result["deleted_at"]
        else "null"
    )
    return response
