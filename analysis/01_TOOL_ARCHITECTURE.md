# 01 — Tool architecture and execution model

## 1. Snapshot summary

The supplied Debug bundle contains 1,450 files totaling 146,978,306 bytes. Major contents:

- 2 executables;
- 36 DLLs;
- 3 PDBs;
- 1,393 PNG templates/crops;
- EmguCV/OpenCV runtime;
- Tesseract + English trained data;
- ADB WinAPI libraries;
- KAutoHelper;
- AutoUpdater.NET;
- WPF/AvalonDock/Toolkit dependencies;
- plaintext runtime/config persistence under `luufile/`.

The source PDB points to a C# WPF project path similar to:

`D:\TOOL\THANLONG_V2\Auto_Bac_TongHop_V3\KhungCode_Auto\...`

Source files directly named by PDB include `MainWindow.xaml.cs`, `login.xaml.cs`, `MouseUtilities.cs`, `ListViewDragDropManager.cs`, `DragAdorner.cs`, generated `App.g.cs`, and resources.

## 2. Application layers

### Layer A — UI shell / operator control

**VERIFIED-PDB**

`KhungCode_Auto.MainWindow` is the central application class. The PDB exposes WPF event handlers and device/quest orchestration names such as:

- `Window_Loaded`
- `Button_Click*`
- `LoadDevices`
- `LoadListDevices`
- `LoadQuest`
- `StartQuestDevice`
- `StartAllSelectedDevice`
- `TimerCheckDevices_Tick`
- `TimerCheckAuthorize_Tick`
- `TimerCheckHenGio_Tick`

The presence of `ListViewDragDropManager<T>`, `DragAdorner`, `MouseUtilities` and drag/drop events indicates the UI supports list ordering/rearrangement, likely for devices/accounts/tasks.

### Layer B — authentication / license / update

**VERIFIED-PDB + VERIFIED-BINARY-STRING**

Classes/symbols:

- `KhungCode_Auto.LogIn`
- `KhungCode_Auto.Cons`
- `LoginResponse`
- `UserInfoDetail`
- `Request`
- `CheckLicense`
- `CheckKey`
- `Login`
- `UserInfo`
- `CheckUpdate`
- `AutoUpdaterOnCheckForUpdateEvent`
- `HttpClient`, `HttpWebRequest`, `Newtonsoft.Json`
- token/user/project/country/update properties

This is a separate control plane from gameplay automation. No current static evidence proves direct gameplay socket/protocol control from this layer.

### Layer C — emulator/process discovery

**VERIFIED-PDB + VERIFIED-METADATA**

The tool contains both its own `NoxMultiIni` model and KAutoHelper's Nox/process helpers. Evidence includes:

- `GetNoxMultiIni`
- `GetNoxTitleFromADBPort`
- `ProcessHelper.GetNetStatPorts`
- process/window handle discovery
- Nox `multi.ini` path support
- local ADB port handling
- `pid`, `vmpid`, `Ports`, `DeviceHandle`, `DeviceID`, `DeviceName`

This layer resolves a human-visible emulator instance to process/window/ADB identities.

### Layer D — per-device state model

**VERIFIED-PDB**

Core models:

- `DeviceInfo`
- `AccountInfo`
- `QuestInfo`
- `CorinateStatus`
- `item`

Observed properties show state for:

- device identity/handle/PID/VM PID;
- selected device;
- account list/current account;
- quest thread/check thread/running flag;
- auto-login;
- train map/level/settings;
- party/team settings;
- item/sell/storage/pet settings;
- dungeon/activity status;
- coordinate/click state;
- image screen cache;
- scheduling and counters.

This strongly supports a design where **each emulator/device owns independent mutable automation state**.

### Layer E — observation/perception

**VERIFIED-METADATA + VERIFIED-ASSET**

The tool has four observation mechanisms:

1. ADB screenshot path (`ADBHelper.ScreenShoot` and screencap/pull command literals);
2. window/screen capture (`CaptureHelper.CaptureWindow`, `CaptureScreen`, crop/resize);
3. OpenCV/EmguCV template/color matching (`ImageScanOpenCV` and MainWindow `FindImage*`/`FindAndClick*` helpers);
4. OCR/Tesseract (`Get_Text_From_Image`, Tesseract runtime/traineddata, captcha-related async methods).

The bundle contains 1,393 PNG files. These are predominantly small UI fragments, not full screenshots, which is consistent with template matching.

### Layer F — decision / feature logic

**VERIFIED-PDB** for method/property names; exact branch order is only partially reconstructed.

High-value donor routines include:

- `trainLEVEL1`
- `setupautotrain`
- `setupautothuylao`
- `setupautotrungac`
- `sellItemm`
- `catdovaokho`
- `laydotrongkho`
- `truyenmap`
- `toinpc_duoc`
- `toinpcbanitem_daily`
- `toinpc_pet_daily`
- `toinpcthuylao`
- `toinpcTBD`
- `xuatpet`
- `nhanitem`
- `nhannvTBD`
- `lienketmau_manalenauto`
- `TAO_PT_1NGUOI`
- `THOAT_PT`
- `THOAT_VAOLAI_PT`
- `Truyenvetochau`

The feature code appears concentrated in a very large `MainWindow.xaml.cs`, rather than cleanly separated service classes.

### Layer G — actuation

**VERIFIED-METADATA + VERIFIED-BINARY-STRING**

Two independent actuator families exist:

- ADB: tap, swipe, long press, keyevent, text input;
- Win32: SendMessage/PostMessage/SendInput, control/window handle click, keyboard, mouse drag/scroll.

The presence of both does **not** prove all features use both. Runtime/call-site proof is still needed for exact routing.

### Layer H — persistence

**VERIFIED-ASSET + VERIFIED-PDB**

`luufile/` contains runtime/config folders including:

- `SETTING/`
- `taikhoan/`
- `matkhau/`
- `maptrain/`
- `sttteam/`
- `thucanPET/`
- `vitri/`
- `TOADO_ACTAC/data/`

PDB symbols include many matching configuration properties and `ReadAllText`, `ReadAllLines`, `WriteAllText` calls. This supports file-based persistence rather than a database.

## 3. Main execution lifecycle

The most defensible reconstructed lifecycle is:

```text
App start
  -> LogIn / license check
  -> update check
  -> MainWindow load
  -> discover emulator processes/windows/ADB ports
  -> build ListDevices / DeviceInfo
  -> load account + quest/config files
  -> periodic device/authorization/schedule timers
  -> operator selects device(s)/quest(s)
  -> StartAllSelectedDevice
       -> StartQuestDevice(device)
       -> per-device QuestThread / CheckQuestThread
       -> acquire screen
       -> detect state by template/color/OCR
       -> execute one UI/input action
       -> wait/re-observe
       -> branch/recover/repeat
```

The exact threading primitives and synchronization policy still need targeted decompilation/runtime tracing. The PDB explicitly exposes `QuestThread`, `CheckQuestThread`, thread fields and per-device running state, so concurrent per-device execution is strongly supported.

## 4. Architectural weaknesses visible from static evidence

1. **Monolithic feature controller.** Many unrelated feature routines live in `MainWindow`, increasing hidden coupling and making state arbitration difficult.
2. **Pixel/template dependence.** Hundreds of tiny templates imply sensitivity to scale, font, theme, antialiasing, UI movement and game updates.
3. **Dual actuator paths.** ADB and Win32 inputs can diverge in coordinate systems/window focus unless normalized behind one abstraction.
4. **File-based mutable state.** Plaintext persistence is simple but weak for validation, atomic updates, schema evolution and secrets.
5. **Protection/obfuscation hides behavior, not risk.** Themida protects the binary but does not protect plaintext config/key files stored beside it.
6. **Potential fixed-delay behavior.** Numerous wait/time variables are visible; exact use must be verified. A rebuilt tool should prefer state proof/timeout loops over sleep-as-success.
7. **Captcha coupling.** Captcha solver-related symbols exist. A modern rebuild should make captcha a pause/manual intervention state.

## 5. Important non-findings

- No static evidence currently establishes direct game packet/socket control by this external tool.
- WebView2 DLLs are bundled, but active MainWindow usage has not been proven from the recovered symbols.
- The exact caller choice between ADB screenshot and Win32 window capture is not yet proven per feature.
- The exact threshold values for each image template are not yet recovered.

These gaps should remain explicit rather than being guessed.
