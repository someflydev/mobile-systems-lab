import 'package:flutter/foundation.dart';

class LabViewModel extends ChangeNotifier {
  // {{STATE_MODEL}}

  void loadConfig() {
    {{CONFIG_LOAD}}
  }

  void saveConfig() {
    {{CONFIG_SAVE}}
  }

  void requestPermissions() {
    {{PERMISSION_REQUEST}}
  }

  void startSensors() {
    {{SENSOR_SUBSCRIPTION}}
  }

  void backgroundPolicy() {
    {{BACKGROUND_BLOCK}}
  }
}
