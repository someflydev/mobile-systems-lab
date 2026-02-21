import 'dart:convert';

class LabConfig {
  final int version;
  final String appTitle;
  final FeatureFlags featureFlags;

  const LabConfig({
    required this.version,
    required this.appTitle,
    required this.featureFlags,
  });

  static const fallback = LabConfig(
    version: 1,
    appTitle: 'LAB_01 Sensor Toggle App',
    featureFlags: FeatureFlags(
      accelerometerEnabled: false,
      gpsEnabled: false,
      darkMode: false,
      logSensorData: true,
    ),
  );

  factory LabConfig.fromJson(Map<String, dynamic> json) {
    return LabConfig(
      version: (json['version'] as num?)?.toInt() ?? 1,
      appTitle: json['app_title'] as String? ?? fallback.appTitle,
      featureFlags: FeatureFlags.fromJson(
          json['feature_flags'] as Map<String, dynamic>? ?? const {}),
    );
  }

  Map<String, dynamic> toJson() => {
        'version': version,
        'app_title': appTitle,
        'feature_flags': featureFlags.toJson(),
      };

  LabConfig copyWith({FeatureFlags? featureFlags}) {
    return LabConfig(
      version: version,
      appTitle: appTitle,
      featureFlags: featureFlags ?? this.featureFlags,
    );
  }

  String encodePretty() => const JsonEncoder.withIndent('  ').convert(toJson());
}

class FeatureFlags {
  final bool accelerometerEnabled;
  final bool gpsEnabled;
  final bool darkMode;
  final bool logSensorData;

  const FeatureFlags({
    required this.accelerometerEnabled,
    required this.gpsEnabled,
    required this.darkMode,
    required this.logSensorData,
  });

  factory FeatureFlags.fromJson(Map<String, dynamic> json) {
    return FeatureFlags(
      accelerometerEnabled: json['accelerometer_enabled'] as bool? ?? false,
      gpsEnabled: json['gps_enabled'] as bool? ?? false,
      darkMode: json['dark_mode'] as bool? ?? false,
      logSensorData: json['log_sensor_data'] as bool? ?? true,
    );
  }

  Map<String, dynamic> toJson() => {
        'accelerometer_enabled': accelerometerEnabled,
        'gps_enabled': gpsEnabled,
        'dark_mode': darkMode,
        'log_sensor_data': logSensorData,
      };

  FeatureFlags copyWith({bool? accelerometerEnabled, bool? gpsEnabled}) {
    return FeatureFlags(
      accelerometerEnabled: accelerometerEnabled ?? this.accelerometerEnabled,
      gpsEnabled: gpsEnabled ?? this.gpsEnabled,
      darkMode: darkMode,
      logSensorData: logSensorData,
    );
  }
}
