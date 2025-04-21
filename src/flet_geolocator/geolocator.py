import asyncio
from typing import Optional

import flet as ft

from .types import *

__all__ = ["Geolocator"]


@ft.control("Geolocator")
class Geolocator(ft.Service):
    """
    A control that allows you to fetch GPS data from your device.
    This control is non-visual and should be added to `page.overlay` list.

    -----

    Online docs: https://flet.dev/docs/controls/geolocator
    """

    location_settings: Optional[GeolocatorSettings] = None
    on_position_change: ft.OptionalEventCallable[GeolocatorPositionChangeEvent] = None
    on_error: ft.OptionalControlEventCallable = None

    async def get_current_position_async(
        self,
        accuracy: GeolocatorPositionAccuracy = GeolocatorPositionAccuracy.BEST,
        location_settings: Optional[GeolocatorSettings] = None,
    ) -> GeolocatorPosition:
        r = await self._invoke_method_async(
            method_name="get_current_position",
            arguments={
                "location_settings": (
                    location_settings
                    or self.location_settings
                    or GeolocatorSettings(accuracy=accuracy)
                )
            },
        )
        return GeolocatorPosition(**r)

    async def get_last_known_position_async(self) -> GeolocatorPosition:
        assert not self.page.web, "get_last_known_position is not supported on web"
        r = await self._invoke_method_async("get_last_known_position")
        return GeolocatorPosition(**r)

    async def get_permission_status_async(self) -> GeolocatorPermissionStatus:
        r = await self._invoke_method_async("get_permission_status")
        return GeolocatorPermissionStatus(r)

    async def request_permission_async(self) -> GeolocatorPermissionStatus:
        r = await self._invoke_method_async("request_permission")
        return GeolocatorPermissionStatus(r)

    async def is_location_service_enabled_async(self) -> bool:
        return await self._invoke_method_async("is_location_service_enabled")

    def open_app_settings(self):
        asyncio.create_task(self.open_app_settings_async())

    async def open_app_settings_async(self):
        assert not self.page.web, "open_app_settings is not supported on web"
        await self._invoke_method_async("open_app_settings")

    def open_location_settings(self):
        asyncio.create_task(self.open_location_settings_async())

    async def open_location_settings_async(self):
        assert not self.page.web, "open_location_settings is not supported on web"
        await self._invoke_method_async("open_location_settings")
