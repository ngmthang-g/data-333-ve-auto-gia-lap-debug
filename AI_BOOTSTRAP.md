# AI Bootstrap — DATA-333 Auto Debug knowledge/data base

## Purpose

DATA-333 is the canonical, reproducible data/knowledge base for the supplied **external Windows Auto Thần Long donor tool**. It is intentionally modeled after DATA-2222's lookup-first/materialization approach.

DATA-333 answers:

- what binaries/assets/state models/features exist in the donor;
- which class/method/property/RID/RVA corresponds to a feature;
- how emulator/process/window identity is resolved;
- which observation/input helper surfaces are actually referenced by the main donor;
- what exact low-level chains KAutoHelper implements;
- which visual templates are associated with each feature;
- what is proven static evidence versus an unresolved protected/runtime call-site.

DATA-2222 remains the canonical source for **game client semantic state/actions**. DATA-333 is the canonical source for **donor tool behavior/policy/control evidence**.

## Mandatory lookup order

For normal work:

```text
AI_BOOTSTRAP
 -> AI_ROUTER
 -> database/TOOL_DATA_INDEX
 -> one specialized generated dataset
 -> database/SUBSYSTEM_SOURCE_MAP or SEMANTIC_JOIN_MAP
 -> one analysis document only if interpretation is needed
 -> targeted runtime proof only for unresolved protected behavior
```

Do not re-scan the ZIP, PDB, all PNGs or all MemberRefs for a normal lookup.

## Frozen snapshot

Generated authority: `database/snapshot/SNAPSHOT_SUMMARY.json` and `database/snapshot/ARTIFACT_MANIFEST_*.csv`.

Current materialized snapshot contains 1,450 files / 146,978,306 bytes, including 1,393 PNG templates, 2 EXE, 36 DLL and 3 PDB files.

Main donor metadata:

- `Auto_ThanLong_obfusca.exe`: 57 TypeDefs, 1,070 MethodDefs, 429 Fields;
- `KAutoHelper.dll`: 40 TypeDefs, 224 MethodDefs;
- Debug PDB: 783 unique identifier-like symbols.

Use hashes in the artifact/binary manifests before applying these facts to a different donor build.

## Evidence/status vocabulary

- **VERIFIED** — directly materialized from binary metadata, clean IL, PDB, file/image asset or exact static reference.
- **VERIFIED_STATIC_NONREFERENCE** — an exact static absence in the checked surface; it does not rule out reflection/dynamic/runtime use.
- **VERIFIED_BUNDLED_NOT_MAIN_REFERENCED** — helper capability exists but main static MemberRefs do not reference it.
- **PARTIAL / TARGETED_RUNTIME_PROOF** — components/identity are solved; exact protected call-site/order/threshold/result still needs runtime evidence.
- **PROBABLE** — strong multi-source inference, not direct proof.
- **HYPOTHESIS** — research direction only.

Never silently upgrade capability into active-path evidence.

## Corrected canonical donor architecture

The strongest current static model is:

```text
WPF operator/login/license/update shell
 -> Nox/process/port/window identity discovery
 -> DeviceInfo / AccountInfo / QuestInfo per-device state
 -> per-device QuestThread + CheckQuestThread + timers
 -> CaptureWindow / crop
 -> OpenCV template matching and/or Tesseract OCR
 -> protected donor feature/policy routine
 -> Win32 window click/key/text/drag
 -> delay/re-capture/re-detect/recover
```

KAutoHelper also bundles a full ADB input/screenshot layer, but the main managed donor statically references only `ADBHelper.Delay`, not `Tap`, `Swipe`, `ScreenShoot` or `ConnectNox`. Therefore do **not** describe ADB gameplay input as the active donor path without new runtime/reflection proof.

## Key generated routes

- all files/hashes: `database/snapshot/`
- PE/protection/sections: `database/binary/`
- CLR classes/methods/fields/properties/PDB: `database/dotnet/`
- control/helper APIs/call graph/strings/threading: `database/control/`
- visual assets/deduplication: `database/assets/`
- feature joins: `database/features/`
- file-backed persistence: `database/persistence/`
- atomic facts: `database/FACTS.jsonl`
- exact generated inventory: `database/TOOL_DATA_MATERIALIZATION_MANIFEST.csv`.

## Static/runtime boundary

Main type/method/property metadata and PDB symbols can prove **identity**. KAutoHelper clean IL can prove **helper implementation chains**. Main static MemberRefs can prove **referenced external surfaces**.

They cannot, by themselves, prove exact protected feature branch order, template threshold, ROI, coordinates, retry count or success state. Store those later as separate runtime trace data instead of guessing.

## DATA-2222 bridge

Use DATA-333 to recover donor intent/policy, then prefer DATA-2222 semantic state/action where already solved. Do not mechanically rebuild `find image -> click -> sleep` when a semantic state/action exists.

## Sensitive material

Credential/key/code-looking plaintext values in the Debug bundle are intentionally excluded. Only schema/path/size/hash metadata may be materialized.

## Captcha

Captcha donor symbols/assets may be indexed as architectural evidence. Production automation should use a pause/manual-handling state rather than automatic bypass.
