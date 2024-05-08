"""
A module for openapi utils in the app.config package.
"""

import re
from typing import Any

import phonenumbers
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.config.exceptions import ServiceException
from app.config.settings import setting


def remove_tag_from_operation_id(tag: str, operation_id: str) -> str:
    """
    Remove tag from the operation ID
    :param tag: Tag to remove
    :type tag: str
    :param operation_id: Original operation ID
    :type operation_id: str
    :return: Updated operation ID
    :rtype: str
    """
    return operation_id.removeprefix(f"{tag}-")


def update_operation_id(operation: dict[str, Any]) -> None:
    """
    Update the operation ID of a single operation.
    :param operation: Operation object
    :type operation: dict[str, Any]
    :return: None
    :rtype: NoneType
    """
    if operation.get(
        "tags",
    ):
        tag: str = operation["tags"][0]
        operation_id: str = operation["operationId"]
        new_operation_id: str = remove_tag_from_operation_id(tag, operation_id)
        operation["operationId"] = new_operation_id


def modify_json_data(
    data: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Modify the JSON data
    :param data: JSON data to modify
    :type data: dict[str, Any]
    :return: Modified JSON data
    :rtype: dict[str, Any]
    """
    paths: dict[str, dict[str, dict[str, Any]]] | None = data.get("paths")
    if not paths:
        return data
    for key, path_data in paths.items():
        if key == "/":
            continue
        for operation in dict(path_data).values():
            update_operation_id(operation)
    return data


def custom_generate_unique_id(route: APIRoute) -> str:
    """
    Generate a custom unique ID for each route in API
    :param route: endpoint route
    :type route: APIRoute
    :return: new ID based on tag and route name
    :rtype: str
    """
    if route.name in (
        "redirect_to_docs",
        "check_health",
    ):
        return str(route.name)
    return f"{route.tags[0]}-{route.name}"


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """
    Generate a custom OpenAPI schema for the application.
    This function customizes the default FastAPI OpenAPI generation by
    incorporating additional configuration settings and modifying the schema.
    The modified schema is then cached for subsequent requests.
    :param app: FastAPI instance.
    :type app: FastAPI
    :return: Customized OpenAPI schema.
    :rtype: dict[str, Any]
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema: dict[str, dict[str, Any]] = get_openapi(
        title=app.state.init_settings.PROJECT_NAME,
        version=app.state.init_settings.VERSION,
        summary=app.state.init_settings.SUMMARY,
        description=app.state.init_settings.DESCRIPTION,
        routes=app.routes,
        servers=[
            {
                "url": app.state.auth_settings.SERVER_URL,
                "description": app.state.auth_settings.SERVER_DESCRIPTION,
            }
        ],
        contact=app.state.settings.CONTACT,
        license_info=app.state.init_settings.LICENSE_INFO,
    )
    openapi_schema = modify_json_data(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def validate_password(password: str | None) -> str:
    """
    Validates a password based on given criteria.
    :param password: The password to validate.
    :type password: Optional[str]
    :return: The validated password.
    :rtype: str
    """
    if not password:
        raise ServiceException("Password cannot be empty or None")
    if not (
        re.search("[A-Z]", password)
        and re.search("[a-z]", password)
        and re.search("[0-9]", password)
        and re.search(setting.DB_USER_PASSWORD_CONSTRAINT, password)
        and 8 <= len(password) <= 14
    ):
        raise ValueError("Password validation failed")
    return password


def validate_phone_number(
    phone_number: PhoneNumber | None,
) -> PhoneNumber | None:
    """
    Validate the phone number format
    :param phone_number: The phone number to validate
    :type phone_number: Optional[PhoneNumber]
    :return: The validated phone number
    :rtype: Optional[PhoneNumber]
    """
    if phone_number is None:
        return None
    try:
        parsed_number = phonenumbers.parse(str(phone_number), None)
    except phonenumbers.phonenumberutil.NumberParseException as exc:
        raise ValueError from exc
    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError("Invalid phone number")
    return phone_number
