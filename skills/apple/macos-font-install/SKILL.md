---
name: macos-font-install
description: Install Google Fonts (or any TTF/OTF) on macOS so they are usable in Word, Office, and other apps. Covers finding the real file, URL-encoding brackets, and verifying with `file`/`mdls`. Use when a user wants a font installed system-wide.
created_by: agent
---

# macOS Font Install

Use when the user asks to install a font (e.g. Cairo, "a font for Word/Arabic") so it's available across macOS apps.

## Where fonts go

- User-level fonts live in `~/Library/Fonts/`. Drop a `.ttf`/`.otf` there and it appears app-wide.
- New documents pick it up immediately; restart Word/Office if it was already open.

## Google Fonts — find the real filename first (don't guess)

Google Fonts repo filenames carry weight/slant axes in square brackets and 404 on wrong guesses.

```bash
# 1. List actual files in the font's dir (Cairo example)
curl -sL "https://api.github.com/repos/google/fonts/contents/ofl/cairo" -o lst.json
# parse with python3, grep for name+size

# 2. Download via raw path — URL-ENCODE brackets/commas:
#    [ -> %5B   ] -> %5D   , -> %2C
curl -sL -o Cairo_Variable.ttf \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/cairo/Cairo%5Bslnt%2Cwght%5D.ttf"
```

**Critical verification — a bad URL is NOT an obvious error.** A 404 returns a tiny HTML file or the literal text `404: Not Found`, not a font. Always run `file <downloaded.ttf>` and confirm it reports `TrueType Font data ...` before installing. (Actual hit: guessed plain names returned HTML/404; the real file was `Cairo[slnt,wght].ttf`.)

## Variable fonts

- One TTF carries ALL weights (ExtraLight → Black) + an italic/slant axis when present.
- Word lists it as a single family with a weight slider/axis, NOT as separate menu entries — that's normal.
- If the user wants classic static weight files instead, download the statics from fonts.google.com/download rather than the variable TTF.

## Install + verify

```bash
cp /tmp/cairo_font/Cairo_Variable.ttf ~/Library/Fonts/Cairo_Variable.ttf
mdls -name kMDItemDisplayName ~/Library/Fonts/Cairo_Variable.ttf   # lists all styles -> confirms Font Book picked it up
```

`mdls` returning multiple `Cairo:style=...` lines confirms macOS Font Book registered the variable font.

## Pitfalls

- Do not hand-type the google/fonts raw URL without listing the directory first — axis brackets make the correct name non-obvious.
- Verify with `file` after every download; a "successful" curl of a 404 leaves a non-font file on disk.
- Note the user-level install (`~/Library/Fonts/`) is per-user; a system-wide (`/Library/Fonts/`) install needs admin and affects all users.
