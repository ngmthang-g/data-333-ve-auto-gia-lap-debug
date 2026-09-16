# 02 — Device/emulator connection and control

## 1. What the tool connects to

The strongest evidence points to an external Windows controller operating Android emulator instances, especially Nox, through a combination of:

- process/window discovery;
- Nox multi-instance metadata;
- localhost ADB endpoints;
- Win32 window handles.

A `(MEmu).txt` file also exists in the Debug root, so MEmu-related operator data is present, but the recovered code-level helpers are much stronger for Nox. Treat MEmu support as **PROBABLE/partial** until an exact caller is recovered.

## 2. Nox identity resolution

**VERIFIED-METADATA / VERIFIED-BINARY-STRING**

KAutoHelper contains `NoxMultiIni` with:

- `pid`
- `vmpid`
- `Ports`
- `GetNoxMultiIni`
- `GetNoxTitleFromADBPort`

It also contains the literal path fragment:

`\Local\Nox\multi.ini`

The main tool PDB independently exposes `KhungCode_Auto.NoxMultiIni`, `GetNoxMultiIni`, `GetNoxTitleFromADBPort`, `pid`, `vmpid`, and `port_number`.

**Interpretation:** the tool correlates emulator metadata/process identity with ADB port and visible emulator title.

## 3. ADB connection path

KAutoHelper contains exact ADB command templates:

```text
adb devices
adb connect 127.0.0.1:<port>
adb -s <device> shell input tap <x> <y>
adb -s <device> shell input swipe <x1> <y1> <x2> <y2> <duration>
adb -s <device> shell input keyevent <key>
adb -s <device> shell input text "<text>"
adb -s <device> shell screencap -p "<remotePath>"
adb -s <device> pull "<remotePath>"
adb -s <device> shell rm -f "<remotePath>"
adb -s <device> shell dumpsys display | Find "mCurrentDisplayRect"
```

KAutoHelper `ADBHelper` methods:

- `SetADBFolderPath`
- `ExecuteCMD`
- `GetDevices`
- `GetDeviceName`
- `TapByPercent`
- `Tap`
- `Key`
- `InputText`
- `SwipeByPercent`
- `Swipe`
- `LongPress`
- `GetScreenResolution`
- `ScreenShoot`
- `ConnectNox`
- `PlanModeON`
- `PlanModeOFF`
- `Delay`
- `FindImage`
- `FindImageAndClick`

This is direct proof that the helper library can drive an emulator without foreground mouse focus.

## 4. Win32 window/control path

KAutoHelper `AutoControl` provides a second actuator family:

### Discovery/handles

- `FindWindow`
- `FindWindowByCaption`
- `FindWindowEx`
- `FindWindowHandle(s)FromProcesses`
- `GetChildHandle`
- `GetControlHandleFromControlID`
- `FindHandle(s)WithText`
- `GetWindowRect`

### Mouse/input

- `SendClickOnControlById`
- `SendClickOnControlByHandle`
- `SendClickOnPosition`
- `SendClickDownOnPosition`
- `SendClickUpOnPosition`
- `SendDragAndDropOnPosition`
- `SendDragAndDropOnMultiPosition`
- `MouseMoveDrag`
- `MouseClick`
- `MouseDragX`
- `MouseDragY`
- `MouseScroll`

### Keyboard/text

- `SendText`
- `SendKeyBoardPress`
- `SendKeyBoardPressStepByStep`
- `SendKeyBoardDown`
- `SendKeyBoardUp`
- `SendTextKeyBoard`
- `SendKeyFocus`
- `SendMultiKeysFocus`
- `SendStringFocus`
- `SendKeyPress/Down/Up`

Native imports include user32/GDI primitives such as `SendMessage`, `PostMessage`, `SendInput`, `SetForegroundWindow`, `mouse_event` and window enumeration APIs.

## 5. Process/port correlation

KAutoHelper `ProcessHelper` contains:

- `GetWindowTitles`
- `EnumWindowsCallback`
- `GetWindowTitle`
- `GetNetStatPorts`
- `LookupProcess`

Combined with `NoxMultiIni` and `DeviceInfo.pid/vmpid/port_number`, this indicates a multi-key identity model:

```text
Nox config instance
 <-> host PID / VM PID
 <-> listening localhost port
 <-> ADB device serial
 <-> emulator window title/handle
 <-> DeviceInfo object
```

This is a core part of multi-emulator isolation.

## 6. DeviceInfo orchestration

PDB symbols support these device-level fields/concepts:

- `DeviceID`
- `DeviceName`
- `DeviceHandle`
- `pid`
- `vmpid`
- `ImageScreen`
- `Accounts`
- `CurrentAccountIndex`
- `Quest`
- `QuestThread`
- `CheckQuestThread`
- `IsRuningQuest`
- selected-device state

`TimerCheckDevices_Tick`, `LoadDevices`, `LoadListDevices`, `waitDevice`, `StartQuestDevice` and `StartAllSelectedDevice` indicate the UI continuously reconciles discovered instances with automation state.

## 7. Coordinate systems — a hidden reliability risk

At least three coordinate spaces may exist:

1. Android display coordinates used by ADB tap/swipe;
2. emulator client-window coordinates used by SendMessage/PostMessage;
3. Windows screen/global coordinates used by SendInput/mouse functions.

Image templates are small pixel crops, and helper APIs include scaling/resizing and percentage-based ADB taps. A rebuilt implementation should explicitly model coordinate transforms rather than allowing each feature to assume one coordinate system.

Recommended normalized contract:

```text
ObservedPoint(image-space)
 -> device viewport transform
 -> canonical game viewport point
 -> actuator transform (ADB/window/screen)
 -> one action
 -> re-observe target state
```

## 8. What is not yet proven

The helper DLL exposes both ADB and Win32 control, but static evidence currently does not map every donor feature to one exact channel. Do not state “all clicks use ADB” or “all clicks use SendMessage” without runtime/call-site proof.

The next targeted proof should record, for one harmless action on one emulator:

- method entered;
- active DeviceID/port/window handle;
- screenshot source;
- selected actuator;
- coordinates before/after transform;
- resulting visual state.
