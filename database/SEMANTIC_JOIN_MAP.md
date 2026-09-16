# Semantic Join Map — how DATA-333 tables connect

DATA-333 is useful only if records can be joined instead of read as isolated dumps.

## Feature -> method -> binary identity

```text
features/FEATURE_INDEX.feature
 -> features/FEATURE_METHOD_MAP.feature
 -> (assembly, rid)
 -> dotnet/METHOD_CATALOG_*.csv
 -> declaring_type / RVA / body_status
 -> dotnet/TYPE_CATALOG.csv
```

For original/debug naming evidence:

```text
method/property name
 <-> dotnet/PDB_IDENTIFIERS.csv.identifier
```

High overlap between PDB symbols and surviving managed metadata means many feature names are not guesses even where bodies are protected.

## Feature -> state/property

```text
feature keyword
 -> dotnet/MODEL_PROPERTIES.feature_tags
 -> declaring_type + property
```

Core joins:

- `DeviceInfo` -> per-emulator mutable state/thread/account/coordinates;
- `MainWindow` -> global/user settings and feature policy;
- `AccountInfo` -> per-account login/server/coordinate data;
- `QuestInfo` -> per-quest execution state;
- `NoxMultiIni` -> process/port identity.

## Feature -> visual detector

```text
features/FEATURE_INDEX.feature
 -> features/FEATURE_ASSET_MAP.feature
 -> path / dimensions / sha256
 -> assets/IMAGE_TEMPLATE_INDEX_*.csv
 -> assets/IMAGE_EXACT_DUPLICATES.csv
```

Do not treat filename/path tagging as proof of exact call-site. It is a query-oriented donor association; exact caller needs protected-body/runtime proof.

## Main external surface -> helper implementation

```text
control/MAIN_STATIC_CONTROL_REFERENCES
  parent_type + member_name
 -> control/KAUTOHELPER_API
  declaring_type + name
 -> control/KAUTOHELPER_CALL_GRAPH
  caller_type + caller_method
 -> native/framework method edge
```

Examples:

```text
SendClickOnPosition
 -> MakeLParamFromXY
 -> PostMessage

CaptureWindow
 -> GetWindowDC/GetWindowRect
 -> CreateCompatibleDC/CreateCompatibleBitmap
 -> BitBlt
 -> Image.FromHbitmap

FindOutPoint
 -> EmguCV MatchTemplate
 -> MinMax
```

`control/CONTROL_STACK.csv` pre-materializes these important joins.

## Nox identity join

```text
KhungCode_Auto.NoxMultiIni pid/vmpid/Ports
 + KAutoHelper.NoxMultiIni.GetNoxMultiIni
 + ProcessHelper.GetNetStatPorts
 + Port.pid/port_number
 -> Process.GetProcessById
 -> MainWindowTitle
 -> AutoControl.FindWindowHandlesFromProcesses
 -> DeviceInfo.DeviceHandle
```

This establishes a host process/port/window isolation mechanism. It does **not** establish ADB input usage.

## ADB capability join and non-reference boundary

```text
KAUTOHELPER_API ADBHelper.Tap/Swipe/ScreenShoot/ConnectNox
 + HELPER_STRING_INDICATORS exact adb command templates
```

is a verified bundled capability.

But:

```text
MAIN_STATIC_CONTROL_REFERENCES
 -> ADBHelper.Delay only
```

So `Tap/Swipe/ScreenShoot/ConnectNox` must remain `BUNDLED_NOT_MAIN_REFERENCED` until a dynamic/reflection/call-site proof appears.

## Persistence join

```text
persistence/PERSISTENCE_LAYOUT.path
 -> snapshot/ARTIFACT_MANIFEST path/hash
 -> dotnet EXTERNAL_MEMBERREFS File/Directory APIs
 -> PDB/method names when feature ownership is recoverable
```

Never join by plaintext secret values; those are intentionally excluded.

## DATA-333 -> DATA-2222 bridge

DATA-333 preserves donor **policy/state-machine clues**. DATA-2222 preserves stronger client semantic state/action contracts.

Typical bridge:

```text
333 feature method/state/assets
 -> infer donor intent/policy
 -> 222 semantic runtime state
 -> 222 semantic action where solved
 -> visual/Win32 fallback only where semantic surface is absent
 -> fresh proof
```

This bridge is directional: do not mistake donor pixel templates for canonical game object identity when DATA-2222 has a semantic ID/state source.
