import Foundation

final class AppViewModel: ObservableObject {
    // {{STATE_MODEL}}

    func loadConfig() {
        {{CONFIG_LOAD}}
    }

    func saveConfig() {
        {{CONFIG_SAVE}}
    }

    func requestPermissions() {
        {{PERMISSION_REQUEST}}
    }

    func startSensors() {
        {{SENSOR_SUBSCRIPTION}}
    }

    func backgroundPolicy() {
        {{BACKGROUND_BLOCK}}
    }
}
