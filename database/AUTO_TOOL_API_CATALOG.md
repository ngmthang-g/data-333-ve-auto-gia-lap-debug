# Auto Tool API Catalog — DATA-333 donor control/query surfaces

This is a compact implementation-facing catalog. Exact RIDs/RVAs and all helper methods live in the generated CSVs.

| Surface | Role | Main static reference | Canonical data |
|---|---|---:|---|
| `AutoControl.FindWindowHandlesFromProcesses` | emulator HWND discovery | yes | `MAIN_STATIC_CONTROL_REFERENCES.csv` |
| `AutoControl.GetText` | read window/control text | yes | same |
| `AutoControl.SendClickOnPosition` | background position click | yes | `CONTROL_STACK.csv` `WIN32-CLICK` |
| `AutoControl.SendTextKeyBoard` | text input | yes | `CONTROL_PRIMITIVES.csv` |
| `AutoControl.SendKeyBoardPress` | key press | yes | `CONTROL_PRIMITIVES.csv` |
| `AutoControl.SendDragAndDropOnPosition` | drag gesture | yes | `CONTROL_STACK.csv` `WIN32-DRAG` |
| `CaptureHelper.CaptureWindow` | HWND screen observation | yes | `CONTROL_STACK.csv` `CAPTURE-WINDOW` |
| `CaptureHelper.CropImage` | ROI extraction | yes | `MAIN_STATIC_CONTROL_REFERENCES.csv` |
| `ImageScanOpenCV.FindOutPoint` | one template location | yes | `CONTROL_STACK.csv` `VISION-ONE` |
| `ImageScanOpenCV.FindOutPoints` | multi-template locations/counting | yes | `CONTROL_STACK.csv` `VISION-MANY` |
| `TesseractEngine.Process` + `Page.GetText` | OCR | yes | main static refs |
| `ProcessHelper.GetNetStatPorts` | process/port discovery | yes | `CONTROL_STACK.csv` `NOX-IDENTITY` |
| `Port.pid`, `Port.port_number` | port ownership | yes | main static refs |
| `ADBHelper.Delay` | timing delay | yes | main static refs |
| `ADBHelper.Tap/Swipe/ScreenShoot/ConnectNox` | ADB input/capture/connect capability | **no static main ref** | `KAUTOHELPER_API.csv`, helper string indicators |

## Per-device/state surfaces

Use `MODEL_PROPERTIES.csv` for the exact property accessors/RVAs. The most important model is `DeviceInfo`, containing screen image cache, feature state flags, coordinate state, account list/current account, quest/check threads, run state, device handle/id/name and credentials/server fields.

`MainWindow` carries broad operator policy/settings for Train, party, sell, storage, HP/mana, activities, trade, pet/mount, captcha and scheduling.

## Reliability boundary

An API appearing in KAutoHelper means **available capability**. It is only marked active in the main donor when `MAIN_STATIC_CONTROL_REFERENCES.csv` or a future exact call-site proves it.
