# Character Governors for Europa Universalis V

Character Governors replaces the split between **Local Governor** and **Naval Governor** buildings with one character-driven provincial administration system.

## Gameplay

- The vanilla `local_governor` building becomes a **Governor's Residence**.
- It can be built in towns, cities and megalopolises without a road-to-capital or maritime/land-connectivity requirement.
- Local and Naval Governor capacity are pooled into one shared limit; Lieutenancies still consume that administrative capacity.
- A residence provides **50 Proximity Source** on its own instead of vanilla's 80.
- Use **Appoint Governor** to assign an eligible character to a vacant residence.
- New appointments begin as a **Normal Governor**.
- Every serving Governor appears in the dedicated **Governors** outliner-style panel with character, governed location, role and Entrenchment.
- **Right-click a Governor entry** to switch role or dismiss the Governor.
- The appointed character is marked busy, so the same person cannot simultaneously take the usual cabinet/military/other busy roles.
- Character contribution to Proximity Source is `ADM × 0.25 + DIP × 0.05 + MIL × 0.05`.
- A 50/50/50 character contributes +17.5; a 100/100/100 character contributes +35.
- Governors can be dismissed. Death automatically vacates the residence.
- A yearly integrity pass refreshes bonuses when abilities change and cleans assignments after ownership or building changes.

## Governor roles

### Normal Governor

The default role for ordinary provincial government in core territory. It retains the standard Governor administration and character-scaled Proximity contribution without an additional specialist modifier.

### Integration Governor

Intended for culturally distinct territory that should be drawn more closely into the state. In 0.2.0 the role adds **+25% local pop assimilation speed** at the Governor's Residence location.

### Colonial Governor

Intended for overseas and colonial possessions. In 0.2.0 the role adds **+25% local migration attraction** at the Governor's Residence location.

Role restrictions and deeper role-specific mechanics can be tightened in later balance passes. The current version deliberately makes all three roles directly selectable so their workflow can be tested first.

## Entrenchment

Each serving Governor and the corresponding Governor's Residence track the same **Entrenchment** value from 0 to 100.

Entrenchment advances once per yearly country pulse using:

`2 + (ADM + DIP + MIL) / 100`

Examples:

- 30/30/30 Governor: +2.9 per year.
- 50/50/50 Governor: +3.5 per year.
- 100/100/100 Governor: +5.0 per year.

Entrenchment is capped at 100. In version 0.2.0 it is **informational only**: there are deliberately no dismissal penalties, rebellion effects, Estate effects or ability penalties yet. Those consequences are reserved for the next balance step.

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

The implementation is grounded in EU5 1.3 vanilla/community-tested patterns for building replacement, character interactions, character/location selection, scope variables, variable maps exposed to GUI datamodels, scripted GUI execution with saved scopes, permanent location modifiers, scaled modifier `size`, `busy_modifier`, character-death on-actions, yearly country pulses and scripted-widget registration.

Because Paradox scripting is patch-sensitive, a release should still be smoke-tested against the exact installed patch with `script_docs`, `dump_data_types`, `error.log` and an in-game behavior test before publishing a Workshop update.
