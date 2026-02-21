import { Accelerometer } from 'expo-sensors';
import * as Location from 'expo-location';

export type SensorHandles = {
  stopAccelerometer: () => void;
  stopGps: () => Promise<void>;
};

export function createSensorHandles(): SensorHandles {
  let accelSub: { remove: () => void } | null = null;
  let gpsSub: Location.LocationSubscription | null = null;

  return {
    stopAccelerometer: () => {
      accelSub?.remove();
      accelSub = null;
    },
    stopGps: async () => {
      gpsSub?.remove();
      gpsSub = null;
    }
  };
}

export function startAccelerometer(onData: (value: string) => void): () => void {
  Accelerometer.setUpdateInterval(300);
  const sub = Accelerometer.addListener((v) => {
    onData(`x=${v.x.toFixed(2)} y=${v.y.toFixed(2)} z=${v.z.toFixed(2)}`);
  });
  return () => sub.remove();
}

export async function startGps(onData: (value: string) => void): Promise<() => void> {
  const subscription = await Location.watchPositionAsync(
    {
      accuracy: Location.Accuracy.High,
      distanceInterval: 1,
      timeInterval: 1000
    },
    (pos) => {
      onData(
        `lat=${pos.coords.latitude.toFixed(5)} lon=${pos.coords.longitude.toFixed(5)} +/-${pos.coords.accuracy?.toFixed(1)}m`
      );
    }
  );

  return () => subscription.remove();
}
