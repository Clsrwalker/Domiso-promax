import DomisoCore
import Foundation
import SwiftUI

struct ContentView: View {
    @StateObject private var model = AppViewModel()

    var body: some View {
        VStack(spacing: 0) {
            toolbar
            Divider()
            HSplitView {
                editor
                    .frame(minWidth: 560)
                inspector
                    .frame(minWidth: 330, idealWidth: 360, maxWidth: 440)
            }
            Divider()
            statusBar
        }
        .onChange(of: model.sheetText) { _ in
            model.reparse()
        }
        .onChange(of: model.speedPercent) { _ in
            model.reparse()
        }
        .onChange(of: model.holdMinimumMilliseconds) { _ in
            model.reparse()
        }
        .onChange(of: model.sameKeyMinimumGapMilliseconds) { _ in
            model.reparse()
        }
    }

    private var toolbar: some View {
        HStack(spacing: 8) {
            Button("Open", action: model.openSheet)
            Button("Save", action: model.saveSheet)
            Button("MIDI", action: model.importMIDI)
            Divider().frame(height: 22)
            Button("Accessibility", action: model.requestAccessibilityPermission)
            Spacer()
            Button("Parse", action: model.reparse)
            Button("Play", action: model.playOrResume)
                .keyboardShortcut(.return, modifiers: [.command])
            Button("Listen", action: model.listenOrResume)
            Button("Pause", action: model.pause)
            Button("Stop", action: model.stop)
                .keyboardShortcut(.escape, modifiers: [])
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
    }

    private var editor: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Text(model.currentFileURL?.lastPathComponent ?? "Untitled")
                    .font(.headline)
                Spacer()
                Text("\(model.parsedSheet.noteEvents.count) parsed notes")
                    .foregroundStyle(.secondary)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)

            TextEditor(text: $model.sheetText)
                .font(.system(.body, design: .monospaced))
                .scrollContentBackground(.hidden)
                .padding(8)
        }
    }

    private var inspector: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                playbackSection
                parseSection
                diagnosticsSection
                conversionSection
            }
            .padding(14)
        }
    }

    private var playbackSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Playback").font(.headline)
            Grid(alignment: .leading, horizontalSpacing: 12, verticalSpacing: 8) {
                GridRow {
                    Text("Play")
                    Text(model.playback.state.rawValue)
                }
                GridRow {
                    Text("Listen")
                    Text(model.preview.state.rawValue)
                }
                GridRow {
                    Text("Position")
                    Text(timeString(max(model.playback.positionMilliseconds, model.preview.positionMilliseconds)))
                }
                GridRow {
                    Text("Duration")
                    Text(timeString(max(model.playback.totalMilliseconds, model.preview.totalMilliseconds)))
                }
            }

            Slider(value: Binding(
                get: { Double(max(model.playback.positionMilliseconds, model.preview.positionMilliseconds)) },
                set: {
                    let value = Int($0.rounded())
                    model.playback.seek(to: value)
                    model.preview.seek(to: value)
                }
            ), in: 0...Double(max(model.playback.totalMilliseconds, model.preview.totalMilliseconds, 1)))

            VStack(alignment: .leading) {
                Text("Speed \(Int(model.speedPercent.rounded()))%")
                Slider(value: $model.speedPercent, in: 70...120, step: 1)
            }
            VStack(alignment: .leading) {
                Text("Hold \(Int(model.holdMinimumMilliseconds.rounded())) ms")
                Slider(value: $model.holdMinimumMilliseconds, in: 80...400, step: 1)
            }
            VStack(alignment: .leading) {
                Text("Same key gap \(Int(model.sameKeyMinimumGapMilliseconds.rounded())) ms")
                Slider(value: $model.sameKeyMinimumGapMilliseconds, in: 20...400, step: 1)
            }
        }
    }

    private var parseSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Analysis").font(.headline)
            Grid(alignment: .leading, horizontalSpacing: 12, verticalSpacing: 8) {
                GridRow {
                    Text("Total beats")
                    Text(String(format: "%.2f", model.parsedSheet.totalBeats))
                }
                GridRow {
                    Text("Playable")
                    Text("\(model.playbackPlan.report.eventCount)")
                }
                GridRow {
                    Text("Ignored")
                    Text("\(model.playbackPlan.ignoredNoteCount)")
                }
                GridRow {
                    Text("Merged")
                    Text("\(model.playbackPlan.report.mergedCount)")
                }
                GridRow {
                    Text("Peak")
                    Text("\(model.playbackPlan.report.peakPerSecond)/s")
                }
                GridRow {
                    Text("Min gap")
                    Text("\(model.playbackPlan.report.minimumGapMilliseconds) ms")
                }
            }
        }
    }

    private var diagnosticsSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Diagnostics").font(.headline)
            if model.parsedSheet.diagnostics.isEmpty {
                Text("No parser diagnostics.")
                    .foregroundStyle(.secondary)
            } else {
                ForEach(model.parsedSheet.diagnostics) { diagnostic in
                    Text("Line \(diagnostic.line): \(diagnostic.message)")
                        .foregroundStyle(diagnostic.severity == .warning ? .orange : .secondary)
                        .textSelection(.enabled)
                }
            }
        }
    }

    private var conversionSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("MIDI Conversion").font(.headline)
            if model.generatedFiles.isEmpty {
                Text("No generated TXT files.")
                    .foregroundStyle(.secondary)
            } else {
                ForEach(model.generatedFiles, id: \.self) { url in
                    Button(url.lastPathComponent) {
                        model.loadGeneratedFile(url)
                    }
                    .buttonStyle(.link)
                }
            }
            if !model.converterLog.isEmpty {
                Text(model.converterLog)
                    .font(.system(.caption, design: .monospaced))
                    .textSelection(.enabled)
                    .lineLimit(12)
            }
        }
    }

    private var statusBar: some View {
        HStack {
            Text(model.statusText)
                .lineLimit(1)
            Spacer()
            Text(AccessibilityPermission.isTrusted() ? "Accessibility OK" : "Accessibility Needed")
                .foregroundStyle(AccessibilityPermission.isTrusted() ? .green : .orange)
        }
        .font(.caption)
        .padding(.horizontal, 12)
        .padding(.vertical, 6)
    }

    private func timeString(_ milliseconds: Int) -> String {
        let totalSeconds = milliseconds / 1000
        let minutes = totalSeconds / 60
        let seconds = totalSeconds % 60
        return String(format: "%02d:%02d", minutes, seconds)
    }
}
