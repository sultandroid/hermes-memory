# Screen OCR Fallback (read on-screen text via terminal)

Use when the user asks you to "read the captions on my screen", "take the access", or
read any live on-screen text (meeting subtitles, dialog boxes, terminal output) and
either `computer_use` is NOT available in the session OR the active model has no vision.

## Steps

1. Capture the screen to PNG:
```bash
screencapture -x /tmp/screen.png
```
`-x` suppresses the shutter sound. Requires macOS Screen Recording permission for the
terminal. If the capture comes back black/blank, that permission is missing (System
Settings > Privacy & Security > Screen Recording) and there is no CLI workaround —
fall back to asking the user to paste the text.

2. OCR with macOS Vision via a Swift script (more reliable than tesseract, and it
   handles the raw RGBA PNG that tesseract rejects). Write `/tmp/ocr.swift`:
```swift
import Foundation
import Vision
import AppKit

let path = "/tmp/screen.png"
guard let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERR: cannot load image"); exit(1)
}
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["en-US", "ar-SA"]   // Arabic for AR/EN bilingual screens
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try? handler.perform([request])
for o in request.results ?? [] {
    if let c = o.topCandidates(1).first { print(c.string) }
}
```
Run: `cd /tmp && swift ocr.swift`

3. Review the OCR text and report the on-screen content. Do NOT claim to "see" what the
   user sees beyond what the OCR returned.

## Pitfalls
- **tesseract rejects the screencapture PNG** ("Image file cannot be read") because it is
  RGBA/16-bit. Either `sips -s format jpeg` first, or skip tesseract and use Swift Vision
  (recommended — Vision also does Arabic natively).
- **Swift Vision needs AppKit** for `NSImage`; it is macOS-only.
- `screencapture` captures only the current Space / frontmost display arrangement. If the
  captions window is in another Space or a separate display, the capture may miss it — ask
  the user to bring it forward or name the app.
- If the model has vision, prefer `vision_analyze` on the captured PNG directly. The Swift
  Vision path is the fallback for non-vision models or when you must return text.
- Be honest about what was captured: if the screenshot shows your own terminal session
  (e.g. the Hermes chat) rather than the expected captions window, say so plainly and ask
  which app/space has the content.
