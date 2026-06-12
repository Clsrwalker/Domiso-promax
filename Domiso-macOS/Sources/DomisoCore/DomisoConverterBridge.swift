import Foundation

public struct DomisoConversionResult: Equatable, Sendable {
    public let log: String
    public let outputFiles: [URL]

    public init(log: String, outputFiles: [URL]) {
        self.log = log
        self.outputFiles = outputFiles
    }
}

public struct DomisoConverterBridge: Sendable {
    public let toolsDirectory: URL?

    public init(toolsDirectory: URL? = nil) {
        self.toolsDirectory = toolsDirectory
    }

    public func convert(midiURL: URL, outputDirectory: URL) async throws -> DomisoConversionResult {
        let script = try locateGenerateScript()
        try FileManager.default.createDirectory(at: outputDirectory, withIntermediateDirectories: true, attributes: nil)

        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        process.arguments = [
            "python3",
            script.path,
            midiURL.path,
            "--target",
            "yihuan",
            "--out-dir",
            outputDirectory.path,
            "--report-dir",
            outputDirectory.path
        ]

        let pipe = Pipe()
        process.standardOutput = pipe
        process.standardError = pipe

        try process.run()
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        process.waitUntilExit()
        let log = String(data: data, encoding: .utf8) ?? String(data: data, encoding: .isoLatin1) ?? ""

        guard process.terminationStatus == 0 else {
            throw DomisoConversionError.processFailed(Int(process.terminationStatus), log)
        }

        let outputs = log
            .split(separator: "\n")
            .compactMap { line -> URL? in
                guard line.hasPrefix("OUTPUT=") else {
                    return nil
                }
                let path = String(line.dropFirst("OUTPUT=".count)).trimmingCharacters(in: .whitespacesAndNewlines)
                return path.isEmpty ? nil : URL(fileURLWithPath: path)
            }
            .filter { $0.pathExtension.lowercased() == "txt" }

        return DomisoConversionResult(log: log, outputFiles: outputs)
    }

    public func locateGenerateScript() throws -> URL {
        let fileManager = FileManager.default
        var candidates: [URL] = []

        if let toolsDirectory {
            candidates.append(toolsDirectory.appendingPathComponent("domiso_generate_select.py"))
        }

        if let envTools = ProcessInfo.processInfo.environment["DOMISO_TOOLS_DIR"], !envTools.isEmpty {
            candidates.append(URL(fileURLWithPath: envTools).appendingPathComponent("domiso_generate_select.py"))
        }

        let cwd = URL(fileURLWithPath: fileManager.currentDirectoryPath)
        candidates.append(cwd.appendingPathComponent("../tools/domiso_generate_select.py").standardizedFileURL)
        candidates.append(cwd.appendingPathComponent("../../tools/domiso_generate_select.py").standardizedFileURL)
        candidates.append(cwd.appendingPathComponent("tools/domiso_generate_select.py").standardizedFileURL)

        for candidate in candidates where fileManager.fileExists(atPath: candidate.path) {
            return candidate
        }

        throw DomisoConversionError.generateScriptNotFound(candidates.map(\.path))
    }
}

public enum DomisoConversionError: LocalizedError, Equatable, Sendable {
    case generateScriptNotFound([String])
    case processFailed(Int, String)

    public var errorDescription: String? {
        switch self {
        case .generateScriptNotFound(let candidates):
            return "domiso_generate_select.py was not found. Checked: \(candidates.joined(separator: ", "))"
        case .processFailed(let code, let log):
            return "Conversion failed with exit code \(code).\n\(log)"
        }
    }
}
