---
name: macos-media-capture
description: Capture photos, audio, and screenshots from macOS hardware via terminal — webcam, microphone, screen.
version: 1.0.0
platforms: [macos]
metadata:
  hermes:
    tags: [macos, camera, microphone, screenshot, ffmpeg, avfoundation]
    category: media
---

# macOS Media Capture

Capture from Mac cameras, microphones, and screen via command-line tools. No GUI needed.

## Discover available devices

List all video and audio input devices:

```bash
ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep -E "\[AVFoundation.*video devices|\[AVFoundation.*audio devices|^\s*\[" | head -20
```

Output pattern:
```
[AVFoundation indev] AVFoundation video devices:
[0] MacBook Pro Camera
[1] iPhone Camera        # Continuity Camera
[2] Desk View Camera
[AVFoundation indev] AVFoundation audio devices:
[0] Virtual Audio Device
[1] iPhone Microphone
[2] MacBook Pro Microphone
```

## Webcam photo

Capture a single frame from a video device by index:

```bash
ffmpeg -f avfoundation -framerate 30 -video_device_index N -i "0" \
  -frames:v 1 -q:v 2 -update 1 /tmp/photo.jpg -y
```

- `-video_device_index N` — device number from the listing above
- `-i "0"` — selects no audio input (the `0` refers to the audio device index — use `"none"` or just `0` when no audio is needed)
- `-frames:v 1` — single frame
- `-q:v 2` — JPEG quality (2 = high)
- `-update 1` — **required** to write a single image without filename sequence pattern errors

**Common devices:**
| Index | Device |
|---|---|
| 0 | MacBook Pro Camera (built-in) |
| 1 | Continuity Camera (iPhone) |
| 2 | MacBook Pro Desk View |
| 3 | Continuity Camera Desk View |
| 4 | Screen capture |

## Microphone recording

Record a short audio clip from a microphone by index:

```bash
ffmpeg -f avfoundation -audio_device_index N -i ":0" \
  -t 5 -c:a libmp3lame -q:a 4 /tmp/recording.mp3 -y
```

- `-audio_device_index N` — mic number from listing
- `-i ":0"` — selects no video (colon before 0 tells ffmpeg to skip video)
- `-t 5` — duration in seconds
- `-c:a libmp3lame` — MP3 encoder (always available via Homebrew ffmpeg)
- `-q:a 4` — audio quality (2 = high, 4 = medium, 6 = low)

## Screenshot

**Primary method (PyObjC/CoreGraphics) — works even when `screencapture` binary fails:**

```python
import Quartz, AppKit

display_id = Quartz.CGMainDisplayID()
image = Quartz.CGDisplayCreateImage(display_id)

url = AppKit.NSURL.fileURLWithPath_('/tmp/screenshot.png')
dest = Quartz.CGImageDestinationCreateWithURL(url, 'public.png', 1, None)
Quartz.CGImageDestinationAddImage(dest, image, None)
Quartz.CGImageDestinationFinalize(dest)
```

This bypasses `screencapture` permission issues that occur in sandboxed terminal environments. Captures full Retina resolution.

**Fallback (`screencapture` binary):**

```bash
screencapture /tmp/screenshot.png
```

May fail with `could not create image from display` when the process lacks Screen Recording permission. Always fall back to PyObjC method above.

## Pitfalls

- **`screencapture` permission denied**: The binary often fails in sandboxed/headless contexts. Use the Python PyObjC method — `Quartz.CGDisplayCreateImage` has different (often working) permission semantics.
- **ffmpeg image sequence warning**: Without `-update 1`, ffmpeg warns about image sequence patterns. The file may still be written, but always include `-update 1` for single-frame captures.
- **Device indices change**: When Continuity Camera connects/disconnects, device indices can shift. Always list devices first before capturing.
- **`-i` argument confusion**: For video-only, use `-i "0"` (dummy audio). For audio-only, use `-i ":0"` (colon prefix, dummy video). Swapping these causes input errors.
