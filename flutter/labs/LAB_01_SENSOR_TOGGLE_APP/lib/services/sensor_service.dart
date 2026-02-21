import 'dart:async';

import 'package:geolocator/geolocator.dart';
import 'package:sensors_plus/sensors_plus.dart';

class SensorService {
  StreamSubscription<AccelerometerEvent>? _accelerometerSub;
  StreamSubscription<Position>? _gpsSub;

  void startAccelerometer(void Function(String value) onData) {
    _accelerometerSub?.cancel();
    _accelerometerSub = accelerometerEventStream(samplingPeriod: SensorInterval.uiInterval)
        .listen((event) {
      onData('x=${event.x.toStringAsFixed(2)} y=${event.y.toStringAsFixed(2)} z=${event.z.toStringAsFixed(2)}');
    });
  }

  void stopAccelerometer() {
    _accelerometerSub?.cancel();
    _accelerometerSub = null;
  }

  void startGps(void Function(String value) onData) {
    _gpsSub?.cancel();
    _gpsSub = Geolocator.getPositionStream(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.best,
        distanceFilter: 1,
      ),
    ).listen((position) {
      onData('lat=${position.latitude.toStringAsFixed(5)} lon=${position.longitude.toStringAsFixed(5)} +/-${position.accuracy.toStringAsFixed(1)}m');
    });
  }

  void stopGps() {
    _gpsSub?.cancel();
    _gpsSub = null;
  }

  void stopAll() {
    stopAccelerometer();
    stopGps();
  }
}
