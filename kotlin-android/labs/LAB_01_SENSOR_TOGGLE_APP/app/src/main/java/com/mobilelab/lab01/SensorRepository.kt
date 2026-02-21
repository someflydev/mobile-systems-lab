package com.mobilelab.lab01

import android.annotation.SuppressLint
import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Looper
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.sample

class SensorRepository(private val context: Context) {
    fun accelerometerFlow(): Flow<AccelReading> = callbackFlow {
        val sensorManager = context.getSystemService(SensorManager::class.java)
        val sensor = sensorManager?.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
            ?: run {
                close(IllegalStateException("No accelerometer available"))
                return@callbackFlow
            }

        val listener = object : SensorEventListener {
            override fun onSensorChanged(event: SensorEvent) {
                trySend(AccelReading(event.values[0], event.values[1], event.values[2]))
            }

            override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) = Unit
        }

        sensorManager.registerListener(listener, sensor, SensorManager.SENSOR_DELAY_GAME)
        awaitClose { sensorManager.unregisterListener(listener) }
    }.sample(300L)

    @SuppressLint("MissingPermission")
    fun gpsFlow(): Flow<GpsReading> = callbackFlow {
        if (!PermissionManager.hasLocationPermission(context)) {
            close(SecurityException("Location permission denied"))
            return@callbackFlow
        }

        val manager = context.getSystemService(LocationManager::class.java)
            ?: run {
                close(IllegalStateException("No location manager available"))
                return@callbackFlow
            }

        val provider = when {
            manager.isProviderEnabled(LocationManager.GPS_PROVIDER) -> LocationManager.GPS_PROVIDER
            manager.isProviderEnabled(LocationManager.NETWORK_PROVIDER) -> LocationManager.NETWORK_PROVIDER
            else -> {
                close(IllegalStateException("No location provider enabled"))
                return@callbackFlow
            }
        }

        val listener = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                trySend(GpsReading(location.latitude, location.longitude, location.accuracy))
            }
        }

        manager.requestLocationUpdates(provider, 1_000L, 1f, listener, Looper.getMainLooper())
        awaitClose { manager.removeUpdates(listener) }
    }.sample(1_000L)
}
