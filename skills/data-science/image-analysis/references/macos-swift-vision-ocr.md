# macOS Swift + Vision OCR Fallback

When `tesseract` fails to read a PNG (`Image file ... cannot be read!`, often on
large high-DPI screenshots like 4112x2658) or produces empty output, the most
reliable fallback on macOS is the **built-in Vision framework** via a short
Swift script. It is pre-installed, needs no pip packages, handles bilingual
(AR/EN) text, and reads large screenshots accurately.

## When to use

- `vision_analyze()` returns "model does not support image input" (or a connection error).
- `tesseract` errors with `Image file ... cannot be read!` or yields empty text.
- You need to read text from a **full-screen screenshot** (e.g. a Hermes terminal,
  meeting captions, a desktop window) that tesseract rejects.

## The script

Write to a `.swift` file, then run `swift <file>.swift`. The first run may take
a few seconds to compile.

```swift
import Foundation
import Vision
import AppKit

let path = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "/path/to/image.png"
guard let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERR: cannot load image"); exit(1)
}
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["en-US", "ar-SA"]  // add/remove languages as needed
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try? handler.perform([request])
let obs = request.results ?? []
for o in obs {
    if let c = o.topCandidates(1).first {
        print(c.string)
    }
}
```

Run with the image path as an argument:

```bash
swift /tmp/ocr.swift /tmp/captions_screen.png
```

## Notes / pitfalls

- `swift` CLI is present on macOS with Command Line Tools (`command -v swift`).
- For a screenshot of a terminal/desktop, the OCR output is **raw text of the whole
  screen** — filter for the relevant window or captions. A Hermes terminal will
  echo the conversation text, which can be confused for meeting captions.
- Bilingual recognition: use `["en-US", "ar-SA"]` for Aseer project docs that mix
  English and Arabic.
- This reads the image at its native resolution; no upscaling step is needed
  (unlike tesseract tiny-text cases). Vision handles large screenshots natively.
- The `topCandidates(1).first` gives the highest-confidence string per text region;
  output is in reading order.
