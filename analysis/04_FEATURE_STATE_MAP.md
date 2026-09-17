# 04 — Feature/state map recovered from PDB and assets

This file records donor-tool feature intent. Method/property existence is static evidence; exact runtime sequencing must be proven separately where marked.

## 1. Core orchestration

**VERIFIED-PDB**

- `LoadDevices`
- `LoadListDevices`
- `LoadQuest`
- `StartQuestDevice`
- `StartAllSelectedDevice`
- `waitDevice`
- `ListDevices`
- `SelectedDevice`
- `IsSelectAllDevice`
- `IsSelectAllQuest`
- `IsRuningQuest`
- `QuestThread`
- `CheckQuestThread`
- `QuestToDo`
- `QuestName`

Interpretation: the operator can select devices/tasks and launch per-device work, with separate worker/check state.

## 2. Account/login rotation

**VERIFIED-PDB**

- `AccountInfo`
- `Accounts`
- `CurrentAccountIndex`
- `taikhoan`
- `matkhau`
- `AUTOLOGIN`
- `nhaptkmk`
- `vaolaigame`
- `closeapp`
- `GetAcc`

Runtime persistence folders `luufile/taikhoan/` and `luufile/matkhau/` exist.

**PROBABLE:** DeviceInfo owns an account list and can rotate/re-login accounts during long-running automation.

## 3. Train/leveling

**VERIFIED-PDB / VERIFIED-ASSET**

Symbols:

- `trainLEVEL1`
- `setupautotrain`
- `TRAINLV`
- `trainlevelNEW`
- `TRANGTHAI_TRAIN`
- `tenmaptrain`
- `BAITRAIN_ALL`
- `BaiTrainSelected`
- `BaiTrainAll`
- `lenbaitrain`
- `clickmap`
- `batdanh`, `tatdanh`, `batbuff`, `batsach`

Assets include map markers, auto settings, target/monster list and combat states.

## 4. Party/team/follow

**VERIFIED-PDB / VERIFIED-ASSET**

- `autoPT`
- `TAO_PT_1NGUOI`
- `THOAT_PT`
- `THOAT_VAOLAI_PT`
- `taoptdoi`
- `duyetPT`
- `checkptdoi`
- `checkthanhvien`
- `fullpt`
- `locPT`
- `sttTEAM`
- `theodoi`
- `botheodoi`

Assets include invite/join/leave/follow and party-channel markers.

## 5. Sell / trash-item filtering

**VERIFIED-PDB / VERIFIED-ASSET**

- `sellItemm`
- `sellItem`
- `banitem`
- `donrac`
- `checkfulltui`
- `loctrangbi`
- `cleartrangbi`
- `vutalltrangbi`
- `vuthettrangbi`
- `toinpcbanitem_daily`

Dedicated visual libraries:

- `ItemSell_TrangVatPham/` — 435 templates
- `ItemSell_TrangNgoc/` — 11 templates
- `itemrac/` — 91 templates

This is one of the strongest examples of donor behavior that should be migrated to semantic item identity/policy from DATA-2222 when rebuilding.

## 6. Storage/bank/item transfer

**VERIFIED-PDB / VERIFIED-ASSET**

- `catdo`
- `catdovaokho`
- `laydotrongkho`
- `Chuyendovaokho`
- `chuyenitem`
- `chuyenitemvang`
- `dungvang`

Assets:

- `Item_vaokho/`
- `KEY_KHO/`
- `OUT_KHO/`
- storage/open-slot markers in `hoatdong/`.

## 7. Consumables, HP/mana and auto-use

**VERIFIED-PDB / VERIFIED-ASSET**

- `autodungmau`
- `lienketmau_manalenauto`
- `phantramHP`
- `soluongmau`
- `soluongmana`
- `muamau`
- `muamana`
- `muamaumana`
- `muathemmau`
- `muathemmana`
- `toinpc_duoc`

Assets include medicine, HP/mana, NPC dược and inventory markers.

## 8. Pet/horse/companion

**VERIFIED-PDB / VERIFIED-ASSET**

- `xuatpet`
- `muadochoipet`
- `muadochopet`
- `muathemdoanpet`
- `soluongdochoi`
- `soluongthucan`
- `phanloaithucan`
- `locthucuoi`
- `coitemngua`
- `xuongngua`

`luufile/thucanPET/` exists. Assets include pet/horse state and pet-NPC markers.

## 9. Thủy Lao

**VERIFIED-PDB / VERIFIED-ASSET**

- `setupautothuylao`
- `toinpcthuylao`
- `vaothuylao`
- `hdthuylao`
- `thuylao`
- `TRANGTHAI_THUYLAO`
- `sttbaithuylao`

The `thuylao/` folder has 59 templates covering entry, party, combat, boss, revive/Đầu thai, coordinates/stages and completion.

## 10. Ác Tặc / activity automation

**VERIFIED-PDB / VERIFIED-ASSET**

- `setupautotrungac`
- `danh_actac`
- `toivitri_actac`
- `gettoado_actac`
- `toado_actac`
- `MAPACTAC`
- `HDACTAC` / `HD_ACTAC`
- `TRANGTHAI_ACTAC`
- `TRANGTHAITIMACTAC`
- `TRANGTHAI_TRUNGAC`

Persistence path `luufile/TOADO_ACTAC/data/` exists.

## 11. Tàng Bảo Đồ-like donor flow (`TBD` symbols)

**VERIFIED-PDB** for names; exact Vietnamese expansion should not be treated as proven.

- `nhannvTBD`
- `toinpcTBD`
- `chayTBD`
- `MaxTBD`
- `TotalBTD`
- `tranvTBD`
- `huynvTBD`
- `danhluaquai`

Assets also contain multiple `tbd`/boss/quest-state markers.

## 12. Navigation / map transfer / NPC routing

**VERIFIED-PDB / VERIFIED-ASSET**

- `truyenmap`
- `Truyenvetochau`
- `laytoadotrongGame`
- `checkdichuyen`
- `dichuyen`
- `toadoclickX`
- `toadoX`, `toadoY`, `toado1`
- numerous map/NPC/transfer templates

This donor layer is highly pixel/coordinate based and is a major candidate for replacement by semantic navigation from DATA-2222.

## 13. Treatment / revive / death recovery

**VERIFIED-PDB / VERIFIED-ASSET**

- `checktrilieutudong`
- `trilieudaily`
- `trilieutochaux`
- `danhytrilieu`
- `dungphuvetochau`
- assets such as `trilieu`, `dauthai`, death/HP states and healer/NPC positions.

## 14. Trade/item consolidation

**VERIFIED-PDB / VERIFIED-ASSET**

Properties and assets expose:

- `trangthaigd`
- `vitrigiaodich`
- `vitrigdX`, `vitrigdY`
- trade/invite/confirm UI templates (`gd`, `giaodich`, `banggd`, `bangmoigd`, confirmation states).

Exact trade sequencing is not fully recovered from the symbol list alone.

## 15. Scheduled automation

**VERIFIED-PDB**

- `TimerCheckHenGio_Tick`
- `HenGio`
- `IsHenGio`
- `ThoiGian`
- `IsThoiGian`
- numerous start-time/time local variables.

This is a host-side scheduler/control feature, independent of client semantic state.

## 16. Captcha/manual interruption

**VERIFIED-PDB / VERIFIED-ASSET**

- `SoveNormalCapt`
- `Nomal`
- `TwoCaptResponseStatus`
- `giaicaptcha`
- `slgiaicaptcha`
- `slCAPTCHA`
- `bangcaptcha` asset

Document the donor state, but production rebuilding should use a user-intervention pause rather than automated captcha bypass.

## 17. Update/auth watchdog

**VERIFIED-PDB**

- `TimerCheckAuthorize_Tick`
- `CheckLicense`
- `CheckKey`
- `CheckMutant`
- `CheckUpdate`
- `AutoUpdaterOnCheckForUpdateEvent`

This means a running automation session can be interrupted by authorization/update logic; this control plane should be separated from gameplay state in a rebuild.

## 18. Suggested normalized state model for a rebuild

Instead of hundreds of loosely coupled fields in MainWindow, normalize to:

```text
DeviceRuntime
  identity: pid/vmpid/adbSerial/windowHandle/viewport
  account: current + queue
  connectivity: online/offline/loading
  screen: latest observation + timestamp
  activity: Idle/Train/Party/Sell/Storage/ThuyLao/AcTac/TBD/Quest/Trade/Recovery
  substate: feature-owned enum
  inventory policy
  consumable policy
  navigation target
  pending action
  last proof
  timeout/retry budget
  manual-intervention reason
```

Each feature should own its state and emit at most one mutable action at a time per device.
