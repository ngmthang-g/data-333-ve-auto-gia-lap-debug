# Auto Tool Action Catalog — DATA-333 donor

The donor is primarily an external UI automation system. These are its verified/available mutation primitives, not game-semantic actions.

| Action family | Primitive | Channel | Evidence status | Expected observable proof |
|---|---|---|---|---|
| Click | `SendClickOnPosition` | Win32/PostMessage | VERIFIED main static reference | recapture target UI state |
| Drag | `SendDragAndDropOnPosition` | Win32/PostMessage | VERIFIED main static reference | recapture moved/scrolled UI state |
| Text input | `SendTextKeyBoard` | Win32 keyboard messages | VERIFIED main static reference | OCR/template/field-state change |
| Key input | `SendKeyBoardPress` | Win32 keyboard messages | VERIFIED main static reference | target UI transition |
| ADB tap | `ADBHelper.Tap` | adb shell input | BUNDLED; no static main reference | device screenshot/UI transition |
| ADB swipe | `ADBHelper.Swipe` | adb shell input | BUNDLED; no static main reference | device screenshot/UI transition |
| ADB key/text | `ADBHelper.Key/InputText` | adb shell input | BUNDLED; no static main reference | device screenshot/UI transition |

Observation primitives are not actions but are coupled to every donor mutation:

```text
CaptureWindow
 -> optional CropImage
 -> FindOutPoint(s) / OCR
 -> decide
 -> one input mutation
 -> wait/re-observe
```

## Feature actions recovered by name

High-value protected donor routines include:

- Train: `trainLEVEL1`, `setupautotrain`, `batdanh`, `tatdanh`, `lenbaitrain`;
- sell/storage: `sellItemm`, `donrac`, `catdovaokho`, `laydotrongkho`, `checkfulltui`;
- party/follow: `TAO_PT_1NGUOI`, `THOAT_PT`, `THOAT_VAOLAI_PT`, `theodoi`, `botheodoi`;
- activities: `setupautothuylao`, `HD_ACTAC`, `danh_actac`, `dilamnvuTBD`;
- navigation: `truyenmap`, `Truyenvetochau`, `toinpc_*`, coordinate helpers;
- pet/mount: `xuatpet`, `lenngua`, `xuongngua`;
- recovery: `checktrilieutudong`, `batbuff`, medicine/mana routines;
- orchestration: `StartQuestDevice`, `StartAllSelectedDevice`.

Exact RID/RVA/body status are in `FEATURE_METHOD_MAP.csv` and `METHOD_CATALOG_*.csv`.

## Important limitation

Method identity does not prove its internal click sequence when the body is protected/non-standard. Do not invent coordinates, image thresholds or retry ordering from names alone. Runtime traces should add those as a separate dynamic dataset rather than overwriting static facts.
