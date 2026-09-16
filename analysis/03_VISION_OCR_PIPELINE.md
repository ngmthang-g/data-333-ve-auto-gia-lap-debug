# 03 — Screen observation, image matching and OCR pipeline

## 1. Evidence inventory

The Debug snapshot contains **1,393 PNG files** totaling about 3.55 MB. The dominant folders are:

| Folder | PNG count | Main inferred purpose |
|---|---:|---|
| `hoatdong/` | 461 | UI states/actions/maps/NPCs/activity screens |
| `ItemSell_TrangVatPham/` | 435 | item visual classification/sell rules |
| `saveImage/` | 215 readable PNGs | small generated crops/samples; 214 are 30x10 |
| `itemrac/` | 91 | trash/equipment visual classes |
| `thuylao/` | 59 | Thủy Lao flow/state templates |
| `PT/` | 35 | party-related templates |
| `level/` | 27 | leveling/new-player flow |
| `truyen/` | 27 | map transfer/navigation templates |
| `Item_vaokho/` | 19 | storage deposit item templates |
| `ItemSell_TrangNgoc/` | 11 | gem/jewel sell templates |
| `tranthu/` | 4 | pet/companion-related templates |

Most templates are tiny fragments, commonly tens of pixels in width/height. This strongly indicates localized template matching rather than full-screen classification.

## 2. Screen acquisition primitives

KAutoHelper exposes two capture families.

### ADB capture

`ADBHelper.ScreenShoot` is backed by literals for:

```text
shell screencap -p
pull
rm -f
```

This path can capture an Android framebuffer independently of host window focus.

### Win32/GDI capture

`CaptureHelper` methods:

- `CaptureScreen`
- `CaptureWindow`
- `CaptureWindowToFile`
- `CaptureScreenToFile`
- `CaptureImage`
- `CropImage`
- `ScaleImage`
- `ResizeImage`

Native GDI helpers include `BitBlt`, `CreateCompatibleBitmap`, `CreateCompatibleDC`, `GetWindowDC`, `GetWindowRect`, and object/DC cleanup.

## 3. Image matching primitives

KAutoHelper `ImageScanOpenCV` exposes:

- `GetImage`
- `Find`
- `FindOutPoint`
- `FindOutPoints`
- `FindColor`
- `RecolizeText`
- `SplitImageInFolder`
- threshold/pixel-replacement helpers

MainWindow PDB independently exposes higher-level wrappers:

- `FindImage`
- `FindImage_OK`
- `FindImage_OutPoint`
- `FindImage_Color_TBDTim`
- `FindAndClick`
- `FindAndClick_OK`
- `FindAndClick_OnPoint`
- `FindAndClick_Color`
- `FindAndClick_Color_TBDTim`
- `FindAndClick_OnPoint_Color`
- `FindAndClick_Until_Found`
- `FindAndClick_OnPoint_Until_Found`
- `Not_FindAndClick_OnPoint`
- `Not_FindAndClick_OnPoint_Until_Found`
- `SoluongImage`
- `SoluongImage_mau`
- `getnhieuvitrihinhanh`
- `getsonhieuchotrenscreen`

This is strong evidence for a reusable perception DSL inside MainWindow: find one/many instances, optionally color-filter them, optionally click, optionally loop until present/absent.

## 4. OCR/text recognition

The bundle includes:

- `Tesseract.dll`
- `tessdata/eng.traineddata`
- `Get_Text_From_Image` helper type in KAutoHelper
- `RecolizeText`
- PDB symbols `SoveNormalCapt`, `Nomal`
- model/status type `TwoCaptResponseStatus`
- properties related to captcha count/solve configuration

Therefore an OCR/captcha-related subsystem is definitely present. Exact external service endpoint/API key behavior is not recovered from current static evidence and raw secrets should not be copied to the KB.

For a rebuilt production tool, Captcha should be represented as:

```text
CAPTCHA_DETECTED
 -> pause mutable automation
 -> surface device/account to operator
 -> user resolves challenge
 -> verify normal game state returned
 -> resume
```

## 5. Template semantics visible from filenames

The `hoatdong/` asset names reveal the state vocabulary the donor tool observes. Examples include categories for:

- map names and map-entry states;
- NPC locations and dialogs;
- bag/storage screens;
- buy/sell screens;
- HP/mana/medicine/items;
- party invite/join/follow/leave;
- trade;
- train/auto-fight settings;
- Thủy Lao / Ác Tặc / Tàng Bảo Đồ-like activity flows;
- revive/Đầu thai/treatment;
- pet/horse/companion controls;
- disconnect/offline/online states;
- confirmation dialogs;
- quest accept/continue/complete/reward states.

This asset vocabulary is valuable donor behavior evidence even when code branches remain obfuscated.

## 6. Reconstructed perception-action loop

**PROBABLE**, based on verified primitives and symbol names:

```text
capture device/window
 -> optional crop/scale/resize
 -> Find / FindColor / OCR
 -> determine visual state
 -> choose feature branch
 -> calculate match point / configured coordinate
 -> ADB tap or Win32 click/key/drag
 -> delay/timeout loop
 -> recapture and verify next visual state
```

The donor likely has multiple variants of this loop because the PDB exposes many `FindAndClick*` helpers rather than one unified state machine API.

## 7. Reliability implications

Pixel matching can fail because of:

- emulator resolution/aspect ratio;
- DPI scaling;
- anti-aliasing/font changes;
- language/text changes;
- animation/transparency;
- theme/UI patch changes;
- occlusion/window border differences for host capture;
- stale screen after click;
- same template appearing in more than one context.

A robust rebuild should store each observation as a structured detector:

```text
Detector ID
template(s)
search region
expected viewport
scale policy
threshold
color constraints
required/forbidden companion markers
state meaning
confidence
```

and separate it from action logic.

## 8. State proof rule

Do not model `FindAndClick` success as feature success. Use:

```text
pre-state detector
 -> one mutation
 -> post-state detector(s)
 -> timeout
 -> recovery/rescan
```

DATA-2222 should be preferred whenever it exposes a semantic state/action that can replace a fragile visual detector/click.
