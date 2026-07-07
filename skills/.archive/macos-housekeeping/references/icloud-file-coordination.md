# iCloud Drive File Coordination Locks

When files live in the iCloud-synced `~/Documents/Documents - <Device Name>/` tree, macOS's `bird` daemon may hold a file coordination lock that makes files **unreadable through normal POSIX methods**.

## Diagnostic Reference Table

| Test | Command | Expected result for locked file | Healthy file |
|------|---------|--------------------------------|--------------|
| xattr | `ls -l@ file` | Shows `com.apple.provenance` | May not show it |
| Daemon | `ps aux \| grep bird` | `bird` is running | May or may not be running |
| POSIX read | `head -1 file` | `Resource deadlock avoided` | Content |
| Swift read | NSFileCoordinator (see below) | Content | Content |
| AppleScript | `read fileRef` | Error -36 (I/O error) | Content |

## Full Swift Reader Template

```swift
import Foundation

let fileManager = FileManager.default

func readFile(_ name: String) -> String? {
    let documentsPath = NSHomeDirectory() + "/Documents"
    guard let enumerator = fileManager.enumerator(atPath: documentsPath) else { return nil }
    
    var targetPath: String? = nil
    for case let file as String in enumerator {
        if file.hasSuffix(name) {
            targetPath = documentsPath + "/" + file
            break
        }
    }
    
    guard let fullPath = targetPath else { return nil }
    
    let url = URL(fileURLWithPath: fullPath)
    let coordinator = NSFileCoordinator(filePresenter: nil)
    var error: NSError?
    var resultData: Data? = nil
    
    coordinator.coordinate(readingItemAt: url, options: .withoutChanges, error: &error) { (readURL) in
        do {
            resultData = try Data(contentsOf: readURL, options: .uncached)
        } catch {
            print("ERROR reading \(name): \(error)")
        }
    }
    
    guard let data = resultData, let content = String(data: data, encoding: .utf8) else { return nil }
    return content
}

// Usage
if let content = readFile("some_file.md") {
    print(content)
}
```

Save as `/tmp/reader.swift`, compile: `swiftc -o /tmp/reader /tmp/reader.swift`, run: `/tmp/reader`.

## Why This Happens

Apple's file coordination framework (`NSFileCoordinator`) is designed to prevent concurrent access conflicts during iCloud sync. When the `bird` daemon is syncing a file, it acquires a coordination lock. Any process that tries to read the file without going through the coordination framework gets `EAGAIN` (errno 11, Resource deadlock avoided).

The `com.apple.provenance` extended attribute (value `11`) is set by the system on managed document trees. It's not a direct lock indicator but correlates with coordination-managed directories.

## Why Other Workarounds Don't Work

| Attempt | Result | Why |
|---------|--------|-----|
| `cat src > dst` | Fails | Pipe still uses blocking read on locked fd |
| `os.open(O_NONBLOCK)` | Fails | Still triggers coordination check |
| `cp` / `ditto` | Fails | copyfile syscall intercepted by sync provider |
| `dd if=src of=dst` | Fails | Same POSIX read path |
| AppleScript `read file` | Error -36 | Scripting additions use uncoordinated access |
| Python `open()` | Errno 11 | CPython uses POSIX open under the hood |
| `brctl download` | Permission denied | No permission to trigger manual download for synced files |

## Working approaches

### 1. NSFileCoordinator (reading)

Swift/ObjC code that calls `NSFileCoordinator.coordinate(readingItemAt:options:error:byAccessor:)` can read the file because it goes through the same coordination framework that `bird` uses. The `.withoutChanges` option tells the framework "I only want to read, I won't modify anything" — this is safe and doesn't trigger write-back.

### 2. `shutil.copy2()` (copying — bypasses fcopyfile EDEADLK)

**Observed in production (June 11, 2026):** Python's `shutil.copy2(src, dst)` can COPY iCloud dataless files even when `cp`/`ditto`/`cat` all fail with `fcopyfile: Resource deadlock avoided`.

**Why it works:** The macOS `cp` command and `ditto` both use the `fcopyfile()` syscall under the hood, which Apple's file coordination framework intercepts and blocks. `shutil.copy2()` uses `open()` + `read()` + `write()` — regular POSIX I/O — which, in practice, succeeds for the copy case even though a plain `open()`+`read()` for reading alone fails with Errno 11.

**Usage:**
```python
import shutil
shutil.copy2(
    "/Users/me/Documents/iCloud/file.txt",   # dataless source
    "/tmp/dest.txt"                           # local destination
)
```

**Limitations:**
- Only works for **copying** from iCloud to a non-iCloud destination — not for reading in place
- Requires the destination to be on a non-iCloud-managed volume
- May timeout on very large files (100MB+) when the iCloud sync daemon is slow to materialize chunks
- For text files you need to READ (not copy), still use NSFileCoordinator / Swift

**Fallback chain:**
```python
def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
    except OSError as e:
        if e.errno == 11:  # EDEADLK
            # Swift NSFileCoordinator approach
            ...
        else:
            raise
```

## See Also

- `man NSFileCoordinator` — Apple documentation
- `bird` daemon — `/System/Library/PrivateFrameworks/iCloudDriveCore.framework/Versions/A/Support/bird`
- `com.apple.provenance` — managed document attribute set by the system file provider extension
