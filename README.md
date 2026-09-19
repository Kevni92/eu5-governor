# Character Governors for Europa Universalis V

Character Governors replaces the split between **Local Governor** and **Naval Governor** buildings with one character-driven provincial administration system.

## Gameplay

- The vanilla `local_governor` building becomes a **Governor's Residence**.
- It can be built in towns, cities and megalopolises without a road-to-capital or maritime/land-connectivity requirement.
- Local and Naval Governor capacity are pooled into one shared limit; Lieutenancies still consume that administrative capacity.
- A residence provides **50 Proximity Source** on its own instead of vanilla's 80.
- Every owned Governor's Residence appears as an office slot directly inside the normal EU5 outliner, including vacant offices.
- Click the portrait of a vacant office to open the native Governor character chooser directly for that Residence.
- Click the portrait of an occupied office to replace the Governor, matching the vanilla Cabinet slot workflow.
- New appointments begin as a **Normal Governor** with 0 Entrenchment.
- Occupied outliner rows show the Governor portrait, character name, governed location, current role and Entrenchment.
- **Left-click** elsewhere on an office row to open its location, **double-click** to pan to it, and **right-click** an occupied row to switch role or dismiss the Governor.
- The currently active Governor role is disabled in the role menu; it cannot be selected again.
- The dismissal entry uses the vanilla red/destructive button style.
- The appointed character is marked busy, so the same person cannot simultaneously take the usual cabinet/military/other busy roles.
- The character view displays an appointed office holder as **Governor** instead of **Courtier**.
- Character contribution to Proximity Source is `ADM × 0.25 + DIP × 0.05 + MIL × 0.05`.
- A 50/50/50 character contributes +17.5; a 100/100/100 character contributes +35.
- A serving Governor increases the power of their Estate by **half their Entrenchment/Machtbasis**. At 100 Machtbasis that is **+50% Estate power**.
- Voluntarily dismissing or replacing a non-Crown Governor has political costs that scale with Machtbasis. At 100: **-25 percentage points Estate Satisfaction** and **-10 Legitimacy**. Crown Governors are free to dismiss or replace.
- Governors can be dismissed. Death automatically vacates the residence without a dismissal penalty, but the vacant office remains visible in the outliner.
- A yearly integrity pass refreshes bonuses, Machtbasis, Estate-power contributions, the complete Governor-office roster and stale assignments.
- English and German localization are included.

## How to use it

1. Build a **Governor's Residence** in an eligible owned location.
2. The Residence appears under **Governors** in the normal right-side outliner as an **Empty Governor Slot** / **Unbesetzter Gouverneursposten**.
3. Click the **empty portrait** in that row. EU5 opens the native character chooser already bound to that Governor's Residence.
4. Select an eligible character. The empty slot becomes an occupied office and displays the Governor's portrait and data.
5. Click an **occupied portrait** to replace that Governor with another eligible character. Replacing an established non-Crown Governor pays the same political cost as dismissal.
6. Right-click the occupied office to change between **Normal Governor**, **Integration Governor** and **Colonial Governor**, or to dismiss the Governor. The current role is disabled.
7. Dismissing or losing the Governor returns the office to the visible vacant-slot state rather than removing the row.

The original **Appoint Governor** character interaction remains available as an alternate path and uses the same eligibility filter.

## Governor eligibility

Governor appointment mirrors the **script-visible vanilla Cabinet restrictions** before applying Governor-specific exclusivity.

A candidate must be alive, adult and loyal, must not be blocked from Cabinet service, and must belong to an Estate that the country is legally allowed to use in the Cabinet. Gender follows the country's Cabinet law: `gender_equality`, `allow_male_cabinet`, `allow_female_cabinet`, `block_male_cabinet` and `block_female_cabinet` are respected. A character with an individually granted Cabinet right (`ignore_gender_block_cabinet`) may bypass the gender restriction just as in the vanilla Cabinet system.

Governorship is intentionally more exclusive than Cabinet eligibility: the candidate must also be free from an existing Cabinet post, military command, exploration assignment or another governorship.

## Governor roles

Changing a role does not reset Entrenchment. The role already held by the Governor is disabled in the right-click menu.

### Normal Governor

The default role for ordinary provincial government in core or home territory. It retains the standard Governor administration and character-scaled Proximity contribution without an additional specialist modifier.

### Integration Governor

Intended for culturally distinct possessions, such as Italian territory governed by France.

- Selectable only while the governed location's dominant culture differs from the owner's culture.
- Grants **+25% local pop assimilation speed** at the Governor's Residence location.

### Colonial Governor

Intended for overseas and New World possessions.

- Selectable only where `is_overseas_for_owner = yes`.
- Grants **+0.25 local migration attraction** at the Governor's Residence location.

These specialist values are deliberately conservative first-pass numbers and can be rebalanced after in-game testing.

## Entrenchment / Machtbasis

Each serving Governor and the corresponding Governor's Residence track the same **Entrenchment** value from 0 to 100. The German localization calls this **Machtbasis**.

Entrenchment advances once per yearly country pulse using:

`2 + (ADM + DIP + MIL) / 100`

Examples:

- 30/30/30 Governor: +2.9 per year.
- 50/50/50 Governor: +3.5 per year.
- 100/100/100 Governor: +5.0 per year.

Entrenchment is capped at 100 and now has two direct political consequences.

### Estate power

Every serving Governor increases the power of their own Estate by half their Machtbasis:

`Estate power bonus = Machtbasis / 2 %`

Examples:

- 20 Machtbasis -> +10% Estate power.
- 50 Machtbasis -> +25% Estate power.
- 100 Machtbasis -> +50% Estate power.

Governors belonging to the same Estate stack additively. Their contributions are aggregated into one country modifier per Estate. The implementation covers Crown, Nobility, Clergy, Burghers, Peasants, Tribes, Cossacks and Dhimmi.

### Voluntary dismissal / replacement

For a non-Crown Governor, dismissal costs scale linearly with Machtbasis:

- Estate Satisfaction: `Machtbasis × -0.0025` -> at 100, **-25 percentage points**.
- Legitimacy: `Machtbasis × -0.10` -> at 100, **-10 Legitimacy**.

Replacing an existing Governor counts as voluntarily dismissing the outgoing office holder and pays the same cost. This prevents replacement from bypassing the mechanic. A Governor belonging to the **Crown Estate** can be dismissed or replaced without either penalty.

Death, demolition and integrity cleanup are not voluntary dismissals and therefore do not charge these political costs; their Estate-power contribution is simply removed.

## Governor management UI

Version 0.2.3 integrated the **Governors** section directly into the vanilla outliner's own scroll content. Version 0.2.4 fixes the role context menu so each entry uses the actual clickable inner `ContextMenuEntry` button. The old free-standing scripted widget remains removed, so the Governor block follows the right-side outliner's position, width and scrolling behavior.

The UI is driven by two country variable maps:

- `eu5gov_governor_offices`: all Governor's Residence locations, whether occupied or vacant.
- `eu5gov_governor_roster`: serving Governor characters and their locations.

The header displays **serving Governors / total Governor's Residences**. The all-office map is updated immediately when a Residence is built or destroyed and rebuilt by the yearly integrity pass for save migration and repair.

Vacant rows show **Empty Governor Slot**, the Residence location and **Vacant**. Occupied rows show the portrait, Governor name, Residence location, role and Entrenchment. The portrait controls use dedicated `owncountry` generic actions with the clicked Residence pre-bound as `scope:target_1`; the action then opens EU5's native character selector. Right-clicking an occupied row opens direct actions for **Normal Governor**, **Integration Governor**, **Colonial Governor** and **Dismiss Governor**. Specialist roles are disabled when their territorial requirement is not met; the active role is also disabled. The dismissal entry uses the vanilla red button texture.

### Character role display

EU5's `CharacterRoleMask` is engine-backed and the same-version script/game files expose no supported effect for registering a new custom role in that mask. Therefore the mod does not fake a Governor by assigning an unrelated vanilla job. Instead, `eu5gov_governorship` remains the authoritative gameplay office state, while the character view displays **Governor / Gouverneur** for characters holding that state. Governor exclusivity is enforced independently through the appointment rules and `busy_modifier`.

## Why the vanilla building ID is retained

The unified residence deliberately keeps the internal ID `local_governor`. This preserves as many existing advances, scripted references and AI expectations as possible. `naval_governor` is retired as a buildable object, but `num_naval_governors` still contributes to the shared capacity.

## Compatibility

This mod replaces the database objects `local_governor` and `naval_governor`. Mods that also replace either building require a compatibility patch.

For seamless UI integration, the mod also supplies same-version overrides of:

- `in_game/gui/outliner.gui` — inserts the Governor section into the native outliner scroll container and its context menu.
- `in_game/gui/character_lateralview.gui` — displays Governor/Gouverneur as the current role while the character holds a governorship.

UI mods that replace either of those files require a compatibility patch. These overrides are based on the EU5 1.3.x vanilla reference used by the mod and should be re-audited after game patches that change those GUI files.

Existing `local_governor` buildings become Governor's Residences. Existing `naval_governor` buildings are removed by the legacy replacement and their capacity becomes available for a Governor's Residence.

## Installation / Workshop

The repository root is the playable mod root. It includes `.metadata/metadata.json` and can be copied directly into an EU5 mod workspace or used as the source for a Steam Workshop upload.

Target metadata: **EU5 1.3.x**.

## Verification status

The implementation is grounded in EU5 1.3 vanilla/community-tested patterns for building replacement, building `on_built`/`on_destroyed` hooks, character interactions, generic actions with character selectors, dynamic Estate Satisfaction types, script-value Legitimacy effects, Estate-power modifier identifiers, scaled country/location modifier `size`, scope variables, variable maps exposed to GUI datamodels, vanilla outliner structures, native GUI `action_button` invocation, scripted GUI execution with saved scopes, `busy_modifier`, character-death on-actions, yearly country pulses, context menus, `dominant_culture` checks and `is_overseas_for_owner`.

Because Paradox scripting and GUI are patch-sensitive, the release should still be smoke-tested against the exact installed patch with `script_docs`, `dump_data_types`, `error.log` and an in-game behavior test before publishing a Workshop update. For 0.2.4 specifically verify: role buttons execute, the current role is disabled, dismissal is red, Crown dismissal is free, non-Crown dismissal applies the scaled penalties, and Estate power changes by exactly half Machtbasis.
