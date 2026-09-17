# 06 — DATA-333 materialization and deep control findings

## Why the previous architecture-only pass was insufficient

A useful DATA repo must answer exact lookup questions without rereading the donor package. Following DATA-2222, DATA-333 now materializes raw evidence into query-oriented CSV/JSONL catalogs with hashes, RIDs/RVAs, joins, feature maps and explicit evidence status.

## 1. Managed donor recovery

`Auto_ThanLong_obfusca.exe` remains a parseable CLR assembly despite obfuscation/protection:

- 57 TypeDefs;
- 1,070 MethodDefs;
- 429 Fields.

The current body classifier finds 802 protected/non-standard methods, 259 valid IL headers and 9 pinvoke/abstract methods. This means metadata identity is much more recoverable than implementation bodies.

The Debug PDB yields 783 unique identifier-like symbols. Surviving original names plus PDB evidence expose core feature routines and per-device state even when the main body cannot be decompiled normally.

## 2. KAutoHelper is the clean behavioral donor

`KAutoHelper.dll` has 40 TypeDefs and 224 MethodDefs, with clean IL for 166 methods and 58 PInvoke/abstract entries. Its IL is materialized into an exact call graph.

Examples:

```text
SendClickOnPosition
 -> MakeLParamFromXY
 -> PostMessage (multiple mouse-message stages)

SendDragAndDropOnPosition
 -> MakeLParamFromXY
 -> PostMessage
 -> Thread.Sleep
 -> PostMessage

CaptureWindow
 -> User32.GetWindowDC/GetWindowRect
 -> GDI32.CreateCompatibleDC/CreateCompatibleBitmap
 -> SelectObject
 -> BitBlt
 -> Image.FromHbitmap
 -> cleanup

FindOutPoint
 -> EmguCV MatchTemplate
 -> MinMax
 -> point
```

These chains are direct IL evidence, not inference from DLL names.

## 3. Corrected actuator conclusion

KAutoHelper bundles a full ADB layer with exact commands for connect, tap, swipe, key, text, screencap/pull and display resolution.

However the main managed donor's static MemberRefs include only `KAutoHelper.ADBHelper.Delay` from `ADBHelper`. They do not include `Tap`, `Swipe`, `ScreenShoot` or `ConnectNox`.

The same main assembly **does** reference Win32-facing helper surfaces for HWND discovery, click, keyboard, drag, window capture/crop and OpenCV point matching, plus Tesseract OCR.

Therefore:

- `ADB capability exists` = VERIFIED;
- `main donor uses ADB gameplay input` = NOT PROVEN by current static evidence;
- `main donor has an active Win32 capture/input + vision/OCR surface` = VERIFIED static reference evidence.

This correction matters because simply seeing `adb.exe`/`AdbWinApi.dll` in a Debug folder would otherwise create a false architectural conclusion.

## 4. Emulator identity/control path

The recovered identity stack combines:

```text
Nox multi.ini
 -> pid / vmpid
 + netstat port discovery
 -> Port(pid, port_number)
 -> Process.GetProcessById(pid)
 -> MainWindowTitle
 -> FindWindowHandlesFromProcesses
 -> DeviceInfo.DeviceHandle
```

`GetNoxTitleFromADBPort` confirms the helper can relate a port to a Nox process/title. This explains why ADB-port metadata can appear in the architecture even if actual gameplay clicks are Win32 messages.

## 5. Per-device orchestration

`DeviceInfo` stores independent state including:

- `DeviceHandle`, `DeviceID`, `DeviceName`;
- account list/current account;
- `QuestThread`, `CheckQuestThread`, `IsRuningQuest`;
- screenshot image state;
- train/activity/party/storage flags;
- coordinates;
- disconnect/captcha counters and status.

The main assembly references `Thread.Start`, `Sleep`, `Abort`, `Suspend`, `Resume`, `IsAlive`, dispatcher APIs, timers and tasks. This strongly supports a per-device worker/checker model plus UI timers.

`Abort/Suspend/Resume` are a donor reliability smell: they can freeze locks or leave resources in inconsistent state. A rebuild should preserve behavior policy but replace this lifecycle with cancellation/state-machine control.

## 6. Perception layer

The snapshot has 1,393 PNG assets but only 1,180 unique SHA-256 values. 178 duplicate groups account for 213 redundant copies.

The major folders map to behavior domains: broad activity UI, sell-item templates, saved visual references, trash-item templates, Thủy Lao, party, level/quest, travel/maps, storage, gems, etc.

The main assembly directly references:

- `CaptureWindow` and `CropImage`;
- `FindOutPoint` and `FindOutPoints`;
- Tesseract engine setup/process/get-text.

So the stable static perception model is:

```text
HWND capture
 -> crop/scale/ROI
 -> template or OCR detection
 -> update donor state
 -> input action
 -> recapture
```

Exact image threshold, ROI and retry order remain dynamic/protected-body gaps and must not be fabricated.

## 7. Feature state/policy layer

The materializer creates a feature index and joins surviving methods/properties/assets into domains. High-value donor method identities include `trainLEVEL1`, `sellItemm`, `catdovaokho`, `laydotrongkho`, `setupautothuylao`, `HD_ACTAC`, `danh_actac`, `dilamnvuTBD`, `truyenmap`, NPC travel helpers, party/follow routines and `StartQuestDevice`.

`MainWindow` properties expose operator policy such as train maps/settings, party mode, item filters, auto HP thresholds, consumable counts, storage toggle, trade coordinates/state, activity toggles, captcha settings and scheduling. `DeviceInfo` holds runtime-like per-device state. This split suggests:

```text
MainWindow = global/user policy + UI shell
DeviceInfo  = mutable per-emulator execution state
AccountInfo = account identity/server/login data
QuestInfo   = scheduled/per-feature work item state
```

## 8. Persistence/control plane

The main assembly statically references file read/write/enumeration APIs. `luufile/` contains settings/account/password/map/team/pet-food/coordinate-style persistence.

Login/license/update is a separate HTTP/JSON/update control plane with `HttpClient`/request/JSON/AutoUpdater references and access-token/update models. No current static evidence promotes that HTTP plane into direct gameplay protocol control.

## 9. DATA-2222 integration direction

DATA-333 should preserve donor behavior/state-machine clues; DATA-2222 should supply game-semantic state/actions where it already has stronger contracts.

For example:

```text
333 sell policy/templates/method names
 + 222 live bag/item-instance/sell semantics
 -> rebuilt sell state machine without brittle icon identity
```

Likewise Train, party, navigation, storage, revive/heal and trade should preserve useful donor policy while replacing image clicks with 222 semantics when available.

## 10. Remaining high-value proofs

The remaining work is targeted, not broad reverse engineering:

1. trace one harmless feature action and record protected caller -> helper API -> HWND/coordinates -> post-state;
2. trace one screenshot cycle to prove actual capture cadence/ROI/threshold;
3. run two emulators and prove PID/port/HWND/DeviceInfo isolation;
4. recover exact feature transition tables for Train, Sell, Thủy Lao and Ác Tặc via runtime logging;
5. only investigate ADB gameplay use if runtime/reflection evidence contradicts the current static non-reference finding.

Those proofs should be materialized as new runtime-event CSVs, leaving the static database immutable for this snapshot.
