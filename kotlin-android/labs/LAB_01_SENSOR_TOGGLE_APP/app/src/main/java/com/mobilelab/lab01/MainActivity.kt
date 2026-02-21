package com.mobilelab.lab01

import android.Manifest
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle

class MainActivity : ComponentActivity() {
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val state by viewModel.uiState.collectAsStateWithLifecycle()

            val permissionLauncher = rememberLauncherForActivityResult(
                ActivityResultContracts.RequestPermission()
            ) { granted -> viewModel.onLocationPermissionResult(granted) }

            val exportLauncher = rememberLauncherForActivityResult(
                ActivityResultContracts.CreateDocument("application/json")
            ) { uri: Uri? -> uri?.let(viewModel::exportConfig) }

            val importLauncher = rememberLauncherForActivityResult(
                ActivityResultContracts.OpenDocument()
            ) { uri: Uri? -> uri?.let(viewModel::importConfig) }

            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    LabScreen(
                        uiState = state,
                        onAccelerometerToggle = viewModel::setAccelerometerEnabled,
                        onGpsToggle = { enabled ->
                            viewModel.setGpsEnabled(enabled)
                            if (enabled && !PermissionManager.hasLocationPermission(this)) {
                                permissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
                            }
                        },
                        onExport = { exportLauncher.launch("lab01-config.json") },
                        onImport = { importLauncher.launch(arrayOf("application/json")) }
                    )
                }
            }
        }
    }

    override fun onStart() {
        super.onStart()
        viewModel.onForegroundChanged(true)
    }

    override fun onStop() {
        viewModel.onForegroundChanged(false)
        super.onStop()
    }
}

@Composable
private fun LabScreen(
    uiState: UiState,
    onAccelerometerToggle: (Boolean) -> Unit,
    onGpsToggle: (Boolean) -> Unit,
    onExport: () -> Unit,
    onImport: () -> Unit
) {
    val flags = uiState.config.feature_flags
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Text(text = uiState.config.app_title, style = MaterialTheme.typography.headlineSmall)

        Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Text("Accelerometer", modifier = Modifier.weight(1f))
            Switch(checked = flags.accelerometer_enabled, onCheckedChange = onAccelerometerToggle)
        }
        Text("Accelerometer data: ${uiState.accelerometerValue}")

        Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Text("GPS", modifier = Modifier.weight(1f))
            Switch(checked = flags.gps_enabled, onCheckedChange = onGpsToggle)
        }
        Text("GPS data: ${uiState.gpsValue}")

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(onClick = onExport) { Text("Export Config") }
            Button(onClick = onImport) { Text("Import Config") }
        }

        Spacer(modifier = Modifier.height(4.dp))
        Text("Status: ${uiState.status}", style = MaterialTheme.typography.bodySmall)
    }
}
