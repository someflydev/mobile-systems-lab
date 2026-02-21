import Foundation

struct LabConfig: Codable {
    var version: Int
    var app_title: String
    var feature_flags: FeatureFlags

    static let fallback = LabConfig(
        version: 1,
        app_title: "LAB_01 Sensor Toggle App",
        feature_flags: FeatureFlags(
            accelerometer_enabled: false,
            gps_enabled: false,
            dark_mode: false,
            log_sensor_data: true
        )
    )
}

struct FeatureFlags: Codable {
    var accelerometer_enabled: Bool
    var gps_enabled: Bool
    var dark_mode: Bool
    var log_sensor_data: Bool
}
