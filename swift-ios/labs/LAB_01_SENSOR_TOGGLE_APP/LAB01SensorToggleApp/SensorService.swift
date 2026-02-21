import CoreLocation
import CoreMotion
import Foundation

final class SensorService: NSObject, CLLocationManagerDelegate {
    private let motionManager = CMMotionManager()
    private let locationManager = CLLocationManager()

    var onAccelerometer: ((String) -> Void)?
    var onGPS: ((String) -> Void)?
    var onStatus: ((String) -> Void)?

    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.distanceFilter = 1
    }

    func startAccelerometer() {
        guard motionManager.isAccelerometerAvailable else {
            onStatus?("accelerometer unavailable")
            return
        }
        motionManager.accelerometerUpdateInterval = 0.3
        motionManager.startAccelerometerUpdates(to: .main) { [weak self] data, _ in
            guard let d = data else { return }
            self?.onAccelerometer?(String(format: "x=%.2f y=%.2f z=%.2f", d.acceleration.x, d.acceleration.y, d.acceleration.z))
        }
    }

    func stopAccelerometer() {
        motionManager.stopAccelerometerUpdates()
    }

    func requestLocationPermissionIfNeeded() {
        if locationManager.authorizationStatus == .notDetermined {
            locationManager.requestWhenInUseAuthorization()
        }
    }

    func canUseLocation() -> Bool {
        locationManager.authorizationStatus == .authorizedWhenInUse || locationManager.authorizationStatus == .authorizedAlways
    }

    func startGPS() {
        guard canUseLocation() else {
            onStatus?("location permission required")
            return
        }
        locationManager.startUpdatingLocation()
    }

    func stopGPS() {
        locationManager.stopUpdatingLocation()
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        if canUseLocation() {
            onStatus?("location permission granted")
        } else {
            onStatus?("location permission denied")
        }
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        onGPS?(String(format: "lat=%.5f lon=%.5f +/-%.1fm", location.coordinate.latitude, location.coordinate.longitude, location.horizontalAccuracy))
    }

    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        onStatus?("gps error: \(error.localizedDescription)")
    }
}
