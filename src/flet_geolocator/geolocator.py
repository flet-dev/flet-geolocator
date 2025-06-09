import asyncio
from typing import Optional

import flet as ft

from .types import (
    GeolocatorConfiguration,
    GeolocatorPermissionStatus,
    GeolocatorPosition,
    GeolocatorPositionAccuracy,
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

    on_position_change: ft.OptionalEventCallable[GeolocatorPositionChangeEvent] = None
    """
    Fires when the position of the device changes.

    Event handler argument is of type [`GeolocatorPositionChangeEvent`][(p).types.].
    """

    on_error: ft.OptionalControlEventCallable = None
    """
    Fires when an error occurs.
    
    The `data` property of the event handler argument contains information on the error. 
    """

    async def get_current_position_async(
        self,
        configuration: Optional[GeolocatorConfiguration],
    ) -> GeolocatorPosition:
        """
        Gets the current position of the device with the desired accuracy and settings.

        Args:
            configuration: Additional configuration for the location request.
                If not specified, then the [`Geolocator.configuration`][...] property is used.
        Returns:
            The current position of the device as a [`GeolocatorPosition`][(p).types.].

        Note:
            Depending on the availability of different location services, this can take several seconds.
            It is recommended to call the [`get_last_known_position`][..] method first to receive a
            known/cached position and update it with the result of the [`get_current_position`][..] method.
        """
        s = (
            configuration
            or self.configuration
            or GeolocatorConfiguration(accuracy=GeolocatorPositionAccuracy.BEST)
        )
        r = await self._invoke_method_async(
            method_name="get_current_position",
            arguments={"configuration": s},
        )
        return GeolocatorPosition(**r)

    async def get_last_known_position_async(
        self, timeout: float = 10
    ) -> GeolocatorPosition:
        """
        Gets the last known position stored on the user's device.
        The accuracy can be defined using the [`Geolocator.configuration`][...] property.

        Not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Raises:
            AssertionError: If called on a web page, as this method is not supported on web.
            TimeoutError: If the request times out.

        Returns:
            `True` if the app's settings were opened successfully, `False` otherwise.
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

        Raises:
            TimeoutError: If the request times out.

        Returns:
            The status of the permission.
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

        Raises:
            TimeoutError: If the request times out.

        Returns:
            The status of the permission request.
        """
        r = await self._invoke_method_async("request_permission", timeout=timeout)
        return GeolocatorPermissionStatus(r)

    async def is_location_service_enabled_async(self, timeout: float = 10) -> bool:
        """
        Checks if location service is enabled.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Raises:
            TimeoutError: If the request times out.

        Returns:
            `True` if location service is enabled, `False` otherwise.
        """
        return await self._invoke_method_async(
            "is_location_service_enabled", timeout=timeout
        )

    def open_app_settings(self, timeout: float = 10):
        """
        Attempts to open the app's settings.

        Not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Raises:
            AssertionError: If called on a web page, as this method is not supported on web.
            TimeoutError: If the request times out.

        Returns:
            `True` if the app's settings were opened successfully, `False` otherwise.
        """
        asyncio.create_task(self.open_app_settings_async(timeout=timeout))

    async def open_app_settings_async(self, timeout: float = 10):
        """
        Attempts to open the app's settings.

        Not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Raises:
            AssertionError: If called on a web page, as this method is not supported on web.
            TimeoutError: If the request times out.

        Returns:
            `True` if the app's settings were opened successfully, `False` otherwise.
        """
        assert not self.page.web, "open_app_settings is not supported on web"
        await self._invoke_method_async("open_app_settings", timeout=timeout)

    def open_location_settings(self, timeout: float = 10):
        """
        Attempts to open the device's location settings.

        Not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Raises:
            AssertionError: If called on a web page, as this method is not supported on web.
            TimeoutError: If the request times out.

        Returns:
            `True` if the device's settings were opened successfully, `False` otherwise.
        """
        asyncio.create_task(self.open_location_settings_async(timeout=timeout))

    async def open_location_settings_async(self, timeout: float = 10):
        """
        Attempts to open the device's location settings.

        Not supported on web plaform.

        Args:
            timeout: The maximum amount of time (in seconds) to wait for a response.

        Raises:
            AssertionError: If called on a web page, as this method is not supported on web.
            TimeoutError: If the request times out.

        Returns:
            `True` if the device's settings were opened successfully, `False` otherwise.
        """
        assert not self.page.web, "open_location_settings is not supported on web"
        await self._invoke_method_async("open_location_settings", timeout=timeout)
