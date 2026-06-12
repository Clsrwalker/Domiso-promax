import ApplicationServices
import DomisoCore
import Foundation

protocol KeyboardEventSink {
    func tap(_ stroke: DomisoKeyStroke)
    func keyDown(_ stroke: DomisoKeyStroke)
    func keyUp(_ stroke: DomisoKeyStroke)
    func releaseAllKnownKeys()
}

final class MacKeyboardEventSink: KeyboardEventSink {
    private let keyCodes: [String: CGKeyCode] = [
        "a": 0,
        "s": 1,
        "d": 2,
        "f": 3,
        "h": 4,
        "g": 5,
        "z": 6,
        "x": 7,
        "c": 8,
        "v": 9,
        "b": 11,
        "q": 12,
        "w": 13,
        "e": 14,
        "r": 15,
        "y": 16,
        "t": 17,
        "u": 32,
        "j": 38,
        "n": 45,
        "m": 46
    ]

    private let modifierCodes: [DomisoKeyModifier: CGKeyCode] = [
        .shift: 56,
        .control: 59
    ]

    func tap(_ stroke: DomisoKeyStroke) {
        if let modifier = stroke.modifier {
            sendModifier(modifier, keyDown: true)
            sendKey(stroke.key, keyDown: true)
            sendKey(stroke.key, keyDown: false)
            sendModifier(modifier, keyDown: false)
        } else {
            sendKey(stroke.key, keyDown: true)
            sendKey(stroke.key, keyDown: false)
        }
    }

    func keyDown(_ stroke: DomisoKeyStroke) {
        if let modifier = stroke.modifier {
            sendModifier(modifier, keyDown: true)
            sendKey(stroke.key, keyDown: true)
            sendModifier(modifier, keyDown: false)
        } else {
            sendKey(stroke.key, keyDown: true)
        }
    }

    func keyUp(_ stroke: DomisoKeyStroke) {
        sendKey(stroke.key, keyDown: false)
    }

    func releaseAllKnownKeys() {
        for key in keyCodes.keys {
            sendKey(key, keyDown: false)
        }
        for modifier in modifierCodes.keys {
            sendModifier(modifier, keyDown: false)
        }
    }

    private func sendModifier(_ modifier: DomisoKeyModifier, keyDown: Bool) {
        guard let code = modifierCodes[modifier] else {
            return
        }
        post(code: code, keyDown: keyDown)
    }

    private func sendKey(_ key: String, keyDown: Bool) {
        guard let code = keyCodes[key.lowercased()] else {
            return
        }
        post(code: code, keyDown: keyDown)
    }

    private func post(code: CGKeyCode, keyDown: Bool) {
        guard let event = CGEvent(keyboardEventSource: nil, virtualKey: code, keyDown: keyDown) else {
            return
        }
        event.post(tap: .cgSessionEventTap)
    }
}

enum AccessibilityPermission {
    static func isTrusted(prompt: Bool = false) -> Bool {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: prompt] as CFDictionary
        return AXIsProcessTrustedWithOptions(options)
    }
}
