import 'dart:convert';
import 'dart:io';

import 'package:flutter/services.dart' show rootBundle;
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/lab_config.dart';

class ConfigService {
  static const _localFileName = 'config.json';
  static const _exportFileName = 'lab01-config-export.json';

  Future<LabConfig> loadConfig() async {
    final local = await _readLocalOrAsset();
    final parsed = LabConfig.fromJson(jsonDecode(local) as Map<String, dynamic>);
    final prefs = await SharedPreferences.getInstance();

    return parsed.copyWith(
      featureFlags: parsed.featureFlags.copyWith(
        accelerometerEnabled:
            prefs.getBool('accelerometer_enabled') ?? parsed.featureFlags.accelerometerEnabled,
        gpsEnabled: prefs.getBool('gps_enabled') ?? parsed.featureFlags.gpsEnabled,
      ),
    );
  }

  Future<void> persistConfig(LabConfig config) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('accelerometer_enabled', config.featureFlags.accelerometerEnabled);
    await prefs.setBool('gps_enabled', config.featureFlags.gpsEnabled);

    final file = await _localFile();
    await file.writeAsString(config.encodePretty(), flush: true);
  }

  Future<String> exportConfig(LabConfig config) async {
    final dir = await getApplicationDocumentsDirectory();
    final file = File('${dir.path}/$_exportFileName');
    await file.writeAsString(config.encodePretty(), flush: true);
    return file.path;
  }

  Future<LabConfig> importConfig() async {
    final dir = await getApplicationDocumentsDirectory();
    final file = File('${dir.path}/$_exportFileName');
    if (!await file.exists()) {
      throw Exception('No exported config found at ${file.path}');
    }

    final payload = await file.readAsString();
    final config = LabConfig.fromJson(jsonDecode(payload) as Map<String, dynamic>);
    if (config.version != 1) {
      throw Exception('Unsupported config version: ${config.version}');
    }
    await persistConfig(config);
    return config;
  }

  Future<String> _readLocalOrAsset() async {
    final local = await _localFile();
    if (await local.exists()) {
      return local.readAsString();
    }
    return rootBundle.loadString('assets/config.json');
  }

  Future<File> _localFile() async {
    final dir = await getApplicationDocumentsDirectory();
    return File('${dir.path}/$_localFileName');
  }
}
