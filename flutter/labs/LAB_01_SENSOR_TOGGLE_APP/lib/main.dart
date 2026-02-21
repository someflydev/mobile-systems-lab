import 'package:flutter/material.dart';

import 'services/config_service.dart';
import 'services/permission_service.dart';
import 'services/sensor_service.dart';
import 'viewmodels/lab01_view_model.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const LabApp());
}

class LabApp extends StatefulWidget {
  const LabApp({super.key});

  @override
  State<LabApp> createState() => _LabAppState();
}

class _LabAppState extends State<LabApp> with WidgetsBindingObserver {
  late final Lab01ViewModel vm;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    vm = Lab01ViewModel(ConfigService(), PermissionService(), SensorService());
    vm.initialize();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    vm.onLifecycleForeground(state == AppLifecycleState.resumed);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    vm.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: vm,
      builder: (context, _) {
        return MaterialApp(
          debugShowCheckedModeBanner: false,
          themeMode: vm.config.featureFlags.darkMode ? ThemeMode.dark : ThemeMode.light,
          darkTheme: ThemeData.dark(useMaterial3: true),
          theme: ThemeData.light(useMaterial3: true),
          home: Scaffold(
            appBar: AppBar(title: Text(vm.config.appTitle)),
            body: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SwitchListTile(
                    contentPadding: EdgeInsets.zero,
                    title: const Text('Accelerometer'),
                    value: vm.config.featureFlags.accelerometerEnabled,
                    onChanged: vm.setAccelerometerEnabled,
                  ),
                  Text('Accelerometer data: ${vm.accelerometerValue}'),
                  const SizedBox(height: 12),
                  SwitchListTile(
                    contentPadding: EdgeInsets.zero,
                    title: const Text('GPS'),
                    value: vm.config.featureFlags.gpsEnabled,
                    onChanged: vm.setGpsEnabled,
                  ),
                  Text('GPS data: ${vm.gpsValue}'),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      ElevatedButton(
                        onPressed: vm.exportConfig,
                        child: const Text('Export Config'),
                      ),
                      const SizedBox(width: 12),
                      ElevatedButton(
                        onPressed: vm.importConfig,
                        child: const Text('Import Config'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text('Status: ${vm.status}'),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
