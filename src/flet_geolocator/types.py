import datetime
from dataclasses import dataclass, field
from enum import Enum

import flet as ft

__all__ = [
    "GeolocatorPositionAccuracy",
    "GeolocatorPermissionStatus",
    "GeolocatorActivityType",
    "GeolocatorPosition",
    "GeolocatorSettings",
    "GeolocatorWebSettings",
    "GeolocatorAppleSettings",
    "GeolocatorAndroidSettings",
    "GeolocatorPositionChangeEvent",
]


class GeolocatorPositionAccuracy(Enum):
    LOWEST = "lowest"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BEST = "best"
    BEST_FOR_NAVIGATION = "bestForNavigation"
    REDUCED = "reduced"


class GeolocatorPermissionStatus(Enum):
    DENIED = "denied"
    DENIED_FOREVER = "deniedForever"
    WHILE_IN_USE = "whileInUse"
    ALWAYS = "always"
    UNABLE_TO_DETERMINE = "unableToDetermine"


class GeolocatorActivityType(Enum):
    AUTOMOTIVE_NAVIGATION = "automotiveNavigation"
    FITNESS = "fitness"
    OTHER_NAVIGATION = "otherNavigation"
    AIRBORNE = "airborne"
    OTHER = "other"


@dataclass
class GeolocatorPosition:
    latitude: ft.OptionalNumber = None
    longitude: ft.OptionalNumber = None
    speed: ft.OptionalNumber = None
    altitude: ft.OptionalNumber = None
    timestamp: datetime.datetime = None
    accuracy: ft.OptionalNumber = None
    altitude_accuracy: ft.OptionalNumber = None
    heading: ft.OptionalNumber = None
    heading_accuracy: ft.OptionalNumber = None
    speed_accuracy: ft.OptionalNumber = None
    floor: ft.OptionalInt = None
    is_mocked: ft.OptionalBool = None


@dataclass
class GeolocatorSettings:
    accuracy: GeolocatorPositionAccuracy = GeolocatorPositionAccuracy.BEST
    distance_filter: int = 0
    time_limit: ft.DurationValue = None


@dataclass
class GeolocatorWebSettings(GeolocatorSettings):
    maximum_age: ft.DurationValue = field(default_factory=ft.Duration)


@dataclass
class GeolocatorAppleSettings(GeolocatorSettings):
    activity_type: GeolocatorActivityType = GeolocatorActivityType.OTHER
    pause_location_updates_automatically: bool = False
    show_background_location_indicator: bool = False
    allow_background_location_updates: bool = True


@dataclass
class GeolocatorAndroidSettings(GeolocatorSettings):
    force_location_manager: bool = False
    interval_duration: ft.DurationValue = None
    foreground_notification_text: ft.OptionalString = None
    foreground_notification_title: ft.OptionalString = None
    foreground_notification_channel_name: str = "Background Location"
    foreground_notification_enable_wake_lock: bool = False
    foreground_notification_enable_wifi_lock: bool = False
    foreground_notification_set_ongoing: bool = False
    foreground_notification_color: ft.OptionalColorValue = None


class GeolocatorPositionChangeEvent(ft.ControlEvent):
    latitude: float
    longitude: float
