# Database navigation index — DATA-333 Auto Debug donor

> Machine/AI-readable knowledge materialized from the supplied Auto Thần Long Debug snapshot. The primary purpose is to preserve **what the donor tool contains, how it observes, decides and controls emulator windows, and which feature/state names survive**, without repeating broad reverse work.

## Start here

Canonical lookup router:

`TOOL_DATA_INDEX.md`

High-value machine-readable entry points:

- `FACTS.jsonl` — atomic verified/probable/non-reference facts;
- `TOOL_DATA_MATERIALIZATION_MANIFEST.csv` — every generated dataset with bytes/rows;
- `features/FEATURE_INDEX.csv` — feature-level lookup surface;
- `features/FEATURE_METHOD_MAP.csv` — feature -> managed method/RID/RVA;
- `features/FEATURE_ASSET_MAP.csv` — feature -> visual template;
- `control/MAIN_STATIC_CONTROL_REFERENCES.csv` — exact helper/OCR/update surfaces referenced by the main managed donor;
- `control/CONTROL_STACK.csv` — high-level control primitive -> low-level helper/native chain;
- `control/KAUTOHELPER_API.csv` — all parsed helper methods;
- `control/KAUTOHELPER_CALL_GRAPH.csv` — exact IL call edges for clean KAutoHelper method bodies;
- `dotnet/TYPE_CATALOG.csv`, `METHOD_CATALOG_*.csv`, `FIELD_CATALOG.csv`, `MODEL_PROPERTIES.csv`;
- `assets/IMAGE_TEMPLATE_INDEX_*.csv`, `IMAGE_EXACT_DUPLICATES.csv`;
- `snapshot/ARTIFACT_MANIFEST_*.csv`, `SNAPSHOT_SUMMARY.json`.

Human/AI routing documents:

- `SUBSYSTEM_SOURCE_MAP.md`
- `SEMANTIC_JOIN_MAP.md`
- `AUTO_TOOL_API_CATALOG.md`
- `AUTO_TOOL_ACTION_CATALOG.md`.

## DATA-2222 pattern applied here

DATA-2222 separates broad evidence from compact lookup data. DATA-333 follows the same pattern:

```text
raw Debug snapshot
 -> reproducible parser/materializer
 -> full artifact/type/method/asset catalogs
 -> specialized tool-first feature/control indexes
 -> atomic FACTS
 -> route/join documents
 -> targeted runtime proof only for unresolved dynamic behavior
```

Do not scan the ZIP from zero for normal questions. Lookup the smallest specialized dataset first.

## Frozen snapshot summary

The current supplied Debug snapshot materializes:

- 1,450 files / 146,978,306 bytes;
- 2 EXE, 36 DLL, 3 PDB;
- 1,393 PNG templates, 1,180 byte-unique;
- 178 exact PNG duplicate groups / 213 redundant copies;
- main managed donor: 57 TypeDefs, 1,070 MethodDefs, 429 Fields;
- KAutoHelper: 40 TypeDefs, 224 MethodDefs;
- Debug PDB: 783 unique identifier-like symbols.

Exact values are generated in `snapshot/SNAPSHOT_SUMMARY.json`.

## Static authority boundary

Three evidence levels must not be mixed:

1. **Main managed metadata/PDB** proves type/method/property identity and RID/RVA, even when method bodies are protected.
2. **KAutoHelper clean IL** proves exact helper call chains and bundled capabilities.
3. **Main static MemberRefs** prove which external helper surfaces the managed donor references globally, but not the exact calling feature when those feature bodies remain protected.

Runtime/call-site tracing is still required for exact feature branch order, thresholds, coordinates and success/failure transitions.

## Critical control finding

The helper DLL bundles a complete `ADBHelper`, but the main managed donor has a static reference only to `ADBHelper.Delay`, not `Tap`, `Swipe`, `ScreenShoot` or `ConnectNox`.

By contrast, the main donor statically references:

- `AutoControl.SendClickOnPosition`;
- `SendTextKeyBoard`;
- `SendKeyBoardPress`;
- `SendDragAndDropOnPosition`;
- `FindWindowHandlesFromProcesses` / `GetText`;
- `CaptureHelper.CaptureWindow` / `CropImage`;
- `ImageScanOpenCV.FindOutPoint(s)`;
- Tesseract engine/process/text extraction.

Therefore the strongest static model is **HWND capture + visual recognition + Win32 input**, while ADB input/screenshot remains a bundled capability without current main static-reference proof.

## Sensitive data rule

Plaintext-looking account/key/code files are never copied into DATA-333. Only path, size, hash, line/schema metadata are stored under `snapshot/SENSITIVE_TEXT_SCHEMAS.csv` and `persistence/PERSISTENCE_LAYOUT.csv`.

## Regeneration

Generator:

`tools/materialize_auto_debug.py`

Workflow:

`.github/workflows/materialize-auto-debug.yml`

When the Debug snapshot changes, regenerate and compare. Do not hand-edit large generated CSV catalogs.
