package {{KOTLIN_PACKAGE}}

class MainViewModel {
    // {{STATE_MODEL}}

    fun loadConfig() {
        {{CONFIG_LOAD}}
    }

    fun saveConfig() {
        {{CONFIG_SAVE}}
    }

    fun syncSensors() {
        {{SENSOR_SUBSCRIPTION}}
    }

    fun ensurePermissions() {
        {{PERMISSION_REQUEST}}
    }

    fun handleBackgroundPolicy() {
        {{BACKGROUND_BLOCK}}
    }
}
