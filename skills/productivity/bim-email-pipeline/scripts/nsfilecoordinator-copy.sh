#!/bin/bash
# nsfilecoordinator-copy.sh — Read a provenance-locked iCloud file via NSFileCoordinator
# and copy it to a destination (OneDrive BIM target or any writable path).
#
# Usage:
#   ./nsfilecoordinator-copy.sh <source_path> <dest_path>
#
# This works where cp, dd, shutil.copy2, and Python os.open() all fail with
# [Errno 11] Resource deadlock avoided on macOS iCloud/OneDrive provenance files.
#
# How it works:
#   1. Generates a temporary Swift script that uses NSFileCoordinator to read the source
#   2. Writes read content to /tmp/<basename>.nscoord.tmp
#   3. Copies from /tmp to the destination (regular cp works on non-provenance path)
#   4. Cleans up
#
# Exit codes:
#   0 — success
#   1 — source not found
#   2 — Swift read failed (source still locked or iCloud deadlock systemic)
#   3 — destination write failed

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <source_path> <dest_path>"
    exit 1
fi

SRC="$1"
DST="$2"

if [ ! -f "$SRC" ]; then
    echo "ERROR: Source not found: $SRC" >&2
    exit 1
fi

BASENAME=$(basename "$SRC")
TMP_OUT="/tmp/${BASENAME}.nscoord.tmp"
SWIFT_SCRIPT="/tmp/_nscoord_read_$$.swift"

cat > "$SWIFT_SCRIPT" << 'SWIFT'
import Foundation

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("Usage: swift <script> <source> <dest>")
    exit(1)
}

let src = URL(fileURLWithPath: args[1])
let dst = URL(fileURLWithPath: args[2])

let coordinator = NSFileCoordinator(filePresenter: nil)
var coordError: NSError?

coordinator.coordinate(readingItemAt: src, options: .withoutChanges, error: &coordError) { readURL in
    do {
        let data = try Data(contentsOf: readURL)
        try data.write(to: dst)
        print("OK: \(data.count) bytes -> \(dst.path)")
    } catch {
        print("FAIL: \(error)")
        exit(2)
    }
}

if let err = coordError {
    print("COORD_FAIL: \(err)")
    exit(2)
}
SWIFT

# Read via Swift NSFileCoordinator to /tmp
swift "$SWIFT_SCRIPT" "$SRC" "$TMP_OUT" 2>&1
SWIFT_EXIT=$?

rm -f "$SWIFT_SCRIPT"

if [ "$SWIFT_EXIT" -ne 0 ]; then
    echo "ERROR: NSFileCoordinator read failed (exit $SWIFT_EXIT)" >&2
    rm -f "$TMP_OUT"
    exit 2
fi

# Copy from /tmp to destination
cp "$TMP_OUT" "$DST" 2>&1
CP_EXIT=$?
rm -f "$TMP_OUT"

if [ "$CP_EXIT" -ne 0 ]; then
    echo "ERROR: cp to destination failed (exit $CP_EXIT)" >&2
    exit 3
fi

echo "COPIED: $SRC -> $DST"
exit 0
