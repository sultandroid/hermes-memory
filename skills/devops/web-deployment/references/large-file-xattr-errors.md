# Surge Deploy: Large Embedded-base64 Files & com.apple.provenance xattr

## The Problem

Standalone HTML files with embedded base64 images (5-7 MB) stored on OneDrive consistently fail to deploy to Surge.sh with:

```
/Users/me/.npm-global/lib/node_modules/surge/lib/middleware/deploy.js:229
    helpers.log("   Processing Error:".yellow, payload.error.filename).log()
                                                             ^
TypeError: Cannot read properties of undefined (reading 'filename')
```

## Root Cause (two interacting factors)

1. **`com.apple.provenance` xattr**: macOS sets this immutable attribute on all OneDrive-synced files. It is immune to:
   - `xattr -c` (clear all)
   - `xattr -cr` (recursive clear)
   - `xattr -d com.apple.provenance`
   - `cp` (inherited by copy)
   - Python `open().read() → open().write()` (inherited)
   - bash `cat source > dest` (inherited)
   - Hermes `write_file` tool (inherited)

2. **Surge origin processing timeout**: The Surge server appears to reject or timeout during processing of 5-7MB single-file uploads. The error occurs at inconsistent percentages (27%, 77%), suggesting a race condition on the Surge side.

## Attempted Fixes That Did NOT Work

- Fresh deploy directory (`mkdir -p /tmp/fresh && cp source /tmp/fresh/`)
- Python open-read-write cycle (xattr persists from source open)
- `write_file` via Hermes tools (xattr persists)
- `cat >` redirection in bash (xattr persists)
- `xattr -c`, `-cr`, `-d` all fail on `com.apple.provenance`

## Workarounds

1. **Externalize assets**: Convert embedded base64 images to external files. Reduces index.html to <1MB which deploys reliably.
2. **`npx surge` (CONFIRMED FIX)**: Run via `npx surge` instead of the local `surge` CLI. The npx version uses a different Node module resolution that bypasses the proxy/stream corruption triggering the TypeError. Proven to succeed on 6.7MB files where local `surge` fails at 27%, 77%, or other percentages. Deploy with background PTY:
   ```bash
   terminal(command='npx surge /tmp/deploy/ domain.surge.sh',
            pty=true, background=true, notify_on_complete=true, timeout=600)
   ```
   The upload shows progress bars (0-100%) — expect 5-10 minutes for 6.7MB on Student plan.
3. **Use a different host**: For standalone HTML with embedded media, use a host that handles larger single-file uploads (Netlify, Vercel, or SCP to a LAMP host).

## Monitoring Pattern for Slow Uploads

```bash
# Start deploy in PTY background
terminal(command='cd /tmp/deploy && surge --project ./ --domain my.surge.sh',
         pty=true, background=true, notify_on_complete=true, timeout=600)
# Poll until done (Surge Student: ~0.5-1 Mbps upload speed)
process(action='wait', session_id=..., timeout=180)
# On timeout, check progress:
process(action='log', session_id=..., offset=-5)
# Repeat wait until deploy completes or fails
```
