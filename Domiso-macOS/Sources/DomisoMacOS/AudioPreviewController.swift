import AudioToolbox
import AVFoundation
import Combine
import DomisoCore
import Foundation

@MainActor
final class AudioPreviewController: ObservableObject {
    enum State: String {
        case stopped = "Stopped"
        case playing = "Listening"
        case paused = "Paused"
    }

    @Published private(set) var state: State = .stopped
    @Published var positionMilliseconds: Int = 0
    @Published var totalMilliseconds: Int = 0

    private let engine = AVAudioEngine()
    private let sampler = AVAudioUnitSampler()
    private var task: Task<Void, Never>?
    private var activeNotes: Set<UInt8> = []
    private var isPrepared = false

    func load(totalMilliseconds: Int) {
        self.totalMilliseconds = totalMilliseconds
        if positionMilliseconds > totalMilliseconds {
            positionMilliseconds = 0
        }
    }

    func play(events: [NoteEvent], from offset: Int? = nil) {
        stop(updateState: false)
        let startOffset = max(0, min(offset ?? positionMilliseconds, totalMilliseconds))
        positionMilliseconds = startOffset
        state = .playing

        do {
            try prepareIfNeeded()
        } catch {
            state = .stopped
            return
        }

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
        releaseActiveNotes()
        state = .paused
    }

    func stop() {
        stop(updateState: true)
        positionMilliseconds = 0
    }

    func seek(to milliseconds: Int) {
        positionMilliseconds = max(0, min(milliseconds, totalMilliseconds))
    }

    private func stop(updateState: Bool) {
        task?.cancel()
        task = nil
        releaseActiveNotes()
        if updateState {
            state = .stopped
        }
    }

    private func prepareIfNeeded() throws {
        guard !isPrepared else {
            return
        }

        engine.attach(sampler)
        engine.connect(sampler, to: engine.mainMixerNode, format: nil)

        let soundBank = URL(fileURLWithPath: "/System/Library/Components/CoreAudio.component/Contents/Resources/gs_instruments.dls")
        if FileManager.default.fileExists(atPath: soundBank.path) {
            try sampler.loadSoundBankInstrument(
                at: soundBank,
                program: UInt8(0),
                bankMSB: UInt8(kAUSampler_DefaultMelodicBankMSB),
                bankLSB: UInt8(kAUSampler_DefaultBankLSB)
            )
        }

        try engine.start()
        isPrepared = true
    }

    private func run(actions: [PreviewAction], startOffset: Int) async {
        let clock = ContinuousClock()
        let startInstant = clock.now

        for action in actions {
            if Task.isCancelled {
                break
            }

            let waitMilliseconds = max(0, action.timeMilliseconds - startOffset)
            do {
                try await clock.sleep(until: startInstant + .milliseconds(waitMilliseconds))
            } catch {
                break
            }

            if Task.isCancelled {
                break
            }

            perform(action)
            positionMilliseconds = min(totalMilliseconds, action.timeMilliseconds)
        }

        releaseActiveNotes()
        if !Task.isCancelled {
            positionMilliseconds = totalMilliseconds
            state = .stopped
        }
    }

    private func perform(_ action: PreviewAction) {
        switch action.kind {
        case .down:
            sampler.startNote(action.note, withVelocity: 72, onChannel: 0)
            activeNotes.insert(action.note)
        case .up:
            sampler.stopNote(action.note, onChannel: 0)
            activeNotes.remove(action.note)
        }
    }

    private func releaseActiveNotes() {
        for note in activeNotes {
            sampler.stopNote(note, onChannel: 0)
        }
        activeNotes.removeAll()
    }

    private func buildActions(events: [NoteEvent], startOffset: Int) -> [PreviewAction] {
        var actions: [PreviewAction] = []

        for event in events {
            guard event.endMilliseconds > startOffset, (0...127).contains(event.midiNote) else {
                continue
            }

            let note = UInt8(event.midiNote)
            actions.append(PreviewAction(timeMilliseconds: max(event.startMilliseconds, startOffset), note: note, kind: .down))
            actions.append(PreviewAction(timeMilliseconds: event.endMilliseconds, note: note, kind: .up))
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

private struct PreviewAction: Equatable {
    enum Kind: Equatable {
        case down
        case up

        var priority: Int {
            switch self {
            case .up:
                return 0
            case .down:
                return 1
            }
        }
    }

    let timeMilliseconds: Int
    let note: UInt8
    let kind: Kind
}
