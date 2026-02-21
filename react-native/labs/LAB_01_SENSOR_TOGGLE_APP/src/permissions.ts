import * as Location from 'expo-location';

export async function ensureLocationPermission(): Promise<boolean> {
  const servicesEnabled = await Location.hasServicesEnabledAsync();
  if (!servicesEnabled) return false;

  const existing = await Location.getForegroundPermissionsAsync();
  if (existing.granted) return true;

  const requested = await Location.requestForegroundPermissionsAsync();
  return requested.granted;
}
