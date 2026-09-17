# DATA-333 runtime proof queue

Purpose: track only facts that remain dynamic/protected after database lookup. Do not broad-reverse the donor before checking this queue.

## Evidence rule

`valid_il_header` means a CLR-style method header is recoverable. It does **not** by itself guarantee the instruction stream is semantically clean; obfuscation or an incomplete decoder can still produce invalid-looking call tokens. Only publish a main-donor call edge as VERIFIED when the target token/signature resolves coherently or runtime evidence confirms it.

KAutoHelper decoded call chains are substantially cleaner and are canonical in `database/control/CONTROL_CALL_CHAINS.csv` / `KAUTOHELPER_CALL_GRAPH.csv`.

## P0 — highest-value proofs

### RP-001 — one harmless UI action end-to-end

Record:

```text
DeviceID
PID / HWND
feature method + RVA
action trigger
automation screenshot/crop source
detector/template/OCR result
actuator API
input coordinates before/after transform
fresh capture/result state
```

Goal: close static-reference -> actual runtime-call gap for Win32 control.

### RP-002 — Train loop

Start from:

- `trainLEVEL1` RVA in `CORE_METHOD_RVA_INDEX.csv`;
- `TRANGTHAI_TRAIN`, `tenmaptrain` in `DEVICE_STATE_CATALOG.csv`;
- Train assets in `FEATURE_ASSET_MAP.csv`;
- Win32/vision static refs.

Prove one iteration:

```text
observed train state
 -> branch/guard
 -> click/keyboard/drag or other action
 -> updated state/template
```

Do not infer combat semantics only from the method name.

### RP-003 — Thủy Lao stage transition

Static evidence already supports a 12-stage visual progression (`sttthuylao1..12` and matching position/stage assets).

Prove one transition with:

```text
sttbaithuylao=N
 + matched stage template
 -> exact method/action
 -> sttbaithuylao=N+1 or explicit alternate state
```

Then repeat only for transitions that differ materially.

### RP-004 — Ác Tặc locate -> navigate -> fight

Track:

- `TRANGTHAITIMACTAC` / `TRANGTHAI_ACTAC`;
- `toado_actac`;
- `gettoado_actac`, `toivitri_actac`, `danh_actac`, `HD_ACTAC`;
- matched position/combat/end templates.

Prove where coordinates originate and which coordinate space they use.

### RP-005 — Sell sequence

Track one item from visual classification to mutation:

```text
bag screenshot/crop
 -> item template/category decision
 -> slot/coordinate resolution
 -> NPC/shop readiness
 -> click sequence
 -> item disappears / bag state changes
```

This is needed to recover donor **policy**; production rebuilding may replace the clicks with DATA-2222 semantic item/sell APIs.

## P1 — orchestration/isolation

### RP-006 — two-device concurrent run

Run two harmless workers and capture:

- each DeviceInfo/DeviceHandle;
- QuestThread/CheckQuestThread identities;
- cancellation/stop behavior;
- whether captures/actions ever cross HWND/device state;
- behavior of legacy `Abort/Suspend/Resume` paths.

Goal: determine actual isolation/arbitration model.

### RP-007 — screenshot source selection

Current strongest static main evidence points to `CaptureHelper.CaptureWindow`; ADB screenshot exists only as helper capability.

Prove whether screenshot source is selected:

- globally;
- per emulator/device;
- per feature;
- or never via ADB in the donor loop.

### RP-008 — ADB gameplay use/non-use

Do not attempt to prove this by DLL presence. Runtime proof requires an actual entry into `ADBHelper.Tap/Swipe/ScreenShoot/ConnectNox` or equivalent indirect path while a gameplay feature runs.

If no call appears during representative runs, record negative runtime evidence without converting it into a universal claim.

## P2 — feature-specific policy recovery

- party create/join/leave/follow ordering;
- HP/mana thresholds and retry policy;
- pet food/mount policy;
- storage deposit/withdraw policy;
- TBD mission state graph;
- account reconnect/rotation limits;
- schedule/hẹn giờ arbitration.

Recover these only when they materially improve the rebuild.

## Stop rule

For each proof, stop once DATA-333 can express:

```text
state source
 -> guard
 -> one action
 -> expected proof
 -> timeout/failure/recovery
```

If DATA-2222 already supplies a stronger semantic action/state surface, preserve donor policy and do not spend time reconstructing every pixel click.