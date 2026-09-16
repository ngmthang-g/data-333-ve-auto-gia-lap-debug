# DATA-333 — Auto feature/research readiness

Purpose: prevent repeated broad reverse engineering of the donor auto. This table separates facts already solved from facts that still need a narrow call-site/runtime proof.

Labels:

- **SOLVED STATIC** — sufficient static evidence exists in PDB/managed metadata/helper binaries/assets.
- **MATERIALIZED** — reproducible generator/index path exists.
- **PARTIAL / TARGETED PROOF** — architecture is known; one narrow runtime or call-edge fact remains.
- **DESIGN BRIDGE** — donor behavior is known, but production implementation should be mapped to DATA-2222 semantic state/action.
- **NO EVIDENCE** — do not claim this mechanism exists without new proof.

| Area | Readiness | Solved evidence | Remaining narrow gap |
|---|---|---|---|
| WPF application shell | **SOLVED STATIC** | `App`, `LogIn`, `MainWindow`, drag/drop utilities, UI event/timer symbols | exact UI layout only if needed |
| Login/license/update control plane | **SOLVED STATIC** | `Cons`, `Login`, `UserInfo`, `CheckKey`, updater handlers, HTTP/JSON dependencies | exact remote endpoints/protocol only if operationally required; never materialize secrets |
| Nox discovery | **SOLVED STATIC** | Nox `multi.ini`, PID/VM PID/port/title helpers | runtime proof on current Nox build if mapping fails |
| ADB control primitives | **SOLVED STATIC** | exact connect/tap/swipe/key/text/screenshot commands and helper methods | feature-by-feature caller mapping |
| Win32 control primitives | **SOLVED STATIC** | window/process discovery, SendMessage/PostMessage/SendInput/mouse/keyboard wrappers | feature-by-feature caller mapping and focus behavior |
| Per-device state model | **SOLVED STATIC** | `DeviceInfo`, accounts, quest threads, PID/handle/image/running state | exact synchronization/locking semantics |
| Multi-device orchestration | **PARTIAL / TARGETED PROOF** | `StartAllSelectedDevice`, `StartQuestDevice`, per-device threads/state | concurrent mutation arbitration and failure isolation |
| Screen acquisition | **SOLVED STATIC** | ADB screencap + Win32/GDI capture families | exact source selected by each feature |
| Template matching | **SOLVED STATIC** | OpenCV/EmguCV helper surface + 1,393 PNG assets + `FindImage*`/`FindAndClick*` wrappers | per-template thresholds/search regions/scale policy |
| OCR | **SOLVED STATIC** | Tesseract runtime/traineddata + text recognition helpers | exact call sites and preprocessing parameters |
| Captcha donor subsystem | **SOLVED STATIC / SAFETY BRIDGE** | captcha symbols/status/assets are present | production rebuild should pause for user handling; no bypass automation |
| Train donor behavior | **DESIGN BRIDGE** | train/setup/map/combat symbols and assets | recover policy ordering only where not already superseded by DATA-2222 semantics |
| Party/follow donor behavior | **DESIGN BRIDGE** | party create/join/follow/leave symbols/assets | map donor policy to semantic team actions |
| Sell/item filtering donor | **DESIGN BRIDGE** | sell routines + 435 item templates + trash/equipment assets | recover keep/sell policy; use live item semantics in rebuilt tool |
| Storage/item move donor | **DESIGN BRIDGE** | deposit/withdraw/move symbols and templates | recover policy; replace pixel slot mutations with semantic item actions |
| HP/mana/consumables donor | **DESIGN BRIDGE** | thresholds, counts, medicine-NPC routines/assets | recover threshold policy; prefer semantic HP/bag state |
| Pet/horse donor | **DESIGN BRIDGE** | pet/food/horse routines/config/assets | exact donor policy only where useful |
| Thủy Lao | **PARTIAL / DESIGN BRIDGE** | dedicated methods, state flags and 59 assets | exact stage transition graph and semantic mapping |
| Ác Tặc/activity | **PARTIAL / DESIGN BRIDGE** | methods, coordinate persistence and state flags | exact state transition graph and semantic mapping |
| `TBD` flow | **PARTIAL** | `nhannvTBD`, `toinpcTBD`, `chayTBD`, counters and related assets | exact expansion/feature semantics and transition graph |
| Navigation/map transfer | **DESIGN BRIDGE** | coordinate/map/NPC transfer routines/assets | retain destinations/policy; prefer semantic navigation |
| Treatment/revive | **DESIGN BRIDGE** | treatment/Đầu thai methods/assets | map to current dynamic dialog/revive state proof |
| Trade | **PARTIAL / DESIGN BRIDGE** | trade UI assets and state/coordinate properties | exact donor sequencing; map to semantic trade session |
| Scheduler | **SOLVED STATIC** | timer/schedule properties and `TimerCheckHenGio_Tick` | exact operator policy only if required |
| Plaintext runtime persistence | **SOLVED STATIC** | `luufile/*` folders + file I/O symbols | migrate secrets to protected storage |
| MEmu support | **PARTIAL** | `(MEmu).txt` artifact exists | exact code path/caller not yet proven |
| WebView2 active use | **NO EVIDENCE** | DLLs are bundled | no MainWindow usage proven; may be residual dependency |
| Direct gameplay socket/protocol control | **NO EVIDENCE** | current gameplay evidence is UI/emulator automation | require concrete socket/protocol call evidence before claiming |
| Production EXE call graph | **PARTIAL / TARGETED PROOF** | PDB symbols + managed obfuscated donor + helper metadata | Themida blocks clean body recovery; use targeted runtime trace rather than broad unpacking |
| Safe data regeneration | **MATERIALIZED** | `tools/materialize_auto_debug.py` + GitHub workflow | source Debug snapshot must be present in repo/workflow input |

## Highest-value next proofs

1. Trace one harmless donor action end-to-end: detector -> caller -> actuator -> coordinates -> visual proof.
2. Trace one concurrent two-device run to establish isolation, locking, cancellation and recovery behavior.
3. Recover per-template threshold/search-region configuration for the highest-value flows only.
4. Recover exact state transition graph for Thủy Lao and Ác Tặc rather than decompiling the whole program.
5. Confirm whether screenshot source and actuator are selected globally, per device, or per feature.

## Stop condition

Do not broad-reverse the protected executable merely because a method body is not visible. If PDB + helper metadata + assets already establish the donor intent and DATA-2222 has the semantic replacement, move directly to implementation/migration design.
