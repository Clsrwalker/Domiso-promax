import AppKit
import Combine
import DomisoCore
import Foundation
import UniformTypeIdentifiers

@MainActor
final class AppViewModel: ObservableObject {
    @Published var sheetText: String = """
    bpm=80
    1=C
    1 2 3 4 5 6 7 +1
    ( 1 3 5 )--
    """
    @Published private(set) var parsedSheet = DomisoParsedSheet(noteEvents: [], totalBeats: 0, totalMilliseconds: 0, diagnostics: [])
    @Published private(set) var playbackPlan = DomisoPlaybackPlan(
        events: [],
        ignoredNoteCount: 0,
        report: PlaybackOptimizationReport(eventCount: 0, mergedCount: 0, peakPerSecond: 0, minimumGapMilliseconds: 0)
    )
    @Published var speedPercent: Double = 95
    @Published var holdMinimumMilliseconds: Double = 150
    @Published var sameKeyMinimumGapMilliseconds: Double = 110
    @Published var statusText: String = "Ready."
    @Published var converterLog: String = ""
    @Published var generatedFiles: [URL] = []
    @Published var currentFileURL: URL?

    let playback = PlaybackController()
    let preview = AudioPreviewController()

    private let parser = DomisoSheetParser()
    private let keyMap = DomisoKeyMap.domiso36
    private let converter = DomisoConverterBridge()
    private var cancellables: Set<AnyCancellable> = []

    init() {
        playback.objectWillChange
            .sink { [weak self] _ in
                self?.objectWillChange.send()
            }
            .store(in: &cancellables)
        preview.objectWillChange
            .sink { [weak self] _ in
                self?.objectWillChange.send()
            }
            .store(in: &cancellables)
        reparse()
    }

    func reparse() {
        parsedSheet = parser.parse(sheetText)
        playbackPlan = keyMap.playbackPlan(
            for: parsedSheet,
            speedPercent: speedPercent,
            sameKeyMinimumGapMilliseconds: Int(sameKeyMinimumGapMilliseconds.rounded())
        )
        playback.holdMinimumMilliseconds = Int(holdMinimumMilliseconds.rounded())
        playback.load(totalMilliseconds: playbackPlan.events.map(\.endMilliseconds).max() ?? parsedSheet.totalMilliseconds)
        preview.load(totalMilliseconds: parsedSheet.totalMilliseconds)
        statusText = "\(playbackPlan.report.eventCount) notes | \(String(format: "%.2f", parsedSheet.totalBeats)) beats | \(playbackPlan.ignoredNoteCount) ignored"
    }

    func requestAccessibilityPermission() {
        if AccessibilityPermission.isTrusted(prompt: true) {
            statusText = "Accessibility permission is already granted."
        } else {
            statusText = "Grant Accessibility permission in System Settings, then relaunch if needed."
        }
    }

    func playOrResume() {
        reparse()
        guard !playbackPlan.events.isEmpty else {
            statusText = "No playable events."
            return
        }
        playback.play(events: playbackPlan.events)
    }

    func listenOrResume() {
        reparse()
        guard !parsedSheet.noteEvents.isEmpty else {
            statusText = "No notes to preview."
            return
        }
        preview.play(events: parsedSheet.noteEvents)
    }

    func pause() {
        playback.pause()
        preview.pause()
    }

    func stop() {
        playback.stop()
        preview.stop()
    }

    func openSheet() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [.plainText]
        panel.allowsMultipleSelection = false
        panel.canChooseDirectories = false
        guard panel.runModal() == .OK, let url = panel.url else {
            return
        }
        do {
            sheetText = try String(contentsOf: url, encoding: .utf8)
            currentFileURL = url
            reparse()
            statusText = "Opened \(url.lastPathComponent)."
        } catch {
            statusText = "Open failed: \(error.localizedDescription)"
        }
    }

    func saveSheet() {
        let destination: URL
        if let currentFileURL {
            destination = currentFileURL
        } else {
            let panel = NSSavePanel()
            panel.allowedContentTypes = [.plainText]
            panel.nameFieldStringValue = "domiso-sheet.txt"
            guard panel.runModal() == .OK, let url = panel.url else {
                return
            }
            destination = url
            currentFileURL = url
        }

        do {
            try sheetText.write(to: destination, atomically: true, encoding: .utf8)
            statusText = "Saved \(destination.lastPathComponent)."
        } catch {
            statusText = "Save failed: \(error.localizedDescription)"
        }
    }

    func importMIDI() {
        let midiPanel = NSOpenPanel()
        midiPanel.allowedContentTypes = [
            UTType(filenameExtension: "mid"),
            UTType(filenameExtension: "midi")
        ].compactMap { $0 }
        midiPanel.allowsMultipleSelection = false
        midiPanel.canChooseDirectories = false
        guard midiPanel.runModal() == .OK, let midiURL = midiPanel.url else {
            return
        }

        let outPanel = NSOpenPanel()
        outPanel.title = "Choose conversion output folder"
        outPanel.canChooseFiles = false
        outPanel.canChooseDirectories = true
        outPanel.canCreateDirectories = true
        outPanel.allowsMultipleSelection = false
        guard outPanel.runModal() == .OK, let outputURL = outPanel.url else {
            return
        }

        statusText = "Converting \(midiURL.lastPathComponent)..."
        converterLog = ""
        generatedFiles = []

        let converter = self.converter
        Task {
            do {
                let result = try await Task.detached {
                    try await converter.convert(midiURL: midiURL, outputDirectory: outputURL)
                }.value
                converterLog = result.log
                generatedFiles = result.outputFiles
                statusText = "Conversion done. \(result.outputFiles.count) TXT files."
                if let first = result.outputFiles.first {
                    loadGeneratedFile(first)
                }
            } catch {
                converterLog = error.localizedDescription
                statusText = "Conversion failed."
            }
        }
    }

    func loadGeneratedFile(_ url: URL) {
        do {
            sheetText = try String(contentsOf: url, encoding: .utf8)
            currentFileURL = url
            reparse()
            statusText = "Loaded \(url.lastPathComponent)."
        } catch {
            statusText = "Load generated file failed: \(error.localizedDescription)"
        }
    }
}
