import Foundation

@MainActor
final class AppViewModel: ObservableObject {
    @Published var config: LabConfig = .fallback
    @Published var accelerometerValue: String = "disabled"
    @Published var gpsValue: String = "disabled"
    @Published var status: String = "ready"

    private let configStore = ConfigStore()
    private let sensorService = SensorService()
    private var isForeground = false

    init() {
        sensorService.onAccelerometer = { [weak self] value in
            guard let self else { return }
            self.accelerometerValue = value
            if self.config.feature_flags.log_sensor_data { self.status = "accelerometer updated" }
        }
        sensorService.onGPS = { [weak self] value in
            guard let self else { return }
            self.gpsValue = value
            if self.config.feature_flags.log_sensor_data { self.status = "gps updated" }
        }
        sensorService.onStatus = { [weak self] value in
            self?.status = value
        }

        config = configStore.load()
    }

    func onSceneActive(_ active: Bool) {
        isForeground = active
        syncSensors()
    }

    func setAccelerometerEnabled(_ enabled: Bool) {
        config.feature_flags.accelerometer_enabled = enabled
        configStore.persist(config)
        syncSensors()
    }

    func setGpsEnabled(_ enabled: Bool) {
        config.feature_flags.gps_enabled = enabled
        if enabled { sensorService.requestLocationPermissionIfNeeded() }
        configStore.persist(config)
        syncSensors()
    }

    func exportData() throws -> Data {
        try configStore.exportConfig(config)
    }

    func importData(_ data: Data) {
        do {
            config = try configStore.importConfig(from: data)
            status = "config imported"
            syncSensors()
        } catch {
            status = "import failed: \(error.localizedDescription)"
        }
    }

    private func syncSensors() {
        sensorService.stopAccelerometer()
        sensorService.stopGPS()

        guard isForeground else {
            accelerometerValue = "paused (background)"
            gpsValue = "paused (background)"
            return
        }

        if config.feature_flags.accelerometer_enabled {
            sensorService.startAccelerometer()
        } else {
            accelerometerValue = "disabled"
        }

        if config.feature_flags.gps_enabled {
            if sensorService.canUseLocation() {
                sensorService.startGPS()
            } else {
                gpsValue = "permission required"
            }
        } else {
            gpsValue = "disabled"
        }
    }
}
