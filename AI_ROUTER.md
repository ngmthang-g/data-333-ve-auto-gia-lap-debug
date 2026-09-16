# AI Router — DATA-333

Read `AI_BOOTSTRAP.md` first, then route to generated data before prose analysis.

## Primary routes

| Question | Start here | Only then |
|---|---|---|
| What files/build is this? | `database/snapshot/SNAPSHOT_SUMMARY.json`, artifact manifests | binary manifest/sections |
| Class/method/property/RVA | `database/dotnet/TYPE_CATALOG.csv`, `MODEL_PROPERTIES.csv`, method chunks | PDB identifiers |
| Feature methods/assets/state | `database/features/FEATURE_INDEX.csv` | feature method/asset maps |
| How main controls windows | `database/control/MAIN_STATIC_CONTROL_REFERENCES.csv` | `CONTROL_STACK.csv`, helper call graph |
| Exact helper API | `database/control/KAUTOHELPER_API.csv` | helper call graph |
| ADB capability vs actual use | `CONTROL_PRIMITIVES.csv`, `HELPER_STRING_INDICATORS.csv` | main static refs |
| Nox/PID/port/HWND mapping | `database/SUBSYSTEM_SOURCE_MAP.md` | `CONTROL_STACK.csv` `NOX-IDENTITY` |
| OCR/template detection | `CONTROL_STACK.csv` + feature asset map | image catalog |
| Threads/multi-device | `control/THREADING_REFERENCES.csv` + `MODEL_PROPERTIES.csv` | targeted runtime proof |
| File persistence | `persistence/PERSISTENCE_LAYOUT.csv`, `FILE_IO_REFERENCES.csv` | sensitive schema only |
| Login/license/update | `control/HTTP_AUTH_UPDATE_REFERENCES.csv` | auth feature methods/models |
| Cross-table relationship | `database/SEMANTIC_JOIN_MAP.md` | exact rows |
| Relationship to game semantics | `analysis/05_DATA222_BRIDGE.md` | DATA-2222 |
| Deep corrected architecture | `analysis/06_DATA_MATERIALIZATION_AND_DEEP_CONTROL.md` | targeted runtime trace |

## Core rule

```text
lookup specialized data
 -> join exact records
 -> separate identity/capability/reference/call-site proof
 -> reverse/trace only the unresolved edge
```

## Evidence priority

1. exact main static metadata/MemberRefs;
2. clean KAutoHelper IL + call graph;
3. PDB original/debug identifiers;
4. exact image/file/hash evidence;
5. protected main method identity/RID/RVA;
6. inference;
7. runtime trace for protected call-site/order.

## Important corrected control rule

KAutoHelper contains full ADB methods and exact command templates. That proves bundled capability, **not active gameplay use**.

The main managed donor statically references Win32 window discovery/click/key/text/drag, `CaptureWindow/CropImage`, OpenCV `FindOutPoint(s)` and Tesseract OCR. From `ADBHelper`, it statically references `Delay` only.

Until dynamic/reflection evidence says otherwise, route donor input/capture questions through the Win32/vision stack first.

## Network rule

HTTP/JSON/updater references support login/license/update control-plane behavior. No current static evidence proves direct gameplay socket/protocol control by this external donor.

## Protected-body rule

Production EXE protection and protected/non-standard bodies in the managed donor mean exact protected routine sequencing should be recovered with narrow runtime traces. Do not broad-unpack merely because an internal branch is unknown.
