package com.mobilelab.lab01

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class UiState(
    val config: LabConfig = LabConfig(),
    val accelerometerValue: String = "disabled",
    val gpsValue: String = "disabled",
    val status: String = "ready"
)

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val configRepo = ConfigRepository(application.applicationContext)
    private val sensorRepo = SensorRepository(application.applicationContext)

    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    private var accelJob: Job? = null
    private var gpsJob: Job? = null
    private var isForeground = false

    init {
        val cfg = configRepo.loadConfig()
        _uiState.update { it.copy(config = cfg) }
    }

    fun onForegroundChanged(isForeground: Boolean) {
        this.isForeground = isForeground
        if (isForeground) {
            syncSensors()
        } else {
            stopSensors()
        }
    }

    fun setAccelerometerEnabled(enabled: Boolean) {
        updateConfig(
            _uiState.value.config.copy(
                feature_flags = _uiState.value.config.feature_flags.copy(accelerometer_enabled = enabled)
            )
        )
    }

    fun setGpsEnabled(enabled: Boolean) {
        updateConfig(
            _uiState.value.config.copy(
                feature_flags = _uiState.value.config.feature_flags.copy(gps_enabled = enabled)
            )
        )
    }

    fun onLocationPermissionResult(granted: Boolean) {
        if (!granted) {
            setGpsEnabled(false)
            _uiState.update { it.copy(status = "location permission denied") }
        } else {
            _uiState.update { it.copy(status = "location permission granted") }
            syncSensors()
        }
    }

    fun exportConfig(uri: Uri) {
        runCatching {
            configRepo.exportConfig(_uiState.value.config, uri)
            _uiState.update { it.copy(status = "config exported") }
        }.onFailure {
            _uiState.update { it.copy(status = "export failed: ${it.message}") }
        }
    }

    fun importConfig(uri: Uri) {
        runCatching {
            val cfg = configRepo.importConfig(uri)
            _uiState.update { it.copy(config = cfg, status = "config imported") }
            syncSensors()
        }.onFailure {
            _uiState.update { it.copy(status = "import failed: ${it.message}") }
        }
    }

    private fun updateConfig(config: LabConfig) {
        configRepo.persistToggles(config)
        _uiState.update { it.copy(config = config) }
        syncSensors()
    }

    private fun syncSensors() {
        stopSensors()
        val config = _uiState.value.config
        if (!isForeground) {
            _uiState.update {
                it.copy(
                    accelerometerValue = "paused (background)",
                    gpsValue = "paused (background)"
                )
            }
            return
        }

        if (config.feature_flags.accelerometer_enabled) {
            accelJob = viewModelScope.launch {
                sensorRepo.accelerometerFlow().collect { reading ->
                    _uiState.update {
                        it.copy(
                            accelerometerValue = reading.toDisplay(),
                            status = if (config.feature_flags.log_sensor_data) "accel updated" else it.status
                        )
                    }
                }
            }
        } else {
            _uiState.update { it.copy(accelerometerValue = "disabled") }
        }

        if (config.feature_flags.gps_enabled) {
            if (!PermissionManager.hasLocationPermission(getApplication())) {
                _uiState.update { it.copy(gpsValue = "permission required", status = "request location permission") }
            } else {
                gpsJob = viewModelScope.launch {
                    sensorRepo.gpsFlow().collect { reading ->
                        _uiState.update {
                            it.copy(
                                gpsValue = reading.toDisplay(),
                                status = if (config.feature_flags.log_sensor_data) "gps updated" else it.status
                            )
                        }
                    }
                }
            }
        } else {
            _uiState.update { it.copy(gpsValue = "disabled") }
        }
    }

    private fun stopSensors() {
        accelJob?.cancel()
        gpsJob?.cancel()
        accelJob = null
        gpsJob = null
    }
}
