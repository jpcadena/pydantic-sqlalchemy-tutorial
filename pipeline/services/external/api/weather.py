"""
A module for weather API interactions in the pipeline.services.external.api
 package.
"""

from pydantic_extra_types.coordinate import Latitude, Longitude

from pipeline.core.decorators import with_logging
from pipeline.schemas.api.weather import APIWeather
from pipeline.services.external.api.api import ApiService


class WeatherApiService(ApiService):
    """
    The class that provides the weather API service for interaction with its
     endpoints.
    """

    @with_logging
    def get_weather_data(
        self,
        lat: Latitude | None = None,
        lng: Longitude | None = None,
        units: str = "metric",
    ) -> APIWeather:
        """
        Retrieves the weather data for a given location.
        :param lat: The latitude for which to retrieve the weather data.
        :type lat: Optional[Latitude]
        :param lng: The longitude for which to retrieve the weather data.
        :type lng: Optional[Longitude]
        :param units: The units of measurement (default: metric).
        :type units: str
        :return: The weather data for the specified location.
        :rtype: APIWeatherModel
        """
        latitude: Latitude = lat or self.settings.DEFAULT_LAT
        longitude: Longitude = lng or self.settings.DEFAULT_LNG
        endpoint = f"{latitude}{self.settings.PATH_PARAMETER}{longitude}"
        params: dict[str, str | int] = {
            "units": units,
        }
        weather_data: APIWeather = self._api_call(
            endpoint=endpoint,
            response_model=APIWeather,
            method="GET",
            params=params,
        )
        return weather_data
