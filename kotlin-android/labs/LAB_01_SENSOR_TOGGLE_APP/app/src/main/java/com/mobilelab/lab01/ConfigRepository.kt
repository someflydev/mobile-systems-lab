package com.mobilelab.lab01

import android.content.Context
import android.net.Uri
import kotlinx.serialization.json.Json

class ConfigRepository(private val context: Context) {
    private val json = Json { prettyPrint = true; ignoreUnknownKeys = false }
    private val prefs = context.getSharedPreferences("lab01_prefs", Context.MODE_PRIVATE)
    private val localConfigName = "config.json"

    fun loadConfig(): LabConfig {
        val raw = readLocalConfigOrAsset()
        val loaded = runCatching { json.decodeFromString<LabConfig>(raw) }.getOrElse { LabConfig() }
        return loaded.copy(
            feature_flags = loaded.feature_flags.copy(
                accelerometer_enabled = prefs.getBoolean(
                    "accelerometer_enabled",
                    loaded.feature_flags.accelerometer_enabled
                ),
                gps_enabled = prefs.getBoolean("gps_enabled", loaded.feature_flags.gps_enabled)
            )
        )
    }

    fun persistToggles(config: LabConfig) {
        prefs.edit()
            .putBoolean("accelerometer_enabled", config.feature_flags.accelerometer_enabled)
            .putBoolean("gps_enabled", config.feature_flags.gps_enabled)
            .apply()
        context.openFileOutput(localConfigName, Context.MODE_PRIVATE).use {
            it.write(json.encodeToString(config).toByteArray())
        }
    }

    fun exportConfig(config: LabConfig, uri: Uri) {
        context.contentResolver.openOutputStream(uri)?.use {
            it.write(json.encodeToString(config).toByteArray())
        } ?: error("Could not open export target")
    }

    fun importConfig(uri: Uri): LabConfig {
        val imported = context.contentResolver.openInputStream(uri)?.use { stream ->
            stream.bufferedReader().readText()
        } ?: error("Could not read import source")
        val cfg = json.decodeFromString<LabConfig>(imported)
        require(cfg.version == 1) { "Unsupported config version: ${cfg.version}" }
        persistToggles(cfg)
        return cfg
    }

    private fun readLocalConfigOrAsset(): String {
        val local = runCatching {
            context.openFileInput(localConfigName).bufferedReader().readText()
        }.getOrNull()
        if (local != null) return local
        return context.assets.open(localConfigName).bufferedReader().use { it.readText() }
    }
}
