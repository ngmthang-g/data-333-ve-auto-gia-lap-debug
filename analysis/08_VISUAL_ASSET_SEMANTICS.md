# 08 — Visual asset semantics: what the PNG corpus is actually doing

## Core conclusion

The 1,393 PNG files are not one homogeneous template set. They implement several distinct perception roles:

```text
navigation/action labels
state/guard text
number/coordinate recognition
actor/item visual identity
minimap/terrain location cues
confirmation/error/completion proof
```

Treating every PNG as a generic `FindImage -> click` template loses donor behavior.

Machine-readable entrypoint: `database/assets/ASSET_ROLE_CATALOG.csv`.

## Thủy Lao is a visual state machine

The supplied Thủy Lao sheet contains two especially important numbered families.

### Stage state

`sttthuylao1..12` provides twelve discrete stage/status markers.

### Position state

`thuylaovitri1..12` visibly encode coordinate text such as:

```text
(106,148)
(143,148)
(150,120)
(150,85)
(150,50)
(120,42)
(85,42)
(49,42)
(41,71)
(41,107)
(41,141)
(71,148)
```

This is strong evidence that the donor does not merely click through a fixed sequence. It can recognize a current stage/position from screen pixels and choose the next action relative to that state.

The same sheet contains lifecycle guards such as entry (`Xin vào`), exit (`[Lối ra]`), completion/limit text and revive (`Đầu thai`). These form a feature-level state-machine vocabulary.

## Ác Tặc uses location-image cues

`vitriactac1..7` are small terrain/minimap-like crops rather than text labels. Combined with:

- `gettoado_actac`;
- `toivitri_actac`;
- `danh_actac`;
- `TRANGTHAITIMACTAC`;
- `TRANGTHAI_ACTAC`;
- `toado_actac`;

this supports a phase split:

```text
search/current-location recognition
 -> coordinate/location selection
 -> movement
 -> challenge/combat
 -> completion/end proof
```

Exact transition order remains protected/runtime evidence.

## Negative-state templates matter

The Hoạt Động corpus contains multiple fragments equivalent to:

- no suitable target;
- no target around;
- cannot reach/location unavailable;
- already in a party;
- daily limit reached;
- no mission;
- mission completed.

These are not decorative assets. They are likely **failure/guard detectors** and explain how a visual auto can recover instead of blindly clicking.

For a rebuild, preserve their semantic intent:

```text
negative observation
 -> classify failure reason
 -> retry / reroute / stop / switch activity
```

rather than copying the exact text crop when DATA-2222 exposes stronger semantic state.

## Generic confirmations are ambiguous

Assets such as `Đồng ý`, `Xác nhận`, plus/cross buttons and common `Tổ đội` labels occur across multiple flows. A generic template match is therefore not enough to infer feature identity.

Correct interpretation requires surrounding state:

```text
current feature
 + active detector set
 + expected dialog/window
 + matched generic button
 -> action
```

This is one reason the database separates feature/state joins from raw asset catalogs.

## Item assets encode policy

The dominant image domains are not navigation UI:

- `ItemSell_TrangVatPham` — 435 templates;
- `itemrac` — 91 templates;
- `Item_vaokho` — 19 templates;
- additional equipment/gem/item groups.

Their volume strongly indicates an embedded visual **item policy database**: recognize an icon/category, then sell/drop/store/keep accordingly.

For migration to DATA-2222, this is valuable policy evidence even when the future implementation should replace icon classification with live item/template identity.

## Coordinates and numeric OCR/templates

The corpus includes numeric labels, visible coordinates and quantity/value fragments. The donor also statically references Tesseract. Therefore the perception model is hybrid:

```text
small exact templates for highly stable labels/icons
 + template/color matching for state fragments
 + OCR for variable text/numbers where required
```

Do not assume Tesseract handles all text or that all digits are OCR-driven; explicit numeric image templates exist.

## Semantic migration rule

For each visual asset family classify it as one of:

1. **policy identity** — preserve rule, replace detector if semantic state exists;
2. **runtime guard/proof** — prefer DATA-2222 state when available, keep visual fallback;
3. **pre-game/emulator UI** — visual/Win32 automation remains appropriate;
4. **generic confirmation** — require feature/dialog context before clicking;
5. **location/coordinate cue** — normalize coordinate spaces and verify post-state.

The target architecture is not `template -> click -> sleep`. It is:

```text
feature state
 -> detector/state source
 -> guard
 -> one action
 -> fresh proof
 -> retry/recovery/next state
```
