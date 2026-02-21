import Foundation

final class ConfigStore {
    private let decoder = JSONDecoder()
    private let encoder = JSONEncoder()
    private let localConfigFilename = "config.json"
    private let defaults = UserDefaults.standard

    init() {
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
    }

    func load() -> LabConfig {
        let baseConfig = loadLocalOrBundled()
        return applyPersistedToggles(baseConfig)
    }

    func persist(_ config: LabConfig) {
        defaults.set(config.feature_flags.accelerometer_enabled, forKey: "accelerometer_enabled")
        defaults.set(config.feature_flags.gps_enabled, forKey: "gps_enabled")
        if let data = try? encoder.encode(config) {
            try? data.write(to: localConfigURL(), options: [.atomic])
        }
    }

    func exportConfig(_ config: LabConfig) throws -> Data {
        try encoder.encode(config)
    }

    func importConfig(from data: Data) throws -> LabConfig {
        let config = try decoder.decode(LabConfig.self, from: data)
        guard config.version == 1 else {
            throw NSError(domain: "LabConfig", code: 1, userInfo: [NSLocalizedDescriptionKey: "Unsupported config version"])
        }
        persist(config)
        return config
    }

    private func loadLocalOrBundled() -> LabConfig {
        if let data = try? Data(contentsOf: localConfigURL()),
           let cfg = try? decoder.decode(LabConfig.self, from: data) {
            return cfg
        }

        guard let url = Bundle.main.url(forResource: "config", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let cfg = try? decoder.decode(LabConfig.self, from: data)
        else {
            return .fallback
        }
        return cfg
    }

    private func applyPersistedToggles(_ config: LabConfig) -> LabConfig {
        var adjusted = config
        adjusted.feature_flags.accelerometer_enabled = defaults.object(forKey: "accelerometer_enabled") as? Bool ?? config.feature_flags.accelerometer_enabled
        adjusted.feature_flags.gps_enabled = defaults.object(forKey: "gps_enabled") as? Bool ?? config.feature_flags.gps_enabled
        return adjusted
    }

    private func localConfigURL() -> URL {
        let dir = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        return dir.appendingPathComponent(localConfigFilename)
    }
}
