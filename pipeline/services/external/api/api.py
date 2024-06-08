"""
A module for api in the pipeline.services.external.api package.
"""

import logging
import time
from typing import Any, Optional, Type, Union

import requests
from pydantic import NonNegativeInt, TypeAdapter
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from pipeline.config.settings import Settings
from pipeline.core.decorators import benchmark, with_logging
from pipeline.exceptions.exceptions import (
    APIValidationError,
    NoAPIResponseException,
)
from pipeline.schemas.api.weather import T

logger: logging.Logger = logging.getLogger(__name__)


class ApiService:
    """
    The class that provides the API service for interaction with its endpoints.
    """

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        self.settings: Settings = settings
        self.last_request_time: float = time.time()
        self.request_count: NonNegativeInt = 0
        self.session: requests.Session = self._initialize_session()

    @with_logging
    def _initialize_session(
        self,
    ) -> requests.Session:
        """
        Initializes a requests Session and configures it with a custom HTTP
         adapter.
        """
        session: requests.Session = requests.Session()
        adapter: HTTPAdapter = self._configure_http_adapter()
        session.mount(self.settings.PREFIX, adapter)
        return session

    @with_logging
    def _configure_http_adapter(
        self,
    ) -> HTTPAdapter:
        """
        Configures and returns a custom HTTP adapter for the session, based
         on settings.
        """
        retries: Retry = Retry(
            total=self.settings.MAX_RETRIES,
            backoff_factor=self.settings.RETRY_BACKOFF_FACTOR,
            backoff_max=self.settings.BACKOFF_MAX,
            status_forcelist=self.settings.RETRY_STATUS_FORCE_LIST,
        )
        adapter: HTTPAdapter = HTTPAdapter(
            pool_connections=self.settings.POOL_CONNECTIONS,
            pool_maxsize=self.settings.POOL_MAXSIZE,
            max_retries=retries,
        )
        return adapter

    @with_logging
    @benchmark
    def _ensure_rate_limit(
        self,
    ) -> None:
        if self.request_count >= self.settings.RATE_LIMIT_THRESHOLD:
            time_elapsed = time.time() - self.last_request_time
            if time_elapsed < self.settings.RATE_LIMIT_RESET_TIME:
                time.sleep(self.settings.RATE_LIMIT_RESET_TIME - time_elapsed)
            self.last_request_time = time.time()
            self.request_count = 0
        self.request_count += 1

    @benchmark
    def _api_call(
        self,
        endpoint: str,
        response_model: Type[T],
        method: str = "GET",
        params: Optional[dict[str, Union[str, int]]] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> T:
        """
        Perform an API call with rate limit checking.
        :param method: The HTTP method for the API call (e.g., "GET", "POST").
        :type method: str
        :param endpoint: The API endpoint to call.
        :type endpoint: str
        :param params: Query parameters to include in the request.
        :type params: Optional[dict[str, Union[str, int]]]
        :param data: JSON data to include in the request body.
        :type data: Optional[dict[str, Any]]
        :param headers: Additional headers to include in the request.
        :type headers: Optional[dict[str, str]]
        :return: The API response data.
        :rtype: dict[str, Union[dict[str,
         Union[dict[str, Any], list[dict[str, Any]]]], Any]]
        """
        self._ensure_rate_limit()
        url: str = (
            f"{self.settings.API_URL}{endpoint}"
            f"{self.settings.ID_PATH_PARAMETER}{self.settings.API_KEY}"
        )
        try:
            response: Response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=data,
            )
            response.raise_for_status()
            type_adapter: TypeAdapter[T] = TypeAdapter(response_model)
            print(response.json())
            print(type(response.json()))
            model_instance: T = type_adapter.validate_python(response.json())
            if hasattr(model_instance, "meta") and model_instance.meta is None:
                logger.warning("Expected pagination data missing in response")
            return model_instance
        except requests.exceptions.RequestException as exc:
            if exc.response is None:
                raise NoAPIResponseException(
                    "No response received from the API"
                ) from exc
            try:
                error_data = exc.response.json()
            except ValueError as e:
                raise APIValidationError(
                    [
                        {
                            "loc": ["response"],
                            "msg": "Invalid JSON response",
                            "type": "value_error.json",
                        }
                    ]
                ) from e
            raise APIValidationError(error_data) from exc
