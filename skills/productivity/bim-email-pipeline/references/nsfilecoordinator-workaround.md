# NSFileCoordinator Workaround for iCloud Dataless Files

Confirmed: 2026-06-10 during automated cron pipeline run (32 files unreadable via POSIX, all succeeded via NSFileCoordinator).

## Problem

iCloud Drive files under `~/Documents/Documents - Mohamed's MacBook Pro/` that have the `compressed,dataless` APFS flag are **unreadable** via standard POSIX tools:
- `cat` → silently produces 0-byte output
- `cp`, `dd`, `ditto` → `Resource deadlock avoided` (fcopyfile failure)
- Python `open()` → `OSError: [Errno 35] Resource deadlock avoided`
- `brctl download` → permission errors from non-GUI contexts

Apple's `NSFileCoordinator` API takes a different code path through the kernel's `fileprovi` hydration engine, succeeding when all POSIX tools fail.

## Swift Implementation Template

Create a Swift file (e.g., `copy_coordinated.swift`) and compile/run with `swift`:

```swift
import Foundation

// Usage: swift copy_coordinated.swift <source_path> <dest_path>
let args = CommandLine.arguments
guard args.count == 3 else {
    print("Usage: copy_coordinated <source> <dest>")
    exit(1)
}

let srcPath = args[1]
let destPath = args[2]
let srcURL = URL(fileURLWithPath: srcPath)
let destURL = URL(fileURLWithPath: destPath)
let semaphore = DispatchSemaphore(value: 0)
var success = false

let coordinator = NSFileCoordinator(filePresenter: nil)
var coordinationError: NSError?

coordinator.coordinate(readingItemAt: srcURL, options: .withoutChanges, error: &coordinationError) { (readingURL) in
    do {
        try FileManager.default.copyItem(at: readingURL, to: destURL)
        success = true
    } catch {
        // Fallback: read data then write
        do {
            let data = try Data(contentsOf: readingURL)
            try data.write(to: destURL)
            success = true
        } catch {
            print("ERROR reading/writing: \(error.localizedDescription)")
        }
    }
    semaphore.signal()
}

if let err = coordinationError {
    print("COORDINATION ERROR: \(err.localizedDescription)")
    semaphore.signal()
}

semaphore.wait()

if success {
    // Verify destination
    if let attrs = try? FileManager.default.attributesOfItem(atPath: destPath),
       let fileSize = attrs[.size] as? UInt64, fileSize > 0 {
        print("OK: \(fileSize) bytes copied to \(destPath)")
    } else {
        print("WARNING: copy reported success but dest is empty or missing")
    }
} else {
    print("FAILED: could not read source")
    exit(1)
}
```

## Running

```bash
# Compile and run (no Xcode needed — Foundation is built-in on macOS)
swift /tmp/copy_coordinated.swift "/path/to/dataless/source.pdf" "/tmp/output.pdf"

# For batch processing from Python:
import subprocess
result = subprocess.run([
    'swift', '/tmp/copy_coordinated.swift', src_path, tmp_path
], capture_output=True, text=True, timeout=60)
```

## How It Works

`NSFileCoordinator` uses Apple's file coordination system which:
1. Acquires a file coordination lock from the `fileprovi` (File Provider) daemon
2. Requests the daemon to hydrate the file content before reading
3. Provides a temporary URL backed by fully local content

The standard POSIX `read()` syscall cannot trigger this hydration path — it returns `EDEADLK` immediately instead of waiting for hydration. The coordination API is designed for this case.

## Detection Before Attempting

Check if a file needs this treatment:

```bash
stat -f "%N: %Sf" "$file"
# compressed,dataless → needs NSFileCoordinator
# -                    → fully local, POSIX tools work
```

## Notes

- Requires Swift runtime (`/usr/bin/swift`), which is pre-installed on all modern macOS
- Filesystem permissions must allow the Swift process to access the iCloud Drive directory (user-level access is sufficient — no SIP disabling needed)
- OneDrive files with `Resource deadlock avoided` may also benefit from this approach, but the `cat|mv` workaround is simpler for OneDrive
- Tested on macOS Sequoia (26.5.1) with Swift 5.x
