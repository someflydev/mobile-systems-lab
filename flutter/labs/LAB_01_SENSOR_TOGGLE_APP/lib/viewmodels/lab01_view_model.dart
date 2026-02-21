import 'package:flutter/foundation.dart';

import '../models/lab_config.dart';
import '../services/config_service.dart';
import '../services/permission_service.dart';
import '../services/sensor_service.dart';

class Lab01ViewModel extends ChangeNotifier {
  final ConfigService _configService;
  final PermissionService _permissionService;
  final SensorService _sensorService;

  LabConfig config = LabConfig.fallback;
  String accelerometerValue = 'disabled';
  String gpsValue = 'disabled';
  String status = 'loading';
  bool _isForeground = true;

  Lab01ViewModel(
    this._configService,
    this._permissionService,
    this._sensorService,
  );

  Future<void> initialize() async {
    config = await _configService.loadConfig();
    status = 'ready';
    await _syncSensors();
    notifyListeners();
  }

  void onLifecycleForeground(bool foreground) {
    _isForeground = foreground;
    _syncSensors();
    notifyListeners();
  }

  Future<void> setAccelerometerEnabled(bool enabled) async {
    config = config.copyWith(
      featureFlags: config.featureFlags.copyWith(accelerometerEnabled: enabled),
    );
    await _configService.persistConfig(config);
    await _syncSensors();
    notifyListeners();
  }

  Future<void> setGpsEnabled(bool enabled) async {
    config = config.copyWith(
      featureFlags: config.featureFlags.copyWith(gpsEnabled: enabled),
    );
    await _configService.persistConfig(config);
    await _syncSensors();
    notifyListeners();
  }

  Future<void> exportConfig() async {
    final path = await _configService.exportConfig(config);
    status = 'config exported: $path';
    notifyListeners();
  }

  Future<void> importConfig() async {
    try {
      config = await _configService.importConfig();
      status = 'config imported';
      await _syncSensors();
    } catch (e) {
      status = 'import failed: $e';
    }
    notifyListeners();
  }

  Future<void> _syncSensors() async {
    _sensorService.stopAll();

    if (!_isForeground) {
      accelerometerValue = 'paused (background)';
      gpsValue = 'paused (background)';
      return;
    }

    if (config.featureFlags.accelerometerEnabled) {
      _sensorService.startAccelerometer((value) {
        accelerometerValue = value;
        if (config.featureFlags.logSensorData) status = 'accelerometer updated';
        notifyListeners();
      });
    } else {
      accelerometerValue = 'disabled';
    }

    if (config.featureFlags.gpsEnabled) {
      final granted = await _permissionService.ensureLocationPermission();
      if (!granted) {
        gpsValue = 'permission required';
        status = 'location permission denied';
        return;
      }
      _sensorService.startGps((value) {
        gpsValue = value;
        if (config.featureFlags.logSensorData) status = 'gps updated';
        notifyListeners();
      });
    } else {
      gpsValue = 'disabled';
    }
  }

  @override
  void dispose() {
    _sensorService.stopAll();
    super.dispose();
  }
}
