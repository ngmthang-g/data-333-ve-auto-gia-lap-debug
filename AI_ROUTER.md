# AI Router — DATA-333

Read `AI_BOOTSTRAP.md` first.

## Route by question

| Question | Start here |
|---|---|
| Overall architecture / execution loop | `analysis/01_TOOL_ARCHITECTURE.md` |
| Device/emulator connection | `analysis/02_DEVICE_CONNECTION_AND_CONTROL.md` |
| Image matching / OCR / screen observation | `analysis/03_VISION_OCR_PIPELINE.md` |
| Auto features and state/config flags | `analysis/04_FEATURE_STATE_MAP.md` |
| Class/type/method inventory | `database/TOOL_CLASS_CATALOG.md` |
| Exact ADB/Win32 helper primitives | `database/CONTROL_PRIMITIVES.md` |
| Relationship to DATA-2222 | `analysis/05_DATA222_BRIDGE.md` |
| Plaintext config/credential exposure | `SECURITY_REDACTION.md` |

## Research rule

Use the smallest evidence surface that answers the task:

```text
PDB symbol / managed metadata / helper DLL API / exact asset
 -> identify component
 -> identify state and caller intent
 -> identify control primitive
 -> identify expected visual/state proof
 -> identify failure/recovery path
```

The production executable is Themida-protected. Avoid broad unpacking unless an exact missing fact cannot be answered from PDB, the managed obfuscated build, helper DLLs, assets, or a targeted runtime trace.

## Tool-vs-client rule

If the question is **what the donor tool currently does**, stay in DATA-333.

If the question is **how to rebuild the behavior reliably using client semantics**, route to DATA-2222 after identifying the donor intent in DATA-333.

## Priority evidence

1. supplied PDB source symbols;
2. KAutoHelper managed metadata and command literals;
3. alternate managed obfuscated executable;
4. Debug image/config assets;
5. protected production executable strings/PE layout;
6. inference.

## Hard cautions

- Bundled DLL does not prove a code path is actively used. WebView2 is present in the folder, but current static evidence does not prove that MainWindow uses it.
- Both ADB and Win32 input/capture capabilities exist. Exact feature-by-feature channel selection still needs call-site/runtime proof.
- No current static evidence shows direct gameplay protocol/socket control by this external tool. Network-related symbols strongly support login/license/update HTTP traffic; gameplay control evidence points to emulator/window/UI automation.
- A matching image is observation, not state proof. Rebuilt logic should verify the resulting state before the next mutation.
