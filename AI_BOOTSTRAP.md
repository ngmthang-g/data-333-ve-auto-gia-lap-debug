# AI Bootstrap — DATA-333 auto debug/tool

## Purpose

DATA-333 is the canonical knowledge base for the **external Windows automation tool** shipped in the Debug bundle. It complements DATA-2222, which is the canonical knowledge base for client/runtime/static game semantics.

The primary question in this repository is:

> How does the existing auto tool discover emulator instances, observe screen state, decide feature state, issue input, persist configuration, and coordinate multiple devices/accounts?

## Evidence levels

- **VERIFIED-PDB** — name/path/symbol observed in the supplied debug PDB.
- **VERIFIED-METADATA** — type/method observed in managed assembly metadata.
- **VERIFIED-BINARY-STRING** — literal/API/command observed in executable/DLL strings.
- **VERIFIED-ASSET** — directly observed file/image/config in the supplied Debug bundle.
- **PROBABLE** — strong architectural inference from several verified facts, but exact caller/call order is not yet recovered.
- **HYPOTHESIS** — research direction only.

Never promote PROBABLE/HYPOTHESIS to VERIFIED without new evidence.

## Frozen source snapshot

Key SHA-256 fingerprints:

- `Auto_ThanLong_Kteam_0789998118.exe` — `e1e4f555da3d4891ab0db674ee345bad67c2414632b7d1684151e7a9243134aa`
- `Auto_ThanLong_obfusca.exe` — `e2ba163c86852e81e60fe6c4694e031a2a7bf1b8838ddef799135736ad764e11`
- `Auto_ThanLong_Kteam_0789998118.pdb` — `5795d8e41d2504d732919dfd74d135a364ec6fc7cbbc47cdfd71021b2780ad84`
- `KAutoHelper.dll` — `55fb7f522ab98227c0c6e00009c8090bc99e6a84ebe1d79427d930fd7900ae05`

The protected executable contains a `.themida`/`.boot` layout. The alternate `Auto_ThanLong_obfusca.exe` is a managed .NET assembly with obfuscated metadata. The PDB preserves many original source-level names and is therefore the highest-value static evidence for the auto layer.

## Read order

For normal work:

1. `AI_BOOTSTRAP.md`
2. `AI_ROUTER.md`
3. `analysis/01_TOOL_ARCHITECTURE.md`
4. exactly one feature/connection document relevant to the task
5. targeted database/catalog records only

Do not re-scan all 1,393 image templates for every task.

## Canonical tool-side architecture

Current best-supported architecture:

```text
Login / license / updater
 -> emulator/process discovery
 -> Nox/ADB-port/window mapping
 -> DeviceInfo + AccountInfo + QuestInfo state
 -> per-device start/orchestration
 -> screen acquisition
 -> image/color/OCR observation
 -> feature state machine / guard
 -> ADB or Win32 input primitive
 -> screen/state re-observation
 -> continue / recover / switch feature
```

The exact call edge between every box is not fully reconstructed because the production executable is Themida-protected and the alternate assembly is obfuscated. The components and many source method names are directly evidenced.

## Critical architectural distinction

DATA-333 describes the **existing UI-driven donor tool**. DATA-2222 describes **semantic client/runtime actions and state**.

Do not assume the most reliable future implementation should reproduce every image click. When DATA-2222 already has a semantic state/action contract, treat DATA-333 as behavior/policy evidence and prefer the semantic client route for a rebuilt tool.

## Sensitive material rule

The Debug bundle contains plaintext files that look like account/license/key material. Repository documents may record:

- file path;
- field count/schema;
- byte/line count;
- cryptographic fingerprint;

but must **not** copy raw credentials, access tokens, passwords, activation keys, or license codes.

## Captcha rule

Captcha-related classes/properties/assets exist in the donor tool. DATA-333 may document that architecture and its state transitions, but rebuilt production automation should pause for user handling rather than attempt automated bypass.
