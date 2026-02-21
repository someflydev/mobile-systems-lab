import { useEffect, useRef, useState } from 'react';
import {
  AppState,
  Button,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  View
} from 'react-native';

import {
  type LabConfig,
  exportConfig,
  importConfig,
  loadConfig,
  persistConfig
} from './src/config';
import { ensureLocationPermission } from './src/permissions';
import { startAccelerometer, startGps } from './src/sensors';

const fallback: LabConfig = {
  version: 1,
  app_title: 'LAB_01 Sensor Toggle App',
  feature_flags: {
    accelerometer_enabled: false,
    gps_enabled: false,
    dark_mode: false,
    log_sensor_data: true
  }
};

export default function App() {
  const [config, setConfig] = useState<LabConfig>(fallback);
  const [accelValue, setAccelValue] = useState('disabled');
  const [gpsValue, setGpsValue] = useState('disabled');
  const [status, setStatus] = useState('loading');
  const [foreground, setForeground] = useState(true);

  const stopAccelRef = useRef<(() => void) | null>(null);
  const stopGpsRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    loadConfig()
      .then((cfg) => {
        setConfig(cfg);
        setStatus('ready');
      })
      .catch((e) => setStatus(`config load failed: ${String(e)}`));
  }, []);

  useEffect(() => {
    const sub = AppState.addEventListener('change', (nextState) => {
      setForeground(nextState === 'active');
    });
    return () => sub.remove();
  }, []);

  useEffect(() => {
    void syncSensors();
    return () => {
      stopAccelRef.current?.();
      stopGpsRef.current?.();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [config.feature_flags.accelerometer_enabled, config.feature_flags.gps_enabled, foreground]);

  const syncSensors = async () => {
    stopAccelRef.current?.();
    stopGpsRef.current?.();
    stopAccelRef.current = null;
    stopGpsRef.current = null;

    if (!foreground) {
      setAccelValue('paused (background)');
      setGpsValue('paused (background)');
      return;
    }

    if (config.feature_flags.accelerometer_enabled) {
      stopAccelRef.current = startAccelerometer((value) => {
        setAccelValue(value);
        if (config.feature_flags.log_sensor_data) setStatus('accelerometer updated');
      });
    } else {
      setAccelValue('disabled');
    }

    if (config.feature_flags.gps_enabled) {
      const granted = await ensureLocationPermission();
      if (!granted) {
        setGpsValue('permission required');
        setStatus('location permission denied');
        return;
      }
      stopGpsRef.current = await startGps((value) => {
        setGpsValue(value);
        if (config.feature_flags.log_sensor_data) setStatus('gps updated');
      });
    } else {
      setGpsValue('disabled');
    }
  };

  const updateConfig = async (next: LabConfig) => {
    setConfig(next);
    await persistConfig(next);
  };

  return (
    <SafeAreaView style={styles.root}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>{config.app_title}</Text>

        <RowSwitch
          label="Accelerometer"
          value={config.feature_flags.accelerometer_enabled}
          onChange={(value) =>
            void updateConfig({
              ...config,
              feature_flags: { ...config.feature_flags, accelerometer_enabled: value }
            })
          }
        />
        <Text style={styles.value}>Accelerometer data: {accelValue}</Text>

        <RowSwitch
          label="GPS"
          value={config.feature_flags.gps_enabled}
          onChange={(value) =>
            void updateConfig({
              ...config,
              feature_flags: { ...config.feature_flags, gps_enabled: value }
            })
          }
        />
        <Text style={styles.value}>GPS data: {gpsValue}</Text>

        <View style={styles.buttons}>
          <Button
            title="Export Config"
            onPress={() => {
              void exportConfig(config)
                .then((path) => setStatus(`config exported: ${path}`))
                .catch((e) => setStatus(`export failed: ${String(e)}`));
            }}
          />
          <Button
            title="Import Config"
            onPress={() => {
              void importConfig()
                .then((cfg) => {
                  setConfig(cfg);
                  setStatus('config imported');
                })
                .catch((e) => setStatus(`import failed: ${String(e)}`));
            }}
          />
        </View>

        <Text style={styles.status}>Status: {status}</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

function RowSwitch({
  label,
  value,
  onChange
}: {
  label: string;
  value: boolean;
  onChange: (next: boolean) => void;
}) {
  return (
    <View style={styles.row}>
      <Text style={styles.label}>{label}</Text>
      <Switch value={value} onValueChange={onChange} />
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#fff' },
  content: { padding: 16, gap: 10 },
  title: { fontSize: 22, fontWeight: '700' },
  row: {
    marginTop: 6,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between'
  },
  label: { fontSize: 16 },
  value: { fontSize: 14 },
  buttons: { marginTop: 10, gap: 10 },
  status: { marginTop: 12, fontSize: 12, color: '#555' }
});
