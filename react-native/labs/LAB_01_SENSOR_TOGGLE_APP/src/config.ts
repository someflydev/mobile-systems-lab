import AsyncStorage from '@react-native-async-storage/async-storage';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';

export type LabConfig = {
  version: number;
  app_title: string;
  feature_flags: {
    accelerometer_enabled: boolean;
    gps_enabled: boolean;
    dark_mode: boolean;
    log_sensor_data: boolean;
  };
};

const DEFAULT_CONFIG: LabConfig = require('../assets/config.json');
const LOCAL_CONFIG = `${FileSystem.documentDirectory}config.json`;
const EXPORT_CONFIG = `${FileSystem.documentDirectory}lab01-config-export.json`;

export async function loadConfig(): Promise<LabConfig> {
  const info = await FileSystem.getInfoAsync(LOCAL_CONFIG);
  const raw = info.exists
    ? await FileSystem.readAsStringAsync(LOCAL_CONFIG)
    : JSON.stringify(DEFAULT_CONFIG);
  const parsed = JSON.parse(raw) as LabConfig;

  const accelOverride = await AsyncStorage.getItem('accelerometer_enabled');
  const gpsOverride = await AsyncStorage.getItem('gps_enabled');

  return {
    ...parsed,
    feature_flags: {
      ...parsed.feature_flags,
      accelerometer_enabled:
        accelOverride == null
          ? parsed.feature_flags.accelerometer_enabled
          : accelOverride === 'true',
      gps_enabled:
        gpsOverride == null ? parsed.feature_flags.gps_enabled : gpsOverride === 'true'
    }
  };
}

export async function persistConfig(config: LabConfig): Promise<void> {
  await AsyncStorage.setItem(
    'accelerometer_enabled',
    String(config.feature_flags.accelerometer_enabled)
  );
  await AsyncStorage.setItem('gps_enabled', String(config.feature_flags.gps_enabled));
  await FileSystem.writeAsStringAsync(LOCAL_CONFIG, JSON.stringify(config, null, 2));
}

export async function exportConfig(config: LabConfig): Promise<string> {
  await FileSystem.writeAsStringAsync(EXPORT_CONFIG, JSON.stringify(config, null, 2));
  return EXPORT_CONFIG;
}

export async function importConfig(): Promise<LabConfig> {
  const picked = await DocumentPicker.getDocumentAsync({
    type: 'application/json',
    copyToCacheDirectory: true,
    multiple: false
  });

  if (picked.canceled) {
    throw new Error('Import cancelled');
  }

  const uri = picked.assets[0]?.uri;
  if (!uri) {
    throw new Error('No file selected');
  }

  const raw = await FileSystem.readAsStringAsync(uri);
  const parsed = JSON.parse(raw) as LabConfig;
  if (parsed.version !== 1) {
    throw new Error(`Unsupported config version: ${parsed.version}`);
  }
  await persistConfig(parsed);
  return parsed;
}
