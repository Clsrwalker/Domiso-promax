import Foundation

public struct DomisoSheetParser: Sendable {
    private let baseOffsets = [1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11]
    private let arpeggioDelayMilliseconds = 40

    public init() {}

    public func parse(_ source: String) -> DomisoParsedSheet {
        var context = ParseContext()
        let lines = source.replacingOccurrences(of: "\r\n", with: "\n").replacingOccurrences(of: "\r", with: "\n").split(separator: "\n", omittingEmptySubsequences: false)

        for lineIndex in lines.indices {
            parseLine(String(lines[lineIndex]), lineNumber: lineIndex + 1, context: &context)
        }

        let lastEventEnd = context.events.map(\.endMilliseconds).max() ?? 0
        let total = Int(max(context.offsetMilliseconds, Double(lastEventEnd)).rounded())
        return DomisoParsedSheet(
            noteEvents: context.events.sorted { lhs, rhs in
                if lhs.startMilliseconds == rhs.startMilliseconds {
                    return lhs.midiNote < rhs.midiNote
                }
                return lhs.startMilliseconds < rhs.startMilliseconds
            },
            totalBeats: context.totalBeats,
            totalMilliseconds: total,
            diagnostics: context.diagnostics
        )
    }

    private func parseLine(_ line: String, lineNumber: Int, context: inout ParseContext) {
        applyControlCommands(in: line, lineNumber: lineNumber, context: &context)

        var group: GroupMode?
        var chordCache: [ParsedTokenNote] = []
        var multipletCache: [ParsedTokenNote] = []

        let tokens = line.split { $0 == " " || $0 == "\t" }.map(String.init)
        for token in tokens {
            if token == "(" {
                if group == nil {
                    group = .chord
                    chordCache.removeAll()
                }
                continue
            }
            if token == "{" {
                if group == nil {
                    group = .multiplet
                    multipletCache.removeAll()
                }
                continue
            }
            if token.first == ")", group == .chord {
                let marks = String(token.dropFirst())
                closeChord(chordCache, durationMarks: marks, context: &context)
                group = nil
                chordCache.removeAll()
                continue
            }
            if token.first == "}", group == .multiplet {
                let marks = String(token.dropFirst())
                closeMultiplet(multipletCache, durationMarks: marks, context: &context)
                group = nil
                multipletCache.removeAll()
                continue
            }
            guard let note = parseNoteToken(token, lineNumber: lineNumber, context: &context) else {
                continue
            }

            switch group {
            case .chord:
                chordCache.append(note)
            case .multiplet:
                multipletCache.append(note)
            case nil:
                appendStandalone(note, context: &context)
            }
        }
    }

    private func applyControlCommands(in line: String, lineNumber: Int, context: inout ParseContext) {
        if let bpmText = firstCapture(in: line, pattern: #"(?i)\bbpm\s*=\s*(\d+)"#), let bpm = Double(bpmText) {
            if (1...480).contains(bpm) {
                context.beatMilliseconds = 60000.0 / bpm
            } else {
                context.beatMilliseconds = 60000.0 / 80.0
                context.diagnostics.append(DomisoDiagnostic(line: lineNumber, message: "BPM \(bpmText) is outside 1...480; reset to 80."))
            }
        }

        if let keyText = firstCapture(in: line, pattern: #"(?i)\b1\s*=\s*([A-G](?:\d{0,2})[#b]?)"#) {
            if let base = midiNote(forKeyControl: keyText) {
                context.baseMidi = base
            } else {
                context.diagnostics.append(DomisoDiagnostic(line: lineNumber, message: "Could not parse key control 1=\(keyText)."))
            }
        }

        if let rollbackText = firstCapture(in: line, pattern: #"(?i)\brollback\s*=\s*(\d+(?:\.\d+)?)"#), let beats = Double(rollbackText) {
            let rollbackMilliseconds = beats * context.beatMilliseconds
            context.offsetMilliseconds = max(0, context.offsetMilliseconds - rollbackMilliseconds)
            context.lastNoteDurationMilliseconds = 0
            context.arpeggioAccumulatedMilliseconds = 0
        }
    }

    private func parseNoteToken(_ token: String, lineNumber: Int, context: inout ParseContext) -> ParsedTokenNote? {
        let pattern = #"(?i)^(~)?([+-]*)([0-7])([#b])?([/\-.]*)$"#
        guard let match = firstMatch(in: token, pattern: pattern) else {
            return nil
        }

        let arpeggio = match[1] == "~"
        let scale = match[2]
        guard let degree = Int(match[3]) else {
            return nil
        }
        let semitone = match[4]
        let durationMarks = match[5]
        let durationBeats = duration(baseBeats: 1, marks: durationMarks)

        if degree == 0 {
            return ParsedTokenNote(midiNote: nil, durationBeats: durationBeats, arpeggio: arpeggio)
        }

        guard let baseOffset = baseOffsets[degree] else {
            context.diagnostics.append(DomisoDiagnostic(line: lineNumber, message: "Unsupported note degree \(degree)."))
            return nil
        }

        let octaveOffset: Int
        if scale.first == "-" {
            octaveOffset = -scale.count
        } else {
            octaveOffset = scale.count
        }

        var midi = context.baseMidi + baseOffset + (octaveOffset * 12)
        if semitone == "#" {
            midi += 1
        } else if semitone.lowercased() == "b" {
            midi -= 1
        }

        return ParsedTokenNote(midiNote: midi, durationBeats: durationBeats, arpeggio: arpeggio)
    }

    private func appendStandalone(_ note: ParsedTokenNote, context: inout ParseContext) {
        var durationMilliseconds = note.durationBeats * context.beatMilliseconds
        var isArpeggio = false

        if note.arpeggio {
            guard context.lastNoteDurationMilliseconds > 0 else {
                return
            }
            if durationMilliseconds <= Double(context.arpeggioAccumulatedMilliseconds + 20) {
                return
            }
            isArpeggio = true
            context.offsetMilliseconds -= Double(context.lastNoteDurationMilliseconds)
            context.offsetMilliseconds += Double(arpeggioDelayMilliseconds)
            context.arpeggioAccumulatedMilliseconds += arpeggioDelayMilliseconds
            durationMilliseconds -= Double(context.arpeggioAccumulatedMilliseconds)
        } else {
            context.arpeggioAccumulatedMilliseconds = 0
        }

        let start = max(0, Int(context.offsetMilliseconds.rounded()))
        let duration = max(1, Int(durationMilliseconds.rounded()))
        if let midiNote = note.midiNote, midiNote > 0 {
            context.events.append(NoteEvent(startMilliseconds: start, durationMilliseconds: duration, midiNote: midiNote))
        }

        context.offsetMilliseconds += durationMilliseconds
        if !isArpeggio {
            context.totalBeats += note.durationBeats
        }
        context.lastNoteDurationMilliseconds = duration
    }

    private func closeChord(_ notes: [ParsedTokenNote], durationMarks: String, context: inout ParseContext) {
        guard !notes.isEmpty else {
            return
        }

        let baseBeats = notes.map(\.durationBeats).max() ?? 1
        let durationBeats = duration(baseBeats: baseBeats, marks: durationMarks)
        let durationMilliseconds = max(1, Int((durationBeats * context.beatMilliseconds).rounded()))
        let start = max(0, Int(context.offsetMilliseconds.rounded()))

        for note in notes {
            if let midiNote = note.midiNote, midiNote > 0 {
                context.events.append(NoteEvent(startMilliseconds: start, durationMilliseconds: durationMilliseconds, midiNote: midiNote))
            }
        }

        context.offsetMilliseconds += Double(durationMilliseconds)
        context.totalBeats += durationBeats
        context.lastNoteDurationMilliseconds = durationMilliseconds
        context.arpeggioAccumulatedMilliseconds = 0
    }

    private func closeMultiplet(_ notes: [ParsedTokenNote], durationMarks: String, context: inout ParseContext) {
        guard !notes.isEmpty else {
            return
        }

        let totalDurationBeats = duration(baseBeats: 1, marks: durationMarks)
        let weight = notes.reduce(0.0) { $0 + $1.durationBeats }
        guard weight > 0 else {
            return
        }

        let multiplier = totalDurationBeats / weight
        for note in notes {
            let noteDurationBeats = note.durationBeats * multiplier
            let durationMilliseconds = max(1, Int((noteDurationBeats * context.beatMilliseconds).rounded()))
            let start = max(0, Int(context.offsetMilliseconds.rounded()))
            if let midiNote = note.midiNote, midiNote > 0 {
                context.events.append(NoteEvent(startMilliseconds: start, durationMilliseconds: durationMilliseconds, midiNote: midiNote))
            }
            context.offsetMilliseconds += Double(durationMilliseconds)
            context.lastNoteDurationMilliseconds = durationMilliseconds
        }

        context.totalBeats += totalDurationBeats
        context.arpeggioAccumulatedMilliseconds = 0
    }

    private func duration(baseBeats: Double, marks: String) -> Double {
        guard !marks.isEmpty else {
            return baseBeats
        }

        var result = baseBeats
        var lastBase = baseBeats
        var index = marks.startIndex

        while index < marks.endIndex {
            let mark = marks[index]
            var count = 0
            while index < marks.endIndex && marks[index] == mark {
                count += 1
                index = marks.index(after: index)
            }

            switch mark {
            case "/":
                let next = lastBase / pow(2.0, Double(count))
                result = result - lastBase + next
                lastBase = next
            case "-":
                result += Double(count)
                lastBase = 1
            case ".":
                var dotBase = lastBase
                for _ in 0..<count {
                    dotBase *= 0.5
                    result += dotBase
                }
            default:
                break
            }
        }

        return max(0, result)
    }

    private func midiNote(forKeyControl keyControl: String) -> Int? {
        let pattern = #"(?i)^([A-G])(\d{0,2})([#b]?)$"#
        guard let match = firstMatch(in: keyControl, pattern: pattern) else {
            return nil
        }

        let noteName = match[1].uppercased()
        let octave = Int(match[2].isEmpty ? "5" : match[2]) ?? 5
        let accidental = match[3]
        let base = [
            "C": 0,
            "D": 2,
            "E": 4,
            "F": 5,
            "G": 7,
            "A": 9,
            "B": 11
        ][noteName]

        guard var midi = base.map({ octave * 12 + $0 }) else {
            return nil
        }
        if accidental == "#" {
            midi += 1
        } else if accidental.lowercased() == "b" {
            midi -= 1
        }
        return midi
    }

    private func firstCapture(in source: String, pattern: String) -> String? {
        firstMatch(in: source, pattern: pattern)?.dropFirst().first
    }

    private func firstMatch(in source: String, pattern: String) -> [String]? {
        guard let regex = try? NSRegularExpression(pattern: pattern) else {
            return nil
        }
        let range = NSRange(source.startIndex..<source.endIndex, in: source)
        guard let match = regex.firstMatch(in: source, range: range) else {
            return nil
        }

        return (0..<match.numberOfRanges).map { index in
            let nsRange = match.range(at: index)
            guard nsRange.location != NSNotFound, let range = Range(nsRange, in: source) else {
                return ""
            }
            return String(source[range])
        }
    }
}

private enum GroupMode {
    case chord
    case multiplet
}

private struct ParsedTokenNote {
    let midiNote: Int?
    let durationBeats: Double
    let arpeggio: Bool
}

private struct ParseContext {
    var baseMidi = 60
    var beatMilliseconds = 60000.0 / 80.0
    var offsetMilliseconds = 0.0
    var totalBeats = 0.0
    var events: [NoteEvent] = []
    var diagnostics: [DomisoDiagnostic] = []
    var lastNoteDurationMilliseconds = 0
    var arpeggioAccumulatedMilliseconds = 0
}
