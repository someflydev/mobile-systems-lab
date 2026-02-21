import Foundation

final class ConfigStore {
    func load() {
        {{CONFIG_LOAD}}
    }

    func save() {
        {{CONFIG_SAVE}}
    }
}
