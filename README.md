# Character Governors for Europa Universalis V

Character Governors replaces the split between **Local Governor** and **Naval Governor** buildings with one character-driven provincial administration system.

## Gameplay

- The vanilla `local_governor` building becomes a **Governor's Residence**.
- It can be built in towns, cities and megalopolises without a road-to-capital or maritime/land-connectivity requirement.
- Local and Naval Governor capacity are pooled into one shared limit; Lieutenancies still consume that administrative capacity.
- A residence provides **50 Proximity Source** on its own instead of vanilla's 80.
- Use **Appoint Governor** to assign an eligible character to a vacant residence.
- The appointed character is marked busy, so the same person cannot simultaneously take the usual cabinet/military/other busy roles.
- Character contribution to Proximity Source is `ADM × 0.25 + DIP × 0.05 + MIL × 0.05`.
- A 50/50/50 character contributes +17.5; a 100/100/100 character contributes +35.
- Governors can be dismissed. Death automatically vacates the residence.
- A yearly integrity pass refreshes bonuses when abilities change and cleans assignments after ownership or building changes.

## Why the vanilla building ID is retained

The unified residence deliberately keeps the internal ID `local_governor`. This preserves as many existing advances, scripted references and AI expectations as possible. `naval_governor` is retired as a buildable object, but `num_naval_governors` still contributes to the shared capacity.

## Compatibility

This mod replaces the database objects `local_governor` and `naval_governor`. Mods that also replace either building require a compatibility patch. It does not override GUI files.

Existing `local_governor` buildings become Governor's Residences. Existing `naval_governor` buildings are removed by the legacy replacement and their capacity becomes available for a Governor's Residence.

## Installation / Workshop

The repository root is the playable mod root. It includes `.metadata/metadata.json` and can be copied directly into an EU5 mod workspace or used as the source for a Steam Workshop upload.

Target metadata: **EU5 1.3.x**.

## Verification status

The implementation is grounded in EU5 1.3 vanilla patterns for building replacement, character interactions, character/location selection, scope variables, permanent location modifiers, scaled modifier `size`, `busy_modifier`, character-death on-actions and yearly country pulses.

Because Paradox scripting is patch-sensitive, a release should still be smoke-tested against the exact installed patch with `script_docs`, `error.log` and an in-game behavior test before publishing a Workshop update.
