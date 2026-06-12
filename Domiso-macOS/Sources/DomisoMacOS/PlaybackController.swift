import Combine
import DomisoCore
import Foundation

@MainActor
final class PlaybackController: ObservableObject {
    enum State: String {
        case stopped = "Stopped"
        case playing = "Playing"
        case paused = "Paused"
    }

    @Published private(set) var state: State = .stopped
    @Published var positionMilliseconds: Int = 0
    @Published var totalMilliseconds: Int = 0

    var holdMinimumMilliseconds = 150

    private let sink: KeyboardEventSink
    private var task: Task<Void, Never>?
    private var activeKeys: Set<DomisoKeyStroke> = []

    init(sink: KeyboardEventSink = MacKeyboardEventSink()) {
        self.sink = sink
    }

    func load(totalMilliseconds: Int) {
        self.totalMilliseconds = totalMilliseconds
        if positionMilliseconds > totalMilliseconds {
            positionMilliseconds = 0
        }
    }

    func play(events: [ScheduledKeyEvent], from offset: Int? = nil) {
        stopReleasingKeys(updateState: false)
        let startOffset = max(0, min(offset ?? positionMilliseconds, totalMilliseconds))
        positionMilliseconds = startOffset
        state = .playing

        let actions = buildActions(events: events, startOffset: startOffset)
        task = Task { [weak self] in
            await self?.run(actions: actions, startOffset: startOffset)
        }
    }

    func pause() {
        guard state == .playing else {
            return
        }
        task?.cancel()
        task = nil
        releaseActiveKeys()
        state = .paused
    }

    func stop() {
        stopReleasingKeys(updateState: true)
        positionMilliseconds = 0
    }

    func seek(to milliseconds: Int) {
        positionMilliseconds = max(0, min(milliseconds, totalMilliseconds))
    }

    private func stopReleasingKeys(updateState: Bool) {
        task?.cancel()
        task = nil
        releaseActiveKeys()
        sink.releaseAllKnownKeys()
        if updateState {
            state = .stopped
        }
    }

    private func releaseActiveKeys() {
        for key in activeKeys {
            sink.keyUp(key)
        }
        activeKeys.removeAll()
    }

    private func run(actions: [PlaybackAction], startOffset: Int) async {
        let clock = ContinuousClock()
        let startInstant = clock.now

        for action in actions {
            if Task.isCancelled {
                break
            }

            let waitMilliseconds = max(0, action.timeMilliseconds - startOffset)
            let target = startInstant + .milliseconds(waitMilliseconds)
            do {
                try await clock.sleep(until: target)
            } catch {
                break
            }

            if Task.isCancelled {
                break
            }

            perform(action)
            positionMilliseconds = min(totalMilliseconds, action.timeMilliseconds)
        }

        releaseActiveKeys()
        if !Task.isCancelled {
            positionMilliseconds = totalMilliseconds
            state = .stopped
        }
    }

    private func perform(_ action: PlaybackAction) {
        switch action.kind {
        case .tap:
            sink.tap(action.keyStroke)
        case .down:
            sink.keyDown(action.keyStroke)
            activeKeys.insert(action.keyStroke)
        case .up:
            sink.keyUp(action.keyStroke)
            activeKeys.remove(action.keyStroke)
        }
    }

    private func buildActions(events: [ScheduledKeyEvent], startOffset: Int) -> [PlaybackAction] {
        var actions: [PlaybackAction] = []

        for event in events {
            if event.endMilliseconds <= startOffset {
                continue
            }

            if event.durationMilliseconds >= holdMinimumMilliseconds {
                let downTime = max(event.startMilliseconds, startOffset)
                actions.append(PlaybackAction(timeMilliseconds: downTime, keyStroke: event.keyStroke, kind: .down))
                actions.append(PlaybackAction(timeMilliseconds: event.endMilliseconds, keyStroke: event.keyStroke, kind: .up))
            } else if event.startMilliseconds >= startOffset {
                actions.append(PlaybackAction(timeMilliseconds: event.startMilliseconds, keyStroke: event.keyStroke, kind: .tap))
            }
        }

        actions.sort { lhs, rhs in
            if lhs.timeMilliseconds == rhs.timeMilliseconds {
                return lhs.kind.priority < rhs.kind.priority
            }
            return lhs.timeMilliseconds < rhs.timeMilliseconds
        }
        return actions
    }
}

private struct PlaybackAction: Equatable {
    enum Kind: Equatable {
        case tap
        case down
        case up

        var priority: Int {
            switch self {
            case .up:
                return 0
            case .tap:
                return 1
            case .down:
                return 2
            }
        }
    }

    let timeMilliseconds: Int
    let keyStroke: DomisoKeyStroke
    let kind: Kind
}
