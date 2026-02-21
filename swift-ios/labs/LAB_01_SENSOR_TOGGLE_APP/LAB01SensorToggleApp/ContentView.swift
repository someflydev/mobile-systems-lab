import SwiftUI
import UniformTypeIdentifiers

struct ConfigDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.json] }
    var data: Data

    init(data: Data = Data()) {
        self.data = data
    }

    init(configuration: ReadConfiguration) throws {
        guard let payload = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        self.data = payload
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        FileWrapper(regularFileWithContents: data)
    }
}

struct ContentView: View {
    @Environment(\.scenePhase) private var scenePhase
    @StateObject private var vm = AppViewModel()

    @State private var showingImporter = false
    @State private var showingExporter = false
    @State private var exportDocument = ConfigDocument()

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(vm.config.app_title)
                .font(.title3)
                .bold()

            Toggle("Accelerometer", isOn: Binding(
                get: { vm.config.feature_flags.accelerometer_enabled },
                set: { vm.setAccelerometerEnabled($0) }
            ))
            Text("Accelerometer data: \(vm.accelerometerValue)")
                .font(.callout)

            Toggle("GPS", isOn: Binding(
                get: { vm.config.feature_flags.gps_enabled },
                set: { vm.setGpsEnabled($0) }
            ))
            Text("GPS data: \(vm.gpsValue)")
                .font(.callout)

            HStack(spacing: 12) {
                Button("Export Config") {
                    do {
                        exportDocument = ConfigDocument(data: try vm.exportData())
                        showingExporter = true
                    } catch {
                        vm.status = "export failed: \(error.localizedDescription)"
                    }
                }

                Button("Import Config") {
                    showingImporter = true
                }
            }

            Text("Status: \(vm.status)")
                .font(.footnote)
                .foregroundStyle(.secondary)

            Spacer()
        }
        .padding(16)
        .preferredColorScheme(vm.config.feature_flags.dark_mode ? .dark : .light)
        .onChange(of: scenePhase) { _, newValue in
            vm.onSceneActive(newValue == .active)
        }
        .fileImporter(
            isPresented: $showingImporter,
            allowedContentTypes: [.json]
        ) { result in
            switch result {
            case .success(let url):
                do {
                    let data = try Data(contentsOf: url)
                    vm.importData(data)
                } catch {
                    vm.status = "import read failed: \(error.localizedDescription)"
                }
            case .failure(let error):
                vm.status = "import cancelled: \(error.localizedDescription)"
            }
        }
        .fileExporter(
            isPresented: $showingExporter,
            document: exportDocument,
            contentType: .json,
            defaultFilename: "lab01-config"
        ) { result in
            switch result {
            case .success:
                vm.status = "config exported"
            case .failure(let error):
                vm.status = "export failed: \(error.localizedDescription)"
            }
        }
    }
}
