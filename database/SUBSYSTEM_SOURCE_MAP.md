# Subsystem Source Map — DATA-333 donor

Purpose: route an Auto Debug question to the smallest useful evidence layer.

| Subsystem / question | First lookup | Second lookup | Deep/static proof | Remaining dynamic proof |
|---|---|---|---|---|
| Device list / multi-emulator identity | `MODEL_PROPERTIES.csv` (`DeviceInfo`, `NoxMultiIni`) | `MAIN_STATIC_CONTROL_REFERENCES.csv` | `CONTROL_STACK.csv` `NOX-IDENTITY`, KAutoHelper call graph | exact main call-site/order per launch |
| Window handle discovery | `MAIN_STATIC_CONTROL_REFERENCES.csv` | `KAUTOHELPER_API.csv` AutoControl | helper call graph / Win32 imports | exact child HWND selected per emulator version |
| Screen observation | `CONTROL_STACK.csv` `CAPTURE-WINDOW` | `KAUTOHELPER_CALL_GRAPH.csv` | GDI/user32 chain | actual capture cadence/ROI per feature |
| Template matching | `FEATURE_ASSET_MAP.csv` | `CONTROL_STACK.csv` VISION rows | KAutoHelper `FindOutPoint(s)` call graph | per-call threshold and selected template |
| OCR | `MAIN_STATIC_CONTROL_REFERENCES.csv` Tesseract rows | image assets / PDB identifiers | Tesseract external refs | ROI/preprocessing/variables per feature |
| Click / key / drag | `CONTROL_PRIMITIVES.csv` | `CONTROL_STACK.csv` | `KAUTOHELPER_CALL_GRAPH.csv` | exact protected caller and coordinate transform |
| ADB capability | `HELPER_STRING_INDICATORS.csv` | `KAUTOHELPER_API.csv` ADBHelper | ADB helper IL | main usage not proven beyond `Delay` |
| Train/combat | `FEATURE_INDEX.csv` | `FEATURE_METHOD_MAP.csv` `train_combat` | PDB + method metadata + image map | exact protected state transitions/callers |
| Party/follow | feature method + asset maps | DeviceInfo/MainWindow properties | Win32/vision stack | exact invitation/follow retry policy |
| Sell/inventory | feature method + asset maps | MainWindow policy properties | vision/click stack | exact item-template decision sequence |
| Storage | feature method + asset maps | persistence/settings | vision/click/drag stack | exact slot coordinates and post-state checks |
| HP/mana/treatment | `heal_buff` maps | OCR/image assets | Tesseract/vision refs | thresholds/branch order per routine |
| Travel/NPC | `travel_navigation` maps | coordinate properties | click/drag/vision stack | exact map/NPC state machine |
| Thủy Lao | `activity_thuylao` maps | `sttbaithuylao` / DeviceInfo state | visual/control stack | exact stage transition graph |
| Ác Tặc | `activity_actac` maps | `toado_actac`, `MAPACTAC`, status properties | visual/control stack | exact schedule/route/target loop |
| TBD | `activity_tbd` maps | `MaxTBD` and state props | visual/control stack | semantic meaning of all TBD states still requires runtime/protected-body proof |
| Quest/level | `quest_level` maps | QuestInfo/AccountInfo | threading + vision stack | exact task progression state machine |
| Pet/mount | `pet_mount` maps | related settings | image/control stack | exact companion policy |
| Trade/transfer | `trade_transfer` maps | trade coordinate/state properties | image/control stack | confirmation/session sequencing |
| Captcha | `captcha` method/asset maps | Tesseract refs | PDB + OCR | treat as pause/manual in rebuilt production flow |
| Login/license/update | `HTTP_AUTH_UPDATE_REFERENCES.csv` | auth_update feature methods/models | external refs | endpoint response behavior if required |
| File persistence | `PERSISTENCE_LAYOUT.csv` | `FILE_IO_REFERENCES.csv` | hashes/schema | exact write ownership per protected routine |
| Per-device concurrency | `THREADING_REFERENCES.csv` | DeviceInfo thread properties | method/PDB metadata | synchronization/race behavior requires runtime proof |

## Source authority

Use direct evidence in this order for donor behavior:

```text
clean KAutoHelper IL / exact main metadata reference
 -> main TypeDef/MethodDef/Property + PDB symbol
 -> visual asset identity/path
 -> inference from naming/grouping
 -> runtime trace for protected branch/call-site proof
```

A bundled DLL API is **capability**, not automatically an active main path. The ADB distinction is the current clearest example.
