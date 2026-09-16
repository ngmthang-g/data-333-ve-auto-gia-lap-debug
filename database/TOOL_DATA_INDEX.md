# Tool Data Index — DATA-333 canonical machine-readable lookup map

Status: **CURRENT STATIC MATERIALIZATION for the supplied Auto Debug snapshot.**

## Core lookup rule

```text
question/feature
 -> specialized index
 -> exact row / state / RID / RVA / asset
 -> source/join map for interpretation
 -> full catalog only if needed
 -> targeted runtime proof for protected/dynamic behavior
```

Do not start by scanning every DLL/PDB/image again.

## Highest-value entrypoints

- `features/FEATURE_INDEX.csv` — cleaned feature counts/router.
- `features/FEATURE_STATE_JOIN.csv` — feature -> state properties -> behavior methods -> asset volume.
- `features/CORE_METHOD_RVA_INDEX.csv` — high-value donor methods with exact RID/RVA/body status.
- `dotnet/DEVICE_STATE_CATALOG.csv` — AccountInfo/DeviceInfo/QuestInfo/Nox state properties and accessor RVAs.
- `features/ACTIVITY_EVIDENCE_MATRIX.csv` — Thủy Lao / Ác Tặc / TBD static evidence.
- `control/MAIN_STATIC_CONTROL_REFERENCES.csv` — what the main donor actually references.
- `control/CONTROL_CALL_CHAINS.csv` — compact exact decoded helper chains.
- `FACTS.jsonl` — atomic conclusions/evidence boundaries.

Canonical interpretation: `../analysis/07_FEATURE_STATE_AND_PROTECTED_BODY_MAP.md`.

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
2. `dotnet/DEVICE_STATE_CATALOG.csv` for high-value mutable models
3. `dotnet/MODEL_PROPERTIES.csv` for the broad property fallback
4. `features/FEATURE_STATE_JOIN.csv`
5. `features/CORE_METHOD_RVA_INDEX.csv`
6. `features/FEATURE_METHOD_MAP.csv` when full generated feature joins are needed
7. matching `dotnet/METHOD_CATALOG_*.csv` for complete RID/RVA/body status
8. `dotnet/FIELD_CATALOG.csv` only when backing-field identity is needed
9. `dotnet/PDB_IDENTIFIERS.csv` for original/debug symbol evidence.

Current core types include `KhungCode_Auto.MainWindow`, `DeviceInfo`, `AccountInfo`, `QuestInfo`, `NoxMultiIni`, login/request/response models and WPF support types.

### Body-status rule

Main donor contains many protected/non-standard method bodies. Do not equate a hidden body with missing knowledge.

```text
valid_il_header
 -> decompile/read statically first

protected_or_nonstandard
 -> join method RVA + device state + assets + main MemberRefs + helper call chain
 -> runtime-trace only the unresolved edge/order
```

Examples and proof queue: `../analysis/07_FEATURE_STATE_AND_PROTECTED_BODY_MAP.md`.

## Feature lookup

Start at `features/FEATURE_INDEX.csv`.

Specialized maps:

- `FEATURE_STATE_JOIN.csv` — clean semantic feature/state/method join;
- `CORE_METHOD_RVA_INDEX.csv` — exact high-value method addresses/status;
- `FEATURE_METHOD_MAP.csv` — full generated feature -> method mapping;
- `FEATURE_ASSET_MAP.csv` — feature -> PNG template/hash/dimensions;
- `ACTIVITY_EVIDENCE_MATRIX.csv` — activity-specific compact evidence.

Materialized domains include orchestration, auth/update, account/login, Train/combat, party/follow, Ác Tặc, Thủy Lao, TBD flow, sell/inventory, storage, consumables, heal/buff, travel/NPC, pet/mount, trade, quest/level, captcha, vision and scheduler.

### Classifier quality rule

The cleaned feature index uses strict token/boundary matching. Do not reintroduce naive substrings such as `mana -> Manager`, `pt -> Opacity`, or `quest -> Request`.

## Observation / vision / OCR

Use:

- `control/MAIN_STATIC_CONTROL_REFERENCES.csv`
- `control/CONTROL_STACK.csv`
- `control/CONTROL_CALL_CHAINS.csv`
- `control/KAUTOHELPER_API.csv`
- `control/KAUTOHELPER_CALL_GRAPH.csv`
- `assets/IMAGE_TEMPLATE_INDEX_*.csv`.

Verified main static surfaces include `CaptureWindow`, `CropImage`, `FindOutPoint(s)`, Win32 click/keyboard/drag and Tesseract `Process/GetText`.

Exact low-level chains include:

```text
CaptureWindow -> user32/GDI32 -> BitBlt -> Image
FindOutPoint -> MatchTemplate -> MinMax -> Point
SendClickOnPosition -> MakeLParamFromXY -> PostMessage
```

## Emulator/window discovery

Use:

- `dotnet/DEVICE_STATE_CATALOG.csv` for `NoxMultiIni`, PID/vmPID/Ports and DeviceInfo handle/identity state;
- `control/MAIN_STATIC_CONTROL_REFERENCES.csv` for process/window helper refs;
- `control/CONTROL_CALL_CHAINS.csv` for `GetNoxTitleFromADBPort`;
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

Do not promote ADB port discovery into proof of ADB gameplay control.

## Win32 actuation

Use:

- `control/MAIN_STATIC_CONTROL_REFERENCES.csv`
- `control/CONTROL_PRIMITIVES.csv`
- `control/CONTROL_STACK.csv`
- `control/CONTROL_CALL_CHAINS.csv`
- `control/KAUTOHELPER_CALL_GRAPH.csv`.

Current static evidence strongly supports HWND/window-message actuation and GDI capture.

## ADB capability

Use:

- `control/KAUTOHELPER_API.csv`
- `control/KAUTOHELPER_CALL_GRAPH.csv`
- `control/HELPER_STRING_INDICATORS.csv`
- `control/CONTROL_PRIMITIVES.csv`.

Bundled ADB helper implements connect/tap/swipe/key/text/screenshot paths.

**Evidence boundary:** `MAIN_STATIC_CONTROL_REFERENCES.csv` currently contains only `KAutoHelper.ADBHelper.Delay` from that helper family. No static main MemberRef to `Tap`, `Swipe`, `ScreenShoot` or `ConnectNox` is present in this managed snapshot. A protected/indirect runtime path remains possible but requires proof.

## Threading / per-device execution

Use:

- `dotnet/DEVICE_STATE_CATALOG.csv`
- `control/THREADING_REFERENCES.csv`
- `features/CORE_METHOD_RVA_INDEX.csv`.

`DeviceInfo` carries `QuestThread`, `CheckQuestThread`, `IsRuningQuest`, screen cache, handle/identity and feature-specific state. Main references Thread Start/Sleep/Abort/Suspend/Resume plus Dispatcher/DispatcherTimer/Timer/Task APIs.

Treat old Thread `Abort/Suspend/Resume` usage as a reliability risk, not a design recommendation.

## Activity flows

For Thủy Lao / Ác Tặc / TBD start with:

1. `features/ACTIVITY_EVIDENCE_MATRIX.csv`
2. `features/FEATURE_STATE_JOIN.csv`
3. `dotnet/DEVICE_STATE_CATALOG.csv`
4. `features/CORE_METHOD_RVA_INDEX.csv`
5. only the matching image-template rows.

Thủy Lao static assets/state strongly indicate a 12-stage visual progression. Exact branch transitions remain protected/runtime truth.

## Persistence / account/config files

Use:

- `persistence/PERSISTENCE_LAYOUT.csv`
- `persistence/FILE_IO_REFERENCES.csv`
- `snapshot/SENSITIVE_TEXT_SCHEMAS.csv`.

The app references ordinary text file I/O. Values from credential/key-looking files are intentionally excluded from the KB.

## Login/license/update control plane

Use:

- `control/HTTP_AUTH_UPDATE_REFERENCES.csv`
- `features/FEATURE_STATE_JOIN.csv` row `auth_update`
- `dotnet/MODEL_PROPERTIES.csv` for token/update/response-model context.

This is separate from gameplay control. HTTP/auth/update references are not proof of direct game protocol automation.

## Image assets

Use:

- `assets/FOLDER_SUMMARY.csv`
- `assets/IMAGE_TEMPLATE_INDEX_*.csv`
- `assets/IMAGE_EXACT_DUPLICATES.csv`.

There are 1,393 PNG files but 1,180 byte-unique images. Exact duplicates should be deduplicated before future template migration/training.

## Full external-reference fallback

If specialized data does not answer the question, use:

`dotnet/EXTERNAL_MEMBERREFS.csv`.

Query it narrowly; do not read the catalog sequentially.

## Hard rule

**Lookup before reversing. Static metadata proves identity, state surfaces and available/reference mechanisms. Runtime tracing is reserved for the exact protected branch/call-site/threshold/action-result that remains unresolved.**
