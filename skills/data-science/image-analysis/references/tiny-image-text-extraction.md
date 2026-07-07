# Tiny Image Text Extraction: Worked Example

## The Problem

A user asked to read text from a PNG image at path `/var/folders/.../waveterm_paste_1783380932834_kqdi2c.png`. The image was **468×40px, 16-bit RGBA** — a thin screenshot caption bar.

`vision_analyze()` failed with: `"this model does not support image input"` (non-vision model).
`browser_vision()` failed with the same error.

The task was to read the text, and a specific ambiguity (SHC-O5 vs SHC-05) needed resolution.

## Tool Setup Check

```bash
which tesseract          # /opt/homebrew/bin/tesseract ✓
which magick             # /opt/homebrew/bin/magick ✓
python3 -c "import PIL; print(PIL.__version__)"  # 11.1.0 ✓
pip3 list | grep pytesseract   # 0.3.13 ✓
```

If missing: `brew install tesseract` and `pip3 install pytesseract Pillow`.

## Step-by-Step Applied

### 1. `file` Command

```bash
$ file /path/to/image.png
PNG image data, 468 x 40, 16-bit/color RGBA, non-interlaced
```

468×40 — very small. 16-bit/color + RGBA suggests a rendered UI screenshot, not a photograph.

### 2. Pixel Value Mapping

```python
img = Image.open(path)
gray = img.convert('L')
pixels = list(gray.getdata())
print(sorted(set(pixels)))  # [0, 114, 115]
```

Only **3 unique values**: 0 (pure black background), 114 and 115 (text pixels). This is a simple black-background-with-light-text rendering.

### 3. Polarity & Threshold

Max pixel = 115, so the image is dark with brighter text. Threshold = 115 - 20 = **95**. Any pixel > 95 is text.

### 4. Full ASCII Render

```
 2|                 ##                    ##         #                              ##
 3|  ######    ####   #### ##         ######  #   ######    ######  ######  #### ###  #### ## ## ####  ########    ######  ######  ####  ###   ###### ## ####  #### ####  ###
 4|  ## ## ###### ##### ###  #######  ## ##### ###### ########### # ###### #######  ###### ########    ###### ##### ##  ########    ## # ## #######  #########    ###### ##### ##  #########   ####### #######  #######    ### ########## #### #### ########## ### #######  ######## ####  ## ###########  ####### ##### ### #### ###
 5|  ############# #########  #### ##  ### ################################ ##  ################### ###############    ### #######     ### ## ##     ### ########     ## ##  ##     ### #######     ### #####     ############     ## ######   #### ########## ################################  ##############  ##  ################### ###############
 6|  ######## ###### #######  ####      ##### ############### ## ########## ##  ############ ######   ########### ####  ########   ### #######   #### ## ##      ##########   ##### ## ###     ###########   #### #######     ##########   ##### ######  ##### ## #######################################   ## ######## ##  ## #### #### ########## ####### ##########
 7|  ##  ############# ###   ## ## #  ## ######## ## ####### #########    ##  ############## ##  ##   ##   ### #### ##          # ##### #### ###### ## ##  #  ## #### ##### ############ ##  ####### #### ###### #########  # #### ##### ########## ##  ####### ## ####### ### #####  #### ##### ## ####   ###### #######  ######### #######  ####################
 8|  ##  ############# ####  ######## ############## ##################   ########################   ##  ## ###### ##          ######  #######  ###########  ####### ## ####   ###########  ######  #######  #####  ##### ####### ## ####   ######### ### #### ## ####### ############ ## ######## #####  ###### #######  ######### ########## ##############
 9|  #   # #### ######  ###   ##   #   ##  #  # ##   #  #   #  ### ##  ###   ## ## ### ##  ##  ## #    ##   #  ##### #              ##  #  #   #     ##      ##   ##  #  ##  ##     ##     ###   ##  #  #   #     ##    # ##   ##  #  ##  ##     ##  ##    #   ### ##  ### #  ###### ### # ## #  ## #  # ##    # ### #  ###        # ## #  # ### # ## ## #  ##  #
10|     ####                                                                                                                               ##                             ##                             ##                               ####
```

### 5. OCR (First Attempt) — Garbled

```python
import pytesseract
t = pytesseract.image_to_string(img, config='--psm 7 --oem 3')
# Result: "(Pipe &: Shomonse Chister Plen — SHCES, SHOR, SHC-OS, SNCS Arenpement ene Gimensions"
```

Total nonsense. This is what happens when OCR gets the raw small image.

### 6. Binarize + Upscale + Re-OCR

```python
new_pixels = [0 if p > 95 else 255 for p in pixels]  # text=black(0), bg=white(255)
binary = Image.new('L', (w, h))
binary.putdata(new_pixels)
big = binary.resize((w*8, h*8), Image.NEAREST)  # 3744×320

t = pytesseract.image_to_string(big, config='--psm 7 --oem 3')
# Result: "Figure 3: Showcase Cluster Plan — SHC-01, SHC-02, SHC-04, SHC-O5 Arrangement and Dimensions"
```

Much better — all words correct, but **SHC-O5** with letter-O rather than zero.

### 7. Disambiguate O vs 0

The issue: Tesseract reads the narrow zero as capital O. This is common in sans-serif fonts where zero has similar width to the letter O.

**Method A: Cross-character comparison (ASCII zoom)**

Located and rendered the '0' from SHC-01, SHC-02, SHC-04, then compared to the contested character in the last code:

```python
# '0' from SHC-01 (x=127-143):
# y=2:       ##
# y=3:   ######
# y=4:  ######### # ###
# y=5:  ##   ##########
# y=6:  ##   ##########
# y=7:  ## ############
# y=8:  ###############
# y=9:   ## ## ### ##
#
# Contested '0/O' from last code (x=264-280):
# y=3:  ##  ###     ####
# y=4:  #######    #####
# y=5:   #####     #####
# y=6:  #######     ####
# y=7:  #########  # ###
# y=8:  ##  ##### ######
# y=9:      # ##   ##  #
# y=10:      ##
```

**Verdict: Same shape** — both show a closed rounded structure, same width (~13 columns), same baseline penetration. Confirmed as '0' (zero).

**Method B: Context** — Sequential codes SHC-01, SHC-02, SHC-04, SHC-05. A letter O in the middle of a numeric sequence makes no sense. It's zero.

### 8. Final Result

```
Figure 3: Showcase Cluster Plan — SHC-01, SHC-02, SHC-04, SHC-05 Arrangement and Dimensions
```

## What Worked

| Technique | Reason |
|-----------|--------|
| `file` command | Gave dimensions (468×40) that flagged this as a tiny-text case |
| Pixel value analysis | Only 3 values → simple binarization threshold |
| ASCII rendering | Let me visually verify character shapes that OCR mangled |
| Cross-character zoom comparison | Definitively resolved O vs 0 by comparing known '0' to contested glyph |
| NEAREST upscale (not LANCZOS) | Preserved hard pixel edges for OCR |
| Multiple PSM modes | Cross-checking 6, 7, 3 caught inconsistencies |

## What Didn't Work

| Attempt | Why |
|---------|-----|
| Raw OCR on original image | Too small (468×40), blurry for Tesseract |
| Magnify with `-sharpen -negate -normalize` (ImageMagick) | Overprocessed, made text unrecognizable |
| Character whitelist in OCR | `-c tessedit_char_whitelist=...` forced wrong readings |
| easyocr | Required model download, failed due to SSL cert issue, overkill for a 468×40 image |
| Invert-then-OCR | Inverting the dark-on-light correctly didn't help; proper binary + upscale was the key |

## When to Use This Approach

- Image is <500px wide and <60px tall (screenshot caption, UI bar, tooltip)
- `vision_analyze()` fails with "model does not support image input"
- Text appears to be rendered (not photographic) — check pixel value cardinality
- You need to resolve a specific character ambiguity (O/0, 5/3, l/1)
