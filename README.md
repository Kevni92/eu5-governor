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
- **Left-click** a Governor entry to open the character; **right-click** to switch role or dismiss the Governor.
- The appointed character is marked busy, so the same person cannot simultaneously take the usual cabinet/military/other busy roles.
- Character contribution to Proximity Source is `ADM × 0.25 + DIP × 0.05 + MIL × 0.05`.
- A 50/50/50 character contributes +17.5; a 100/100/100 character contributes +35.
- Governors can be dismissed. Death automatically vacates the residence.
- A yearly integrity pass refreshes bonuses when abilities change and cleans assignments after ownership or building changes.

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

Entrenchment is capped at 100. In version 0.2.0 it is **informational only**: there are deliberately no dismissal penalties, rebellion effects, Estate effects or ability penalties yet. Those consequences are reserved for the next balance step.

## Governor management UI

The mod adds a dedicated **Governors** outliner-style block through EU5's scripted-widget system. The header is collapsible and displays the number of serving Governors.

Each row shows the character, governed location, current role and Entrenchment. Right-clicking opens direct actions for **Normal Governor**, **Integration Governor**, **Colonial Governor** and **Dismiss Governor**. Specialist roles are disabled when their territorial requirement is not met.

The roster is backed by the country variable map `eu5gov_governor_roster` and is rebuilt/healed by the yearly integrity pass. Existing 0.1 assignments are migrated lazily: missing role and Entrenchment state becomes Normal Governor / 0 on the next yearly pass.

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

The implementation is grounded in EU5 1.3 vanilla/community-tested patterns for building replacement, character interactions, character/location selection, scope variables, variable maps exposed to GUI datamodels, scripted GUI execution with saved scopes, permanent location modifiers, scaled modifier `size`, `busy_modifier`, character-death on-actions, yearly country pulses, scripted-widget registration, context menus, `dominant_culture` checks and `is_overseas_for_owner`.

Because Paradox scripting and GUI are patch-sensitive, a release should still be smoke-tested against the exact installed patch with `script_docs`, `dump_data_types`, `error.log` and an in-game behavior test before publishing a Workshop update.
