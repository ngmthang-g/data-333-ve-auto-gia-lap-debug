# 02 — Device/emulator connection and control

## 1. Evidence hierarchy

This subsystem must distinguish three different facts:

1. **helper capability** — an API exists in `KAutoHelper.dll`;
2. **donor static reference** — `Auto_ThanLong_obfusca.exe` has a CLR `MemberRef` to that API;
3. **runtime call-site** — the protected donor actually enters the API in a concrete feature.

Existence at level 1 must not be promoted to level 2/3.

## 2. Emulator identity model

The strongest evidence is Nox-oriented. KAutoHelper and donor metadata expose Nox `multi.ini`, `pid`, `vmpid`, ADB/local ports, process lookup, window title and window-handle discovery.

Exact decoded helper chain:

```text
GetNoxTitleFromADBPort
 -> ProcessHelper.GetNetStatPorts
 -> NoxMultiIni.GetNoxMultiIni
 -> match port/config record
 -> NoxMultiIni.get_pid
 -> Process.GetProcessById
 -> Process.MainWindowTitle
```

Together with donor `DeviceInfo.DeviceHandle`, PID/VM-PID/port fields, this supports:

```text
Nox instance
 <-> PID / VM PID
 <-> localhost/ADB port
 <-> process main-window title
 <-> HWND
 <-> DeviceInfo
```

`(MEmu).txt` exists in the supplied snapshot, but no equivalently strong main/helper caller chain for MEmu has yet been recovered. Treat MEmu support as **PARTIAL**.

## 3. ADB: capability is solved, donor usage is not

`KAutoHelper.ADBHelper` implements:

- `GetDevices`, `GetDeviceName`, `ConnectNox`;
- `Tap`, `TapByPercent`, `Swipe`, `SwipeByPercent`, `LongPress`;
- `Key`, `InputText`;
- `ScreenShoot`, `GetScreenResolution`;
- `FindImage`, `FindImageAndClick`;
- `Delay`, plane-mode helpers and command execution.

Command strings prove standard paths such as:

```text
adb connect 127.0.0.1:<port>
adb -s <serial> shell input tap ...
adb -s <serial> shell input swipe ...
adb -s <serial> shell input keyevent ...
adb -s <serial> shell input text ...
adb -s <serial> shell screencap -p ...
adb -s <serial> pull ...
```

Decoded IL also proves:

```text
Tap -> format command -> ExecuteCMD
Swipe -> format command -> ExecuteCMD
ScreenShoot -> GetDevices -> ExecuteCMD -> Bitmap
FindImageAndClick -> ScreenShoot -> Delay -> FindOutPoint -> Tap -> Delay
```

However the main donor's CLR `MemberRef` catalog currently contains only **`KAutoHelper.ADBHelper.Delay`** from the ADBHelper family. No static donor `MemberRef` is present for `Tap`, `Swipe`, `ScreenShoot` or `ConnectNox` in this managed snapshot.

Therefore the defensible statement is:

> ADB is a bundled and fully implemented helper capability, but current main-donor static evidence does **not** establish ADB as the active gameplay click/capture channel.

A protected/native-indirect call could still exist; that requires targeted runtime proof.

## 4. Win32/GDI path: strong donor-side static evidence

The main donor statically references these KAutoHelper members:

```text
AutoControl.FindWindowHandlesFromProcesses
AutoControl.GetText
AutoControl.SendClickOnPosition
AutoControl.SendTextKeyBoard
AutoControl.SendKeyBoardPress
AutoControl.SendDragAndDropOnPosition
CaptureHelper.CaptureWindow
CaptureHelper.CropImage
ImageScanOpenCV.FindOutPoint
ImageScanOpenCV.FindOutPoints
```

It also references Tesseract engine/process/text APIs.

This makes the strongest statically supported gameplay-observation/control stack:

```text
process/Nox identity
 -> HWND
 -> CaptureWindow(HWND)
 -> crop/ROI
 -> OpenCV template match and/or Tesseract OCR
 -> feature/state decision
 -> SendClickOnPosition / keyboard / drag
 -> recapture and re-observe
```

### Exact click chain

Decoded KAutoHelper IL:

```text
SendClickOnPosition
 -> MakeLParamFromXY
 -> PostMessage(...)
 -> PostMessage(...)
 -> ...
```

So this API can target an HWND using window-message input rather than requiring a physical foreground mouse click.

### Exact capture chain

```text
CaptureWindow
 -> User32.GetWindowDC
 -> User32.GetWindowRect
 -> GDI32.CreateCompatibleDC
 -> GDI32.CreateCompatibleBitmap
 -> GDI32.SelectObject
 -> GDI32.BitBlt
 -> Image.FromHbitmap
 -> GDI cleanup / ReleaseDC
```

### Exact visual matching chain

```text
FindOutPoint
 -> MatchTemplate
 -> MinMax
 -> return one Point

FindOutPoints
 -> MatchTemplate
 -> MinMax / result inspection
 -> collect Points
```

Canonical machine-readable records:

- `database/control/MAIN_STATIC_CONTROL_REFERENCES.csv`
- `database/control/KAUTOHELPER_API.csv`
- `database/control/KAUTOHELPER_CALL_GRAPH.csv`
- `database/control/CONTROL_CALL_CHAINS.csv`

## 5. Multi-device state and orchestration

The donor models independent per-device state through `DeviceInfo`/account/quest objects. High-value properties include:

- `DeviceHandle`, identity/PID-related state;
- `ImageScreen`;
- `QuestThread`, `CheckQuestThread`, `IsRuningQuest`;
- per-feature settings/status fields for Train, party, Thủy Lao, Ác Tặc, inventory, HP/mana, trade and navigation.

Threading references include `Thread.Start`, `Sleep`, `IsAlive`, `Abort`, `Suspend`, `Resume`, `Task.Run`, `Dispatcher.Invoke/InvokeAsync`, `DispatcherTimer` and `System.Timers.Timer`.

This strongly supports concurrent per-device workers plus UI/timer coordination. It does **not** yet prove the locking/arbitration policy between two simultaneous mutable actions.

## 6. Coordinate spaces

At least these spaces exist in the helper surface:

1. captured window-image coordinates;
2. HWND/client coordinates for `PostMessage` input;
3. Windows global coordinates for focus/physical-input APIs;
4. Android display coordinates if an ADB action path is used.

A rebuild should make transforms explicit:

```text
matched Point in captured ROI
 -> restore ROI offset
 -> normalize to captured client viewport
 -> target-actuator transform
 -> one action
 -> fresh visual/state proof
```

Do not assume one `(x,y)` is interchangeable across ADB, client HWND and screen coordinates.

## 7. Current conclusion

For this frozen snapshot, the strongest evidence-supported external-control model is:

```text
Nox/process discovery
 -> PID/port/title/HWND correlation
 -> per-device DeviceInfo
 -> GDI/window capture
 -> OpenCV/Tesseract perception
 -> feature state logic
 -> Win32 HWND input
 -> re-observation
```

ADB remains a real helper capability and may be used by a protected/indirect path, but it is not currently proven as the donor's primary gameplay actuator.

## 8. Highest-value remaining proof

Trace one harmless donor action at runtime and record:

```text
feature method
 -> DeviceInfo / HWND
 -> capture method
 -> detector/template/OCR result
 -> selected actuator method
 -> coordinates before/after transform
 -> resulting recaptured state
```

That one trace will close the remaining gap between static donor references and exact feature-level runtime routing.