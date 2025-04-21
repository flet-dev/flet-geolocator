import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

import 'utils/geolocator.dart';

class GeolocatorService extends FletService {
  GeolocatorService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("Geolocator(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
    if (control.getBool("on_position_change", false)!) {
      _onPositionChangedSubscription = Geolocator.getPositionStream(
        locationSettings: parseLocationSettings(
            control.get("location_settings"), Theme.of(context)),
      ).listen(
        (Position? newPosition) {
          if (newPosition != null) {
            _onPositionChange(newPosition);
            debugPrint('Geolocator - $newPosition');
          } else {
            debugPrint('Geolocator: Position is null.');
          }
        },
        onError: (Object error, StackTrace stackTrace) {
          debugPrint('Geolocator Error getting stream position: $error');
          control.triggerEvent("error", error.toString());
        },
        onDone: () {
          debugPrint('Geolocator: Done getting stream position.');
        },
      );
    }
  }

  void _onPositionChange(Position position) {
    control.triggerEvent("position_change", {
      "latitude": position.latitude,
      "longitude": position.longitude,
    });
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Geolocator.$name($args)");
    switch (name) {
      case "request_permission":
        var permission = await Geolocator.requestPermission();
        return permission.name;
      case "get_permission_status":
        var permission = await Geolocator.checkPermission();
        return permission.name;
      case "is_location_service_enabled":
        var serviceEnabled = await Geolocator.isLocationServiceEnabled();
        return serviceEnabled;
      case "open_app_settings":
        if (!kIsWeb) {
          await Geolocator.openAppSettings();
        }
        break;
      case "open_location_settings":
        if (!kIsWeb) {
          await Geolocator.openLocationSettings();
        }
        break;
      case "get_last_known_position":
        if (!kIsWeb) {
          Position? position = await Geolocator.getLastKnownPosition();
          return positionAsMap(position);
        }
        break;
      case "get_current_position":
        Position currentPosition = await Geolocator.getCurrentPosition(
          locationSettings: parseLocationSettings(
              args["location_settings"], Theme.of(context)),
        );
        return positionAsMap(currentPosition)!;
      default:
        throw Exception("Unknown Geolocator method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("Geolocator(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _onPositionChangedSubscription?.cancel();
    super.dispose();
  }
}
