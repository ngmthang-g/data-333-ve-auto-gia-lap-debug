# DATA-333 — feature/data readiness

Purpose: track what is already materialized and prevent repeated broad reverse engineering.

| Area | Readiness | Materialized evidence | Remaining gap |
|---|---|---|---|
| Full snapshot identity | **SOLVED / MATERIALIZED** | 1,450-file SHA/path manifests + binary hashes | regenerate only when donor snapshot changes |
| CLR type/method/field inventory | **SOLVED / MATERIALIZED** | 57 main TypeDefs / 1,070 methods / 429 fields; helper 40/224 | signature decoding can be expanded only if needed |
| Original/debug symbol recovery | **SOLVED / MATERIALIZED** | 783 PDB identifier-like symbols | local-variable/line-level PDB parsing only if a concrete gap requires it |
| Main method identity/RVA | **SOLVED / MATERIALIZED** | method chunks + body status | protected body internals remain targeted-runtime work |
| KAutoHelper implementation | **SOLVED / MATERIALIZED** | API catalog + clean IL call graph | none for current helper snapshot |
| Main external control references | **SOLVED / MATERIALIZED** | exact KAutoHelper/Tesseract/update MemberRefs | exact protected caller per feature remains runtime/body proof |
| Win32 click/key/text/drag | **SOLVED STATIC** | main static refs + exact helper chains | feature call-site/coordinates/transform |
| Window capture | **SOLVED STATIC** | main `CaptureWindow` ref + user32/GDI32 BitBlt helper chain | cadence/ROI per feature |
| OpenCV matching | **SOLVED STATIC** | main FindOutPoint(s) refs + helper MatchTemplate chain | threshold/ROI/template selected per protected routine |
| OCR | **SOLVED STATIC** | Tesseract constructor/config/process/GetText refs | preprocessing/ROI per protected routine |
| ADB helper capability | **SOLVED STATIC CAPABILITY** | exact tap/swipe/key/text/screencap/connect commands/methods | no need to re-reverse helper |
| ADB gameplay use by main | **NOT PROVEN / STATIC NONREFERENCE** | main statically refs `ADBHelper.Delay` only | runtime/reflection proof required before claiming Tap/Swipe/ScreenShoot/ConnectNox use |
| Nox PID/vmPID/port/title mapping | **SOLVED STATIC MECHANISM** | NoxMultiIni + netstat + Port + Process title chain | current-runtime mapping test only if integration fails |
| DeviceInfo per-emulator state | **SOLVED / MATERIALIZED** | properties for device handle/id/name, threads, accounts, coordinates, feature flags | exact synchronization ownership |
| Multi-device threading | **PARTIAL / TARGETED RUNTIME** | QuestThread/CheckQuestThread + Start/Sleep/Abort/Suspend/Resume/Dispatcher/timers | race/isolation/cancellation behavior |
| Image database | **SOLVED / MATERIALIZED** | 1,393 PNG, 1,180 unique, feature map, exact duplicate groups | visual semantic labeling can be enriched incrementally |
| Train/combat donor | **MATERIALIZED IDENTITY / PARTIAL FLOW** | methods/properties/assets indexed | exact branch/threshold/action order |
| Party/follow donor | **MATERIALIZED IDENTITY / PARTIAL FLOW** | methods/properties/assets indexed | exact retry/leader/follow flow |
| Sell/inventory donor | **MATERIALIZED IDENTITY / PARTIAL FLOW** | methods + tagged image rows/policy properties | exact keep/sell branch order; bridge to DATA-2222 semantic items |
| Storage donor | **MATERIALIZED IDENTITY / PARTIAL FLOW** | deposit/withdraw methods/settings/assets | exact slot/action sequence; bridge to semantic move |
| HP/mana/heal/buff | **MATERIALIZED IDENTITY / PARTIAL FLOW** | settings/methods/assets + OCR/vision surface | exact thresholds and action order |
| Navigation/NPC/map | **MATERIALIZED IDENTITY / PARTIAL FLOW** | transfer/NPC/coordinate methods/assets | exact destination state transitions |
| Thủy Lao | **MATERIALIZED IDENTITY / TARGETED RUNTIME** | methods/status fields/assets | exact stage transition graph |
| Ác Tặc | **MATERIALIZED IDENTITY / TARGETED RUNTIME** | methods/coordinate/status/assets | exact activity loop/state graph |
| TBD flow | **MATERIALIZED IDENTITY / TARGETED RUNTIME** | methods/counters/assets | exact domain meaning and transition graph |
| Pet/mount | **MATERIALIZED IDENTITY / PARTIAL FLOW** | methods/settings/assets | exact policy sequencing |
| Trade/transfer | **MATERIALIZED IDENTITY / TARGETED RUNTIME** | methods/coordinates/state/assets | confirmation/session order |
| Quest/level/account rotation | **MATERIALIZED IDENTITY / TARGETED RUNTIME** | QuestInfo/AccountInfo + methods/assets | full protected state machine |
| Scheduler | **SOLVED STATIC SURFACE** | timers/settings/checktime/Hẹn giờ refs | operator-specific policy if needed |
| File persistence | **SOLVED STATIC / MATERIALIZED** | layout + File/Directory refs | exact method owner for each write only if needed |
| Sensitive plaintext | **SOLVED SAFETY BOUNDARY** | schema/hash only | values intentionally excluded |
| Login/license/update HTTP | **SOLVED STATIC SURFACE** | HTTP/JSON/update refs + auth models | exact remote behavior only if explicitly needed |
| Direct gameplay socket/protocol | **NO EVIDENCE** | none in current donor data | concrete socket/protocol call proof required |
| WebView2 active main use | **NO EVIDENCE** | bundled dependency only | exact main ref/call required |
| Reproducible generation | **SOLVED / MATERIALIZED** | `tools/materialize_auto_debug.py` + workflow + manifest | source snapshot must be available to workflow |

## Highest-value next runtime datasets

Future proof should be recorded as structured rows, not prose-only notes:

```text
RUN_ID, DeviceID, PID, HWND, Feature, StateBefore,
Detector, Template/OCR, Threshold/ROI,
ActionHelper, InputCoordinates,
StateAfter, Result, ElapsedMs, FailureReason
```

Priority traces: one harmless click, one full capture/detect/action cycle, two-emulator isolation, then exact Train/Sell/Thủy Lao/Ác Tặc state transitions.
