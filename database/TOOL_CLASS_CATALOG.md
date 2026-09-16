# Tool class/type catalog

Evidence comes from the supplied PDB and managed metadata. Compiler-generated display/state-machine classes are listed only where they reveal ownership of async/event behavior.

## A. Source-level KhungCode_Auto types — VERIFIED-PDB

| Type | Role inferred from direct members |
|---|---|
| `KhungCode_Auto.App` | WPF application bootstrap |
| `KhungCode_Auto.LogIn` | login window / operator authentication UI |
| `KhungCode_Auto.Cons` | HTTP/auth/license client helpers (`Login`, `UserInfo`, `CheckKey`) |
| `KhungCode_Auto.LoginResponse` | token/login response model |
| `KhungCode_Auto.UserInfoDetail` | user/project/country/license metadata model |
| `KhungCode_Auto.Request` | request model |
| `KhungCode_Auto.MainWindow` | central UI + device orchestration + feature logic + image helpers |
| `KhungCode_Auto.DeviceInfo` | per-emulator/device runtime state |
| `KhungCode_Auto.AccountInfo` | account/config state |
| `KhungCode_Auto.QuestInfo` | per-task/auto-feature definition/state |
| `KhungCode_Auto.CorinateStatus` | coordinate/status model |
| `KhungCode_Auto.NoxMultiIni` | Nox PID/VM PID/port mapping |
| `KhungCode_Auto.item` | small item/data model |
| `KhungCode_Auto.TwoCaptResponseStatus` | captcha/recognition response status model |

### Compiler-generated evidence

PDB contains async/event state-machine ownership such as:

- `KhungCode_Auto.Cons.<Login>d__*`
- `KhungCode_Auto.Cons.<UserInfo>d__*`
- `KhungCode_Auto.Cons.<CheckKey>d__*`
- `KhungCode_Auto.MainWindow.<AutoUpdaterOnCheckForUpdateEvent>d__*`
- `KhungCode_Auto.MainWindow.<SoveNormalCapt>d__*`
- `KhungCode_Auto.MainWindow.<Nomal>d__*`
- display classes for `TimerCheckDevices`, `StartQuestDevice`, `StartAllSelectedDevice`

These prove async/task/lambda behavior in those subsystems even where obfuscation blocks clean decompilation.

## B. WPF drag/drop utility types — VERIFIED-PDB

- `WPF.JoshSmith.ServiceProviders.UI.ListViewDragDropManager<T>`
- `WPF.JoshSmith.ServiceProviders.UI.ListViewItemDragState`
- `WPF.JoshSmith.ServiceProviders.UI.ProcessDropEventArgs<T>`
- `WPF.JoshSmith.Controls.Utilities.MouseUtilities`
- `WPF.JoshSmith.Adorners.DragAdorner`

Relevant methods include list-view preview mouse events, drag enter/leave/over/drop, adorner initialization/update and mouse-position helpers.

These are UI-shell utilities, not game control primitives.

## C. KAutoHelper types and exact public/internal method surface — VERIFIED-METADATA

### `KAutoHelper.ADBHelper`

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

### `KAutoHelper.NoxMultiIni`

- properties `pid`, `vmpid`, `Ports`
- `GetNoxMultiIni`
- `GetNoxTitleFromADBPort`

### `KAutoHelper.AutoControl`

Win32 discovery/input wrapper. High-value managed methods:

- `BringToFront`
- `IsWindowVisible_`
- `FindWindowHandle`
- `FindWindowHandlesFromProcesses`
- `FindWindowHandleFromProcesses`
- `FindWindowExFromParent`
- `FindWindowByIndex`
- `GetControlHandleFromControlID`
- `GetChildHandle`
- `FindHandleWithText`
- `FindHandlesWithText`
- `FindHandle`
- `FindHandles`
- `SendClickOnControlById`
- `SendClickOnControlByHandle`
- `SendClickOnPosition`
- `SendDragAndDropOnPosition`
- `SendDragAndDropOnMultiPosition`
- `MouseMoveDrag`
- `SendClickDownOnPosition`
- `SendClickUpOnPosition`
- `SendText`
- `SendKeyBoardPress`
- `SendKeyBoardPressStepByStep`
- `SendKeyBoardUp/Down`
- `SendTextKeyBoard`
- `SendKeyFocus`
- `SendMultiKeysFocus`
- `SendStringFocus`
- `SendKeyPress/Down/Up`
- `MouseClick`
- `MouseDragX/Y`
- `MouseScroll`
- `Click`
- `GetWindowRect`
- `GetGlobalPoint`
- `GetText`
- `GetClassName`
- `MakeLParam/MakeLParamFromXY`

Native import surface includes FindWindow/EnumChildWindows/GetWindowText/GetClassName/SendMessage/PostMessage/SendInput/GetWindowRect/SetForegroundWindow/mouse_event.

### `KAutoHelper.CaptureHelper`

- `CaptureScreen`
- `CaptureWindow`
- `ScaleImage`
- `ResizeImage`
- `CaptureWindowToFile`
- `CaptureScreenToFile`
- `CaptureImage`
- `CropImage`

### `KAutoHelper.ImageScanOpenCV`

- `GetImage`
- `Find` overloads
- `FindOutPoint`
- `FindOutPoints`
- `FindColor` overloads
- `RecolizeText`
- `SplitImageInFolder`
- `ThreshHoldBinary`
- pixel replacement/conversion helpers

### `KAutoHelper.Get_Text_From_Image`

- `information`
- `Get_Text` overloads
- `make_new_image`
- `split_image`
- `Image_Equal`
- `check_folder_exists`

### `KAutoHelper.ProcessHelper`

- `GetWindowTitles`
- `EnumWindowsCallback`
- `TitleMatches`
- `GetWindowTitle`
- `GetNetStatPorts`
- `LookupProcess`

### Other helper/native types

- `BitmapConversion`
- `FindWindow`
- `Port`
- `ParentProcessUtilities`
- `ThamKhao`
- `GDI32`
- `User32`
- `RECT`
- input structures/enums (`INPUT`, `MOUSEINPUT`, `KEYBDINPUT`, `VKeys`, `ADBKeyEvent`, etc.)

## D. High-value MainWindow source symbols — VERIFIED-PDB

### Orchestration

`LoadDevices`, `LoadListDevices`, `LoadQuest`, `StartQuestDevice`, `StartAllSelectedDevice`, `waitDevice`, timers.

### Perception helpers

`FindImage*`, `FindAndClick*`, `FindColor`, `SoluongImage*`, `getnhieuvitrihinhanh`, `getsonhieuchotrenscreen`, `ScaleImage`, `ResizeImage`, `ImageToByteArray`.

### Feature routines

`trainLEVEL1`, `setupautotrain`, `setupautothuylao`, `setupautotrungac`, `sellItemm`, `catdovaokho`, `laydotrongkho`, `truyenmap`, `toinpc*`, `xuatpet`, `nhanitem`, `nhannvTBD`, `lienketmau_manalenauto`, party helpers.

## E. Important static limitation

The production executable is Themida-protected and the alternate managed executable uses obfuscation/anti-decompiler metadata. Therefore this catalog is a **symbol/type surface**, not a complete recovered call graph. Exact calls, conditions, thresholds and branch ordering should be promoted only after targeted runtime or successful method-body recovery.
