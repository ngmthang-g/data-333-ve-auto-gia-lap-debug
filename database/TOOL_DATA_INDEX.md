# Tool Data Index — DATA-333 canonical machine-readable lookup map

Status: **CURRENT STATIC MATERIALIZATION for the supplied Auto Debug snapshot.**

## Core lookup rule

```text
question/feature
 -> specialized index
 -> exact row/RID/RVA/asset
 -> source/join map for interpretation
 -> full catalog only if needed
 -> targeted runtime proof for dynamic branch/call-site behavior
```

## Snapshot / file identity

Use:

- `snapshot/SNAPSHOT_SUMMARY.json`
- `snapshot/ARTIFACT_MANIFEST_0001_0750.csv`
- `snapshot/ARTIFACT_MANIFEST_0751_1450.csv`
- `binary/BINARY_MANIFEST.csv`
- `binary/BINARY_SECTIONS.csv`.

Use SHA-256 before assuming two Debug packages are the same donor build.

## Managed architecture / classes / methods

Use in this order:

1. `dotnet/TYPE_CATALOG.csv`
2. `dotnet/MODEL_PROPERTIES.csv`
3. `features/FEATURE_METHOD_MAP.csv` for feature-specific methods
4. matching `dotnet/METHOD_CATALOG_*.csv` for RID/RVA/body status
5. `dotnet/FIELD_CATALOG.csv` only when field identity is needed
6. `dotnet/PDB_IDENTIFIERS.csv` for original/debug symbol evidence.

Current core types include `KhungCode_Auto.MainWindow`, `DeviceInfo`, `AccountInfo`, `QuestInfo`, `NoxMultiIni`, login/request/response models and WPF support types.

## Feature lookup

Start at `features/FEATURE_INDEX.csv`.

Specialized maps:

- `FEATURE_METHOD_MAP.csv` — feature -> method RID/RVA/body status;
- `FEATURE_ASSET_MAP.csv` — feature -> PNG template/hash/dimensions.

Materialized domains include orchestration, auth/update, account/login, Train/combat, party/follow, Ác Tặc, Thủy Lao, TBD flow, sell/inventory, storage, consumables, heal/buff, travel/NPC, pet/mount, trade, quest/level, captcha, vision and scheduler.

## Observation / vision / OCR

Use:

- `control/MAIN_STATIC_CONTROL_REFERENCES.csv`
- `control/CONTROL_STACK.csv`
- `control/KAUTOHELPER_API.csv`
- `control/KAUTOHELPER_CALL_GRAPH.csv`
- `assets/IMAGE_TEMPLATE_INDEX_*.csv`.

Verified active static surfaces include `CaptureWindow`, `CropImage`, `FindOutPoint(s)`, and Tesseract `Process/GetText`.

## Emulator/window discovery

Use:

- `dotnet/MODEL_PROPERTIES.csv` for `NoxMultiIni`, PID/vmPID/Ports, `DeviceInfo.DeviceHandle/DeviceID/DeviceName`;
- `control/MAIN_STATIC_CONTROL_REFERENCES.csv` for `ProcessHelper.GetNetStatPorts`, `Port.pid/port_number`, window helper refs;
- `control/CONTROL_STACK.csv` row `NOX-IDENTITY`;
- `control/HELPER_STRING_INDICATORS.csv` for `\\Local\\Nox\\multi.ini` and `netstat.exe` literals.

Static identity model:

```text
Nox multi.ini pid/vmpid
 + host netstat PID/port mapping
 -> process identity
 -> MainWindowTitle / HWND
 -> DeviceInfo
```

Do not silently promote ADB port discovery into proof of ADB gameplay control.

## Win32 actuation

Use:

- `control/CONTROL_PRIMITIVES.csv`
- `control/CONTROL_STACK.csv`
- `control/KAUTOHELPER_CALL_GRAPH.csv`.

Verified helper chains include:

- click -> `MakeLParamFromXY -> PostMessage`;
- drag -> `PostMessage` sequence + delay;
- capture -> user32/GDI32 `BitBlt` pipeline;
- template match -> EmguCV/OpenCV `MatchTemplate -> MinMax`.

## ADB capability

Use:

- `control/KAUTOHELPER_API.csv`
- `control/HELPER_STRING_INDICATORS.csv`
- `control/CONTROL_PRIMITIVES.csv`.

Exact bundled command templates include `adb devices`, localhost connect, tap/swipe/key/text, screencap/pull/rm and display dumpsys.

**Boundary:** `MAIN_STATIC_CONTROL_REFERENCES.csv` currently contains only `KAutoHelper.ADBHelper.Delay`. No static main MemberRef to `Tap`, `Swipe`, `ScreenShoot` or `ConnectNox` is present.

## Threading / per-device execution

Use:

- `control/THREADING_REFERENCES.csv`
- `dotnet/MODEL_PROPERTIES.csv`
- `features/FEATURE_METHOD_MAP.csv`.

`DeviceInfo` carries `QuestThread`, `CheckQuestThread`, `IsRuningQuest`; main references Thread Start/Sleep/Abort/Suspend/Resume plus Dispatcher/DispatcherTimer/Timer/Task APIs.

Treat old Thread `Abort/Suspend/Resume` usage as a reliability risk, not a design recommendation.

## Persistence / account/config files

Use:

- `persistence/PERSISTENCE_LAYOUT.csv`
- `persistence/FILE_IO_REFERENCES.csv`
- `snapshot/SENSITIVE_TEXT_SCHEMAS.csv`.

The app statically references `File.ReadAllText`, `WriteAllText`, `ReadAllLines`, `Exists` and directory enumeration. Values from credential/key-looking files are intentionally excluded.

## Login/license/update control plane

Use:

- `control/HTTP_AUTH_UPDATE_REFERENCES.csv`
- `features/FEATURE_METHOD_MAP.csv` feature `auth_update`
- `dotnet/MODEL_PROPERTIES.csv` for AccessToken/LoginStamp/UpdateURL and response models.

This is a separate control plane. Its presence is not evidence of direct gameplay packet control.

## Image assets

Use:

- `assets/FOLDER_SUMMARY.csv`
- `assets/IMAGE_TEMPLATE_INDEX_*.csv`
- `assets/IMAGE_EXACT_DUPLICATES.csv`.

There are 1,393 PNG files but only 1,180 byte-unique images. Exact duplicate groups should be deduplicated before any future template retraining or asset migration.

## Full external reference fallback

If a specialized surface does not answer the question, use:

`dotnet/EXTERNAL_MEMBERREFS.csv`.

This is analogous to DATA-2222's broad fallback database: query it, do not read it sequentially.

## Hard rule

**Lookup before reversing. Static metadata proves identity and available/reference surfaces; only runtime tracing can prove the exact protected feature call-site, branch ordering, coordinates, thresholds and resulting game state.**
