# 05 — DATA-333 donor behavior -> DATA-2222 semantic bridge

## Principle

DATA-333 answers: **what behavior/policy did the existing external auto attempt?**

DATA-2222 answers: **what semantic client/runtime state/action can implement that behavior more reliably?**

The rebuilt tool should not blindly reproduce every image click if the equivalent client semantic action is already solved.

## Bridge matrix

| DATA-333 donor area | Donor evidence | DATA-2222 semantic target | Migration direction |
|---|---|---|---|
| Train | `trainLEVEL1`, `setupautotrain`, visual map/auto markers | Train state/start-stop, target/chase/skill runtime contracts | keep policy/map choice; replace start/combat clicks with semantic state/action |
| Monster targeting | image lists / `bangdanhsachquai` / combat markers | nearby monster scanner, target/chase/use-skill | replace visual target discovery when runtime scanner is available |
| Sell | `sellItemm`, 435 item visual templates, NPC sell navigation | live item instance semantics + exact Sell action | preserve keep/sell policy, replace icon identity and click sequence |
| Storage | `catdovaokho`, `laydotrongkho`, storage templates | item Move action/site semantics | replace slot/image clicking with live instance -> destination site mutation |
| Consumables | HP/mana images, `autodungmau`, quantities/thresholds | runtime HP/MaxHP, bag medicines, semantic use action | preserve thresholds/policy; replace OCR/image state where possible |
| NPC routing | `toinpc*`, map/NPC templates | `GetNPCPosition`, navigation, ClickNPC/GameDialog | replace fixed/pixel routes with semantic navigation/dialog state |
| Treatment/revive | treatment/Đầu thai templates, `checktrilieutudong` | dynamic GameDialog + revive semantics | preserve recovery policy; use current dialog/state proof |
| Party/follow | `autoPT`, invite/follow/leave templates | team member state + join/leave/follow requests | replace UI dialog clicks with semantic team actions where solved |
| Loot | bag/full/item visual state | ItemPack/runtime loot + bag free space | use runtime item/bag state; preserve donor loot priorities if recovered |
| Trade/dồn đồ | trade UI templates + coordinate state | trade session/ExchangeID/live-instance semantics | preserve orchestration policy; replace UI-only session control |
| Map transfer | `truyenmap`, many map markers | semantic movement/NPC/portal routing | use donor destinations, not donor pixels |
| Pet/Spirit | pet methods/templates | DATA-2222 pet/spirit runtime donor/database | map donor policy to semantic companion actions |
| Auto Quest | quest accept/continue/complete templates | task/objective/navigation donor contracts | visual UI only as fallback |
| Thủy Lao / FuBen-like flows | dedicated state templates + stage fields | FuBen scenario/action/boss knowledge where applicable | preserve feature state machine; substitute semantic state/actions stage by stage |
| Ác Tặc/activity | coordinate map and activity templates | map/NPC/monster semantic scanner/actions | preserve schedule/spot policy; replace brittle state detection |
| Captcha | `SoveNormalCapt`, captcha status/images | DATA-2222 safety contract | pause for user handling, do not automate bypass |

## Donor facts worth preserving even after semantic migration

Image-driven code may still encode valuable **policy**, even when its input method should be replaced:

- which activity is attempted first;
- map/spot preferences;
- HP/mana thresholds;
- item keep/sell categories;
- account rotation behavior;
- party composition assumptions;
- timeout/retry/fallback ordering;
- return-to-town/return-to-train decisions;
- dungeon stage ordering;
- schedule rules.

Recover these separately from the click implementation.

## Recommended rebuilt architecture

```text
DATA-2222 Resolver/Scanner
 -> immutable per-PID/client snapshot
 -> DATA-333-derived policy/state machine
 -> safety/arbitration
 -> semantic DATA-2222 action when available
 -> visual/ADB fallback only for missing semantic surface
 -> state proof
```

For emulator-only tasks (launcher/login/captcha/manual UI before game runtime exists), DATA-333 ADB/Win32/vision primitives remain appropriate.

## Three-level action selection

For every donor click, classify:

### Level 1 — semantic action available

Use DATA-2222 state/action contract. Image template can remain optional telemetry/fallback.

### Level 2 — semantic state available, action not available

Use semantic state for guards/proof; use DATA-333 UI input only for the mutation.

### Level 3 — no semantic surface

Use DATA-333 visual detector + normalized ADB/Win32 action + explicit post-state proof.

## Migration anti-pattern

Do not create a new auto by mechanically translating:

```text
find image A -> click fixed point -> sleep 2s -> find image B
```

into another language/framework.

Translate the donor intent into:

```text
state A
 -> guard
 -> action X
 -> expected state B
 -> timeout/retry/recovery
```

Then select the strongest observation/action source available across DATA-2222 and DATA-333.
