// swift-tools-version: 5.9

import PackageDescription

let package = Package(
    name: "DomisoMacOS",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(name: "DomisoMacOS", targets: ["DomisoMacOS"])
    ],
    targets: [
        .target(
            name: "DomisoCore"
        ),
        .executableTarget(
            name: "DomisoMacOS",
            dependencies: ["DomisoCore"]
        ),
        .testTarget(
            name: "DomisoCoreTests",
            dependencies: ["DomisoCore"]
        )
    ]
)
