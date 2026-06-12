import Foundation

public enum DomisoDiagnosticSeverity: String, Hashable, Sendable {
    case info
    case warning
}

public struct DomisoDiagnostic: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let line: Int
    public let message: String
    public let severity: DomisoDiagnosticSeverity

    public init(line: Int, message: String, severity: DomisoDiagnosticSeverity = .warning) {
        self.id = UUID()
        self.line = line
        self.message = message
        self.severity = severity
    }

    public static func == (lhs: DomisoDiagnostic, rhs: DomisoDiagnostic) -> Bool {
        lhs.line == rhs.line &&
            lhs.message == rhs.message &&
            lhs.severity == rhs.severity
    }
}

public struct NoteEvent: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let startMilliseconds: Int
    public let durationMilliseconds: Int
    public let midiNote: Int

    public init(startMilliseconds: Int, durationMilliseconds: Int, midiNote: Int) {
        self.id = UUID()
        self.startMilliseconds = startMilliseconds
        self.durationMilliseconds = durationMilliseconds
        self.midiNote = midiNote
    }

    public var endMilliseconds: Int {
        startMilliseconds + durationMilliseconds
    }

    public static func == (lhs: NoteEvent, rhs: NoteEvent) -> Bool {
        lhs.startMilliseconds == rhs.startMilliseconds &&
            lhs.durationMilliseconds == rhs.durationMilliseconds &&
            lhs.midiNote == rhs.midiNote
    }
}

public enum DomisoKeyModifier: String, Hashable, Sendable {
    case shift = "Shift"
    case control = "Ctrl"
}

public struct DomisoKeyStroke: Hashable, Sendable {
    public let key: String
    public let modifier: DomisoKeyModifier?

    public init(key: String, modifier: DomisoKeyModifier? = nil) {
        self.key = key.lowercased()
        self.modifier = modifier
    }

    public var displayName: String {
        if let modifier {
            return "\(modifier.rawValue)+\(key)"
        }
        return key
    }
}

public struct ScheduledKeyEvent: Identifiable, Equatable, Sendable {
    public let id: UUID
    public var startMilliseconds: Int
    public var durationMilliseconds: Int
    public let midiNote: Int
    public let keyStroke: DomisoKeyStroke

    public init(startMilliseconds: Int, durationMilliseconds: Int, midiNote: Int, keyStroke: DomisoKeyStroke) {
        self.id = UUID()
        self.startMilliseconds = startMilliseconds
        self.durationMilliseconds = durationMilliseconds
        self.midiNote = midiNote
        self.keyStroke = keyStroke
    }

    public var endMilliseconds: Int {
        startMilliseconds + durationMilliseconds
    }

    public static func == (lhs: ScheduledKeyEvent, rhs: ScheduledKeyEvent) -> Bool {
        lhs.startMilliseconds == rhs.startMilliseconds &&
            lhs.durationMilliseconds == rhs.durationMilliseconds &&
            lhs.midiNote == rhs.midiNote &&
            lhs.keyStroke == rhs.keyStroke
    }
}

public struct PlaybackOptimizationReport: Equatable, Sendable {
    public let eventCount: Int
    public let mergedCount: Int
    public let peakPerSecond: Int
    public let minimumGapMilliseconds: Int

    public init(eventCount: Int, mergedCount: Int, peakPerSecond: Int, minimumGapMilliseconds: Int) {
        self.eventCount = eventCount
        self.mergedCount = mergedCount
        self.peakPerSecond = peakPerSecond
        self.minimumGapMilliseconds = minimumGapMilliseconds
    }
}

public struct DomisoParsedSheet: Equatable, Sendable {
    public let noteEvents: [NoteEvent]
    public let totalBeats: Double
    public let totalMilliseconds: Int
    public let diagnostics: [DomisoDiagnostic]

    public init(noteEvents: [NoteEvent], totalBeats: Double, totalMilliseconds: Int, diagnostics: [DomisoDiagnostic]) {
        self.noteEvents = noteEvents
        self.totalBeats = totalBeats
        self.totalMilliseconds = totalMilliseconds
        self.diagnostics = diagnostics
    }
}

public struct DomisoPlaybackPlan: Equatable, Sendable {
    public let events: [ScheduledKeyEvent]
    public let ignoredNoteCount: Int
    public let report: PlaybackOptimizationReport

    public init(events: [ScheduledKeyEvent], ignoredNoteCount: Int, report: PlaybackOptimizationReport) {
        self.events = events
        self.ignoredNoteCount = ignoredNoteCount
        self.report = report
    }
}
