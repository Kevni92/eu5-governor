# Character Governors for Europa Universalis V

Character Governors replaces the split between **Local Governor** and **Naval Governor** buildings with one character-driven provincial administration system.

## Gameplay

- The vanilla `local_governor` building becomes a **Governor's Residence**.
- It can be built in towns, cities and megalopolises without a road-to-capital or maritime/land-connectivity requirement.
- Local and Naval Governor capacity are pooled into one shared limit; Lieutenancies still consume that administrative capacity.
- A residence provides **50 Proximity Source** on its own instead of vanilla's 80.
- Every owned Governor's Residence appears as an office slot in the dedicated **Governors** outliner, including vacant offices.
- Click the portrait of a vacant office to open the Governor character chooser directly for that Residence.
- Click the portrait of an occupied office to replace the Governor, matching the vanilla Cabinet slot workflow.
- New appointments begin as a **Normal Governor** with 0 Entrenchment.
- Occupied outliner rows show the Governor portrait, character name, governed location, current role and Entrenchment.
- **Left-click** elsewhere on an office row to open its location, **double-click** to pan to it, and **right-click** an occupied row to switch role or dismiss the Governor.
- The appointed character is marked busy, so the same person cannot simultaneously take the usual cabinet/military/other busy roles.
- Character contribution to Proximity Source is `ADM × 0.25 + DIP × 0.05 + MIL × 0.05`.
- A 50/50/50 character contributes +17.5; a 100/100/100 character contributes +35.
- Governors can be dismissed. Death automatically vacates the residence, but the vacant office remains visible in the outliner.
- A yearly integrity pass refreshes bonuses, rebuilds the complete Governor-office roster and cleans assignments after ownership or building changes.

## How to use it

1. Build a **Governor's Residence** in an eligible owned location.
2. The Residence immediately appears under **Governors** as an **Empty Governor Slot**, similar to an inactive Cabinet entry.
3. Click the **empty portrait** in that row. EU5 opens the native character chooser already bound to that Governor's Residence.
4. Select an eligible character. The empty slot becomes an occupied office and displays the Governor's portrait and data.
5. Click an **occupied portrait** to replace that Governor with another eligible character.
6. Right-click the occupied office to change between **Normal Governor**, **Integration Governor** and **Colonial Governor**, or to dismiss the Governor.
7. Dismissing or losing the Governor returns the office to the visible vacant-slot state rather than removing the row.

The original **Appoint Governor** character interaction remains available as an alternate path and uses the same eligibility filter.

## Governor eligibility

Governor appointment mirrors the **script-visible vanilla Cabinet restrictions** before applying Governor-specific exclusivity.

A candidate must be alive, adult and loyal, must not be blocked from Cabinet service, and must belong to an Estate that the country is legally allowed to use in the Cabinet. Gender follows the country's Cabinet law: `gender_equality`, `allow_male_cabinet`, `allow_female_cabinet`, `block_male_cabinet` and `block_female_cabinet` are respected. A character with an individually granted Cabinet right (`ignore_gender_block_cabinet`) may bypass the gender restriction just as in the vanilla Cabinet system.

Governorship is intentionally more exclusive than Cabinet eligibility: the candidate must also be free from an existing Cabinet post, military command, exploration assignment or another governorship.

## Governor roles

Changing a role does not reset Entrenchment.

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

## Entrenchment

Each serving Governor and the corresponding Governor's Residence track the same **Entrenchment** value from 0 to 100.

Entrenchment advances once per yearly country pulse using:

`2 + (ADM + DIP + MIL) / 100`

Examples:

- 30/30/30 Governor: +2.9 per year.
- 50/50/50 Governor: +3.5 per year.
- 100/100/100 Governor: +5.0 per year.

Entrenchment is capped at 100. In version 0.2.x it is **informational only**: there are deliberately no dismissal penalties, rebellion effects, Estate effects or ability penalties yet. Those consequences are reserved for the next balance step.

## Governor management UI

The mod adds a dedicated **Governors** outliner-style block through EU5's scripted-widget system. It deliberately follows the visual language of the vanilla Cabinet outliner: compact paper rows, a small portrait slot, portrait-driven appointment/replacement and a persistent empty-office state.

The UI is driven by two country variable maps:

- `eu5gov_governor_offices`: all Governor's Residence locations, whether occupied or vacant.
- `eu5gov_governor_roster`: serving Governor characters and their locations.

The header displays **serving Governors / total Governor's Residences**. The all-office map is updated immediately when a Residence is built or destroyed and rebuilt by the yearly integrity pass for save migration and repair.

Vacant rows show **Empty Governor Slot**, the Residence location and **Vacant**. Occupied rows show the portrait, Governor name, Residence location, role and Entrenchment. Right-clicking an occupied row opens direct actions for **Normal Governor**, **Integration Governor**, **Colonial Governor** and **Dismiss Governor**. Specialist roles are disabled when their territorial requirement is not met.

## Why the vanilla building ID is retained

The unified residence deliberately keeps the internal ID `local_governor`. This preserves as many existing advances, scripted references and AI expectations as possible. `naval_governor` is retired as a buildable object, but `num_naval_governors` still contributes to the shared capacity.

## Compatibility

This mod replaces the database objects `local_governor` and `naval_governor`. Mods that also replace either building require a compatibility patch.

The Governor management UI is supplied as its own scripted widget rather than replacing the full vanilla `outliner.gui`, which avoids a large whole-file GUI override. UI mods that place their own permanent widgets in the same top-right screen region may still require positioning adjustments.

Existing `local_governor` buildings become Governor's Residences. Existing `naval_governor` buildings are removed by the legacy replacement and their capacity becomes available for a Governor's Residence.

## Installation / Workshop

The repository root is the playable mod root. It includes `.metadata/metadata.json` and can be copied directly into an EU5 mod workspace or used as the source for a Steam Workshop upload.

Target metadata: **EU5 1.3.x**.

## Verification status

The implementation is grounded in EU5 1.3 vanilla/community-tested patterns for building replacement, building `on_built`/`on_destroyed` hooks, character interactions, character/location selection, script-visible Cabinet restrictions, scope variables, variable maps exposed to GUI datamodels, Cabinet-style outliner widgets, native GUI `action_button` invocation, scripted GUI execution with saved scopes, permanent location modifiers, scaled modifier `size`, `busy_modifier`, character-death on-actions, yearly country pulses, scripted-widget registration, context menus, `dominant_culture` checks and `is_overseas_for_owner`.

Because Paradox scripting and GUI are patch-sensitive, a release should still be smoke-tested against the exact installed patch with `script_docs`, `dump_data_types`, `error.log` and an in-game behavior test before publishing a Workshop update. The portrait-bound `target_1` character-interaction path is specifically worth validating in runtime because the native Cabinet candidate list itself is partly engine-backed.
