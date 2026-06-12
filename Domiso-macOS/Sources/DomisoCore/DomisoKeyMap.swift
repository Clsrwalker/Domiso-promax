import Foundation

public struct DomisoKeyMap: Sendable {
    public let midiToKey: [Int: DomisoKeyStroke]

    public init(midiToKey: [Int: DomisoKeyStroke]) {
        self.midiToKey = midiToKey
    }

    public static let domiso36 = DomisoKeyMap(midiToKey: [
        48: DomisoKeyStroke(key: "z"),
        50: DomisoKeyStroke(key: "x"),
        52: DomisoKeyStroke(key: "c"),
        53: DomisoKeyStroke(key: "v"),
        55: DomisoKeyStroke(key: "b"),
        57: DomisoKeyStroke(key: "n"),
        59: DomisoKeyStroke(key: "m"),
        60: DomisoKeyStroke(key: "a"),
        62: DomisoKeyStroke(key: "s"),
        64: DomisoKeyStroke(key: "d"),
        65: DomisoKeyStroke(key: "f"),
        67: DomisoKeyStroke(key: "g"),
        69: DomisoKeyStroke(key: "h"),
        71: DomisoKeyStroke(key: "j"),
        72: DomisoKeyStroke(key: "q"),
        74: DomisoKeyStroke(key: "w"),
        76: DomisoKeyStroke(key: "e"),
        77: DomisoKeyStroke(key: "r"),
        79: DomisoKeyStroke(key: "t"),
        81: DomisoKeyStroke(key: "y"),
        83: DomisoKeyStroke(key: "u"),

        49: DomisoKeyStroke(key: "z", modifier: .shift),
        51: DomisoKeyStroke(key: "c", modifier: .control),
        54: DomisoKeyStroke(key: "v", modifier: .shift),
        56: DomisoKeyStroke(key: "b", modifier: .shift),
        58: DomisoKeyStroke(key: "m", modifier: .control),
        61: DomisoKeyStroke(key: "a", modifier: .shift),
        63: DomisoKeyStroke(key: "d", modifier: .control),
        66: DomisoKeyStroke(key: "f", modifier: .shift),
        68: DomisoKeyStroke(key: "g", modifier: .shift),
        70: DomisoKeyStroke(key: "j", modifier: .control),
        73: DomisoKeyStroke(key: "q", modifier: .shift),
        75: DomisoKeyStroke(key: "e", modifier: .control),
        78: DomisoKeyStroke(key: "r", modifier: .shift),
        80: DomisoKeyStroke(key: "t", modifier: .shift),
        82: DomisoKeyStroke(key: "u", modifier: .control)
    ])

    public func playbackPlan(
        for parsedSheet: DomisoParsedSheet,
        speedPercent: Double = 95,
        sameKeyMinimumGapMilliseconds: Int = 110
    ) -> DomisoPlaybackPlan {
        let scale = speedPercent > 0 ? 100.0 / speedPercent : 1.0
        var ignored = 0
        var rawEvents: [ScheduledKeyEvent] = []

        for event in parsedSheet.noteEvents {
            guard let keyStroke = midiToKey[event.midiNote] else {
                ignored += 1
                continue
            }
            rawEvents.append(ScheduledKeyEvent(
                startMilliseconds: Int((Double(event.startMilliseconds) * scale).rounded()),
                durationMilliseconds: max(1, Int((Double(event.durationMilliseconds) * scale).rounded())),
                midiNote: event.midiNote,
                keyStroke: keyStroke
            ))
        }

        rawEvents.sort {
            if $0.startMilliseconds == $1.startMilliseconds {
                return $0.keyStroke.displayName < $1.keyStroke.displayName
            }
            return $0.startMilliseconds < $1.startMilliseconds
        }

        let optimized = Self.mergeCloseSameKeyEvents(rawEvents, minimumGapMilliseconds: sameKeyMinimumGapMilliseconds)
        let report = Self.buildReport(events: optimized.events, mergedCount: optimized.mergedCount)
        return DomisoPlaybackPlan(events: optimized.events, ignoredNoteCount: ignored, report: report)
    }

    private static func mergeCloseSameKeyEvents(
        _ events: [ScheduledKeyEvent],
        minimumGapMilliseconds: Int
    ) -> (events: [ScheduledKeyEvent], mergedCount: Int) {
        var output: [ScheduledKeyEvent] = []
        var lastIndexByKey: [DomisoKeyStroke: Int] = [:]
        var merged = 0

        for event in events {
            if let previousIndex = lastIndexByKey[event.keyStroke] {
                let previous = output[previousIndex]
                let gap = event.startMilliseconds - previous.startMilliseconds
                if gap < minimumGapMilliseconds {
                    let newEnd = max(previous.endMilliseconds, event.endMilliseconds)
                    output[previousIndex].durationMilliseconds = max(1, newEnd - previous.startMilliseconds)
                    merged += 1
                    continue
                }
            }
            output.append(event)
            lastIndexByKey[event.keyStroke] = output.count - 1
        }

        return (output, merged)
    }

    private static func buildReport(events: [ScheduledKeyEvent], mergedCount: Int) -> PlaybackOptimizationReport {
        guard !events.isEmpty else {
            return PlaybackOptimizationReport(eventCount: 0, mergedCount: mergedCount, peakPerSecond: 0, minimumGapMilliseconds: 0)
        }

        var peak = 0
        var windowStart = 0
        var minimumGap = Int.max

        for index in events.indices {
            while windowStart < index && events[index].startMilliseconds - events[windowStart].startMilliseconds > 1000 {
                windowStart += 1
            }
            peak = max(peak, index - windowStart + 1)
            if index > events.startIndex {
                minimumGap = min(minimumGap, events[index].startMilliseconds - events[index - 1].startMilliseconds)
            }
        }

        return PlaybackOptimizationReport(
            eventCount: events.count,
            mergedCount: mergedCount,
            peakPerSecond: peak,
            minimumGapMilliseconds: minimumGap == Int.max ? 0 : minimumGap
        )
    }
}
