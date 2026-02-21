package com.mobilelab.lab01

import kotlinx.serialization.Serializable

@Serializable
data class LabConfig(
    val version: Int = 1,
    val app_title: String = "LAB_01 Sensor Toggle App",
    val feature_flags: FeatureFlags = FeatureFlags()
)

@Serializable
data class FeatureFlags(
    val accelerometer_enabled: Boolean = false,
    val gps_enabled: Boolean = false,
    val dark_mode: Boolean = false,
    val log_sensor_data: Boolean = true
)

data class AccelReading(val x: Float, val y: Float, val z: Float)

data class GpsReading(val latitude: Double, val longitude: Double, val accuracyMeters: Float)

fun AccelReading.toDisplay(): String = "x=%.2f y=%.2f z=%.2f".format(x, y, z)

fun GpsReading.toDisplay(): String =
    "lat=%.5f lon=%.5f +/-%.1fm".format(latitude, longitude, accuracyMeters)
