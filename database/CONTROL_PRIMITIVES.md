# Control primitives — exact helper capabilities

## ADB primitives — VERIFIED-BINARY-STRING / VERIFIED-METADATA

| Primitive | Evidence | Meaning |
|---|---|---|
| enumerate | `adb devices`, `GetDevices` | list connected emulator/device serials |
| connect | `adb connect 127.0.0.1:<port>`, `ConnectNox` | connect Nox localhost ADB endpoint |
| tap | `shell input tap`, `Tap`, `TapByPercent` | point click in Android coordinates |
| swipe | `shell input swipe`, `Swipe`, `SwipeByPercent` | drag/swipe gesture |
| long press | `LongPress` | long-touch gesture |
| key | `shell input keyevent`, `Key` | Android key event |
| text | `shell input text`, `InputText` | Android text input |
| display size | `dumpsys display`, `GetScreenResolution` | determine device viewport |
| screenshot | `screencap -p`, `ScreenShoot` | capture Android screen |
| transfer | `pull`, remote `rm -f` | retrieve/delete temporary screenshot |

## Win32 primitives — VERIFIED-METADATA

### Handle targeting

- find top-level window by caption/class;
- enumerate process windows/child windows;
- get child/control handles;
- target a window by process identity or text.

### Background/window messaging

- `SendMessage`
- `PostMessage`
- control click/position click
- keyboard messages

These can potentially operate without physically moving the user's foreground mouse, depending on target control/window behavior.

### Foreground/global input

- `SetForegroundWindow`
- `SendInput`
- `mouse_event`
- keyboard/mouse drag/scroll wrappers

This path is more sensitive to focus and global desktop coordinates.

## Capture primitives — VERIFIED-METADATA

```text
CaptureScreen
CaptureWindow
CropImage
ScaleImage
ResizeImage
CaptureImage
```

GDI path includes BitBlt/DC/bitmap operations.

## Vision primitives — VERIFIED-METADATA / VERIFIED-PDB

```text
Find / FindImage
FindOutPoint / FindImage_OutPoint
FindOutPoints
FindColor
FindAndClick*
SoluongImage*
getnhieuvitrihinhanh
getsonhieuchotrenscreen
```

Higher-level wrappers support present/absent loops and point/color variants.

## OCR primitives — VERIFIED-METADATA / VERIFIED-ASSET

```text
RecolizeText
Get_Text
make_new_image
split_image
Image_Equal
TesseractEngine runtime
```

## Recommended control abstraction for rebuild

Do not let feature code call ADB/Win32 directly. Normalize behind one device controller:

```text
IDeviceController
  Capture()
  Tap(GamePoint)
  Swipe(GamePoint a, GamePoint b, duration)
  Key(KeyCode)
  Text(string)
  GetViewport()
  IsAlive()
```

Then provide implementations:

```text
AdbDeviceController
WindowMessageController
ForegroundInputController
```

The orchestrator chooses one channel per device/session and records it. Mixing channels inside feature code should be exceptional and observable.

## Mutation discipline

Recommended per-device invariant:

```text
observe -> guard -> at most one mutable input -> observe proof -> next decision
```

This prevents overlapping clicks from independent feature threads and makes donor behavior reproducible/debuggable.
