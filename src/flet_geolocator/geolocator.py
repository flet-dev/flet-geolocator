import asyncio
from dataclasses import field
from typing import Optional

import flet as ft

from .types import (
    GeolocatorConfiguration,
    GeolocatorPermissionStatus,
    GeolocatorPosition,
    GeolocatorPositionChangeEvent,
)

__all__ = ["Geolocator"]


@ft.control("Geolocator")
class Geolocator(ft.Service):
    """
    A control that allows you to fetch GPS data from your device.

    This control is non-visual and should be added to `page.overlay` list.
    """

    configuration: Optional[GeolocatorConfiguration] = None
    """
    Some additional configuration.
    """

    on_position_change: ft.OptionalEventHandler[
        GeolocatorPositionChangeEvent["Geolocator"]
    ] = None
    """
    Fires when the position of the device changes.

    Event handler argument is of type [`GeolocatorPositionChangeEvent`][(p).].
    """

    on_error: ft.OptionalControlEventHandler["Geolocator"] = None
    """
    Fires when an error occurs.
    
    The `data` property of the event handler argument contains information on the error. 
    """

    position: Optional[GeolocatorPosition] = field(default=None, init=False)  # todo: make this property readonly
    """
    The current position of the device. (read-only)

    Starts as `None` and will be updated when the position changes.
    """

    async def get_current_position_async(
        self,
        configuration: Optional[GeolocatorConfiguration] = None,
        timeout: float = 30,
    ) -> GeolocatorPosition:
        """
        Gets the current position of the device with the desired accuracy and settings.

        Args:
            configuration: Additional configuration for the location request.
                If not specified, then the [`Geolocator.configuration`][(p).] property is used.
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            The current position of the device as a [`GeolocatorPosition`][(p).].
        Raises:
            TimeoutError: If the request times out.

        Note:
            Depending on the availability of different location services, this can take several seconds.
            It is recommended to call the [`get_last_known_position`][..] method first to receive a
            known/cached position and update it with the result of the [`get_current_position`][..] method.
        """
        r = await self._invoke_method_async(
            method_name="get_current_position",
            arguments={"configuration": configuration or self.configuration},
            timeout=timeout,
        )
        return GeolocatorPosition(**r)

    async def get_last_known_position_async(
        self, timeout: float = 10
    ) -> GeolocatorPosition:
        """
        Gets the last known position stored on the user's device.
        The accuracy can be defined using the [`Geolocator.configuration`][(p).] property.

        Note:
            This method is not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the app's settings were opened successfully, `False` otherwise.
        Raises:
            AssertionError: If invoked on a web platform.
            TimeoutError: If the request times out.
        """
        assert not self.page.web, "get_last_known_position is not supported on web"
        r = await self._invoke_method_async("get_last_known_position", timeout=timeout)
        return GeolocatorPosition(**r)

    async def get_permission_status_async(
        self, timeout: float = 10
    ) -> GeolocatorPermissionStatus:
        """
        Gets which permission the app has been granted to access the device's location.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            The status of the permission.
        Raises:
            TimeoutError: If the request times out.
        """
        r = await self._invoke_method_async("get_permission_status", timeout=timeout)
        return GeolocatorPermissionStatus(r)

    async def request_permission_async(
        self, timeout: int = 60
    ) -> GeolocatorPermissionStatus:
        """
        Requests the device for access to the device's location.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            The status of the permission request.
        Raises:
            TimeoutError: If the request times out.
        """
        r = await self._invoke_method_async("request_permission", timeout=timeout)
        return GeolocatorPermissionStatus(r)

    async def is_location_service_enabled_async(self, timeout: float = 10) -> bool:
        """
        Checks if location service is enabled.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if location service is enabled, `False` otherwise.
        Raises:
            TimeoutError: If the request times out.
        """
        return await self._invoke_method_async(
            "is_location_service_enabled", timeout=timeout
        )

    async def open_app_settings_async(self, timeout: float = 10) -> bool:
        """
        Attempts to open the app's settings.

        Note:
            This method is not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the app's settings were opened successfully, `False` otherwise.
        Raises:
            AssertionError: If invoked on a web platform.
            TimeoutError: If the request times out.
        """
        assert not self.page.web, "open_app_settings is not supported on web"
        return await self._invoke_method_async("open_app_settings", timeout=timeout)

    def open_location_settings(self, timeout: float = 10):
        """
        Attempts to open the device's location settings.

        Note:
            This method is not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the device's settings were opened successfully, `False` otherwise.
        Raises:
            AssertionError: If invoked on a web platform.
            TimeoutError: If the request times out.
        """
        asyncio.create_task(self.open_location_settings_async(timeout=timeout))

    async def open_location_settings_async(self, timeout: float = 10):
        """
        Attempts to open the device's location settings.

        Note:
            This method is not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            `True` if the device's settings were opened successfully, `False` otherwise.
        Raises:
            AssertionError: If invoked on a web platform.
            TimeoutError: If the request times out.
        """
        assert not self.page.web, "open_location_settings is not supported on web"
        await self._invoke_method_async("open_location_settings", timeout=timeout)

    async def distance_between_async(
        self,
        start_latitude: ft.Number,
        start_longitude: ft.Number,
        end_latitude: ft.Number,
        end_longitude: ft.Number,
        timeout: float = 10,
    ):
        """
        Calculates the distance between the supplied coordinates in meters.

        The distance between the coordinates is calculated using the
        Haversine formula (see https://en.wikipedia.org/wiki/Haversine_formula).

        Args:
            start_latitude: The latitude of the starting point, in degrees.
            start_longitude: The longitude of the starting point, in degrees.
            end_latitude: The latitude of the ending point, in degrees.
            end_longitude: The longitude of the ending point, in degrees.
            timeout: The maximum amount of time (in seconds) to wait for a response.
        Returns:
            The distance between the coordinates in meters.
        Raises:
            TimeoutError: If the request times out.
        """
        await self._invoke_method_async(
            method_name="distance_between",
            arguments={
                "start_latitude": start_latitude,
                "start_longitude": start_longitude,
                "end_latitude": end_latitude,
                "end_longitude": end_longitude,
            },
            timeout=timeout,
        )
