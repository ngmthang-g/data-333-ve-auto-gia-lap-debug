# 07 — Feature/state joins and protected-body strategy

## Purpose

DATA-333 must answer **where a feature lives and what evidence is already solved** before any new reverse work begins.

The main donor has 1,070 CLR MethodDefs, but most gameplay bodies are protected/non-standard. This does not mean the whole tool is opaque: class identity, method identity, RID/RVA, model state, external MemberRefs, PDB symbols, image assets and helper-library implementation remain materializable.

Canonical lookup surfaces:

- `database/features/CORE_METHOD_RVA_INDEX.csv`
- `database/dotnet/DEVICE_STATE_CATALOG.csv`
- `database/features/FEATURE_STATE_JOIN.csv`
- `database/features/ACTIVITY_EVIDENCE_MATRIX.csv`
- `database/control/CONTROL_CALL_CHAINS.csv`

## Main-donor body split

Frozen managed donor `Auto_ThanLong_obfusca.exe` contains:

- 1,070 MethodDefs;
- approximately 802 protected/non-standard bodies;
- approximately 259 methods with valid CLR IL headers;
- the remainder P/Invoke/abstract/no-body cases.

Therefore the correct strategy is not broad unpacking. Split work into two queues.

### Queue A — valid-IL donor methods

Read/decompile these first because they can reveal orchestration and smaller state transitions without runtime instrumentation.

High-value examples include:

- `nhaptkmk`
- `checkthanhvien`
- `toivitri_actac`
- `THOAT_VAOLAI_PT`
- `botheodoi`
- `tatdanh`
- `donrac`
- `laydotrongkho`
- `nhanitem`
- `Truyenvetochau`
- `toinpc_pet_daily`
- `check_dinhviphu`
- `lenngua`
- `dungphuvetochau`
- `getsonhieuchotrenscreen`
- `FindImage_OK`
- `FindImage_OutPoint`
- `FindAndClick_Color_TBDTim`
- `FindImage_Color_TBDTim`
- `FindAndClick_Until_Found`
- `StartAllSelectedDevice`
- `GetAcc`.

Exact RID/RVA/body status is in `CORE_METHOD_RVA_INDEX.csv`.

### Queue B — protected/non-standard feature bodies

Do not broad-unpack them just because their method body is hidden. First combine:

```text
method identity/RVA
 + DeviceInfo/QuestInfo/AccountInfo state
 + feature image templates
 + static external MemberRefs
 + exact KAutoHelper implementation chain
```

Only then runtime-trace the missing branch/order/threshold/call-site.

Examples:

- `trainLEVEL1`
- `setupautotrain`
- `sellItemm`
- `catdovaokho`
- `setupautothuylao`
- `HD_ACTAC`
- `StartQuestDevice`
- `SoveNormalCapt`.

## State is per device, not global UI decoration

`DeviceInfo` contains feature-specific mutable state alongside its window and worker identity. Important fields include:

```text
ImageScreen
QuestThread / CheckQuestThread / IsRuningQuest
DeviceHandle / DeviceID / DeviceName
TRANGTHAI_TRAIN
TRANGTHAI_THUYLAO
TRANGTHAITIMACTAC
TRANGTHAI_ACTAC
TRANGTHAI_CHINHTUYEN
slCAPTCHA
sldisgame
tenmaptrain
toado_actac / toadoX / toadoY / toadoclickX
account/server fields
```

This strongly supports a per-emulator state-machine model. `QuestInfo` separately carries the assigned quest/work item, device binding, run status and scheduling state.

## Feature joins

`FEATURE_STATE_JOIN.csv` ties together:

```text
feature
 -> state properties
 -> behavior method names
 -> method-row count
 -> image-row count
 -> evidence boundary
```

This prevents a common error: treating every property/method containing a loose substring as belonging to a feature.

### Classifier correction

The first materializer version used overly broad substring rules. That produced false joins such as:

- `mana` matching `Manager`;
- `pt` matching `Opacity`;
- `quest` matching `Request`.

The corrected materializer uses stricter token/camel-case/boundary matching and scopes feature methods to the donor tool namespace. The cleaned `FEATURE_INDEX.csv` is authoritative for this snapshot.

## Thủy Lao

Static evidence establishes a much richer state surface than a single `setupautothuylao` method:

- state: `TRANGTHAI_THUYLAO`, `thuylao`, `sttbaithuylao`;
- methods: `vaothuylao`, `hdthuylao`, `toinpcthuylao`, `setupautothuylao`;
- image families include `sttthuylao1..12` and corresponding Thủy Lao position/stage templates, plus entry/end detectors.

**Strong inference:** the donor encodes at least a 12-stage visual state progression. The exact branch graph and transition actions are not statically proven because the controlling bodies are protected.

Do not re-scan all assets to rediscover the 12-stage shape; runtime work should target one stage transition at a time.

## Ác Tặc

State/method evidence:

```text
TRANGTHAITIMACTAC
TRANGTHAI_ACTAC
toado_actac
HDACTAC
MAPACTAC

danh_actac
gettoado_actac
toivitri_actac
HD_ACTAC
```

Assets include multiple position templates and combat/end markers. This supports a coordinate-driven activity state machine with discovery/navigation/combat/completion phases. Exact ordering remains runtime proof.

## TBD flow

Evidence groups into an accept/locate/execute/turn-in family:

```text
toinpcTBD
nhannvTBD
tranvTBD
huynvTBD
dilamnvuTBD
laylenhbai
checklenhbai
check_dinhviphu
```

Together with `tbd`, `tentbd`, `lenhbai`, `dinhviphu`, boss/end templates, this is stronger than merely knowing the method names. The exact meaning of the acronym and server-side objective semantics still require contextual/runtime proof.

## Observation/action bridge

The helper-library implementation is clean enough to close the low-level mechanism:

```text
CaptureWindow -> GDI BitBlt image
FindOutPoint(s) -> MatchTemplate -> Point(s)
SendClickOnPosition -> MakeLParamFromXY -> PostMessage
```

Main-donor static references point to these Win32/vision APIs. ADB remains an implemented helper capability, but the managed main donor only statically references `ADBHelper.Delay` from that family.

Therefore feature research should begin from Win32/GDI/vision unless runtime evidence demonstrates an ADB branch.

## Runtime proof queue

Highest-value unresolved facts are narrow:

1. one Train loop: detector/state -> protected method -> HWND action -> resulting visual state;
2. one Thủy Lao stage transition, including `sttbaithuylao` before/after;
3. one Ác Tặc discovery/navigation transition, including coordinate source;
4. one Sell sequence, including how image/template identity is converted into the clicked bag slot;
5. one two-device concurrent run, to prove cancellation/locking/isolation behavior.

Each trace should record exact method RVA, DeviceID/HWND, detector/template, coordinate transform, actuator and post-state. No broad executable unpacking is needed unless one of these traces cannot be resolved by the existing catalogs.