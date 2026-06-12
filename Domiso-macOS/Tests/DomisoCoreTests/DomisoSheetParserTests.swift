import XCTest
@testable import DomisoCore

final class DomisoSheetParserTests: XCTestCase {
    func testParsesBasicScaleAtDefaultTempo() {
        let parsed = DomisoSheetParser().parse("1 2 3 4 5 6 7 +1")

        XCTAssertEqual(parsed.noteEvents.map(\.midiNote), [60, 62, 64, 65, 67, 69, 71, 72])
        XCTAssertEqual(parsed.noteEvents.first?.startMilliseconds, 0)
        XCTAssertEqual(parsed.noteEvents.first?.durationMilliseconds, 750)
        XCTAssertEqual(parsed.totalMilliseconds, 6000)
    }

    func testBPMAndDurationMarkers() {
        let parsed = DomisoSheetParser().parse("bpm=120\n5.. 6/")

        XCTAssertEqual(parsed.noteEvents.count, 2)
        XCTAssertEqual(parsed.noteEvents[0].durationMilliseconds, 875)
        XCTAssertEqual(parsed.noteEvents[1].startMilliseconds, 875)
        XCTAssertEqual(parsed.noteEvents[1].durationMilliseconds, 250)
    }

    func testChordUsesLongestInnerDurationAndOuterMarks() {
        let parsed = DomisoSheetParser().parse("( 1 3/ 5 )--")

        XCTAssertEqual(parsed.noteEvents.count, 3)
        XCTAssertEqual(Set(parsed.noteEvents.map(\.startMilliseconds)), Set([0]))
        XCTAssertEqual(Set(parsed.noteEvents.map(\.durationMilliseconds)), Set([2250]))
    }

    func testTupletDistributesOneBeatByDefault() {
        let parsed = DomisoSheetParser().parse("{ 1 3 5 }")

        XCTAssertEqual(parsed.noteEvents.count, 3)
        XCTAssertEqual(parsed.noteEvents.map(\.startMilliseconds), [0, 250, 500])
        XCTAssertEqual(parsed.noteEvents.map(\.durationMilliseconds), [250, 250, 250])
    }

    func testRollbackCreatesOverlappingVoice() {
        let parsed = DomisoSheetParser().parse("""
        1 2
        rollback=2
        3 4
        """)

        XCTAssertEqual(parsed.noteEvents.map(\.startMilliseconds), [0, 0, 750, 750])
        XCTAssertEqual(parsed.noteEvents.map(\.midiNote), [60, 64, 62, 65])
    }

    func testZeroIsRest() {
        let parsed = DomisoSheetParser().parse("1 0 2")

        XCTAssertEqual(parsed.noteEvents.map(\.midiNote), [60, 62])
        XCTAssertEqual(parsed.noteEvents.map(\.startMilliseconds), [0, 1500])
    }

    func testKeyMapBuildsDomiso36Plan() {
        let parsed = DomisoSheetParser().parse("1 1# 2 3b")
        let plan = DomisoKeyMap.domiso36.playbackPlan(for: parsed, speedPercent: 100, sameKeyMinimumGapMilliseconds: 20)

        XCTAssertEqual(plan.ignoredNoteCount, 0)
        XCTAssertEqual(plan.events.map { $0.keyStroke.displayName }, ["a", "Shift+a", "s", "Ctrl+d"])
    }
}
