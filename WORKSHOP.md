# Steam Workshop Description

## Character Governors

Turn provincial administration into a personnel decision.

Character Governors merges EU5's Local Governor and Naval Governor concepts into one **Governor's Residence**. Build it where your realm needs a provincial administrative center, appoint an actual character to run it, then specialize that Governor for the territory.

### Features

- One unified Governor system instead of separate land/naval buildings.
- No road-to-capital or disconnected-island placement split.
- Governor's Residence: 50 base Proximity Source.
- Appointed characters add Proximity based on ADM, with smaller DIP and MIL contributions.
- Three Governor roles:
  - **Normal Governor** for ordinary provincial administration.
  - **Integration Governor** for culturally distinct territory: +25% local pop assimilation speed.
  - **Colonial Governor** for overseas possessions: +0.25 local migration attraction.
- Integration Governor is only available when the location's dominant culture differs from its owner.
- Colonial Governor is only available in overseas territory.
- Governors track **Entrenchment** from 0 to 100.
- Entrenchment grows yearly by `2 + (ADM + DIP + MIL) / 100`, so more capable Governors establish themselves faster.
- Entrenchment is informational in version 0.2.0; political and dismissal consequences are planned for the next balance step.
- Dedicated **Governors** outliner-style management block showing character, location, role and Entrenchment.
- Left-click a Governor to open the character; right-click to change role or dismiss them.
- Governors are occupied by their office and cannot freely double as other busy roles.
- Local + Naval Governor capacity is pooled, so existing advances and bonuses remain useful.
- Governor death, dismissal, conquest and building changes are cleaned up automatically.
- The Governor UI is an additive scripted widget and does not replace the full vanilla `outliner.gui` file.

### Compatibility

Replaces the vanilla `local_governor` and `naval_governor` building objects. Mods that also replace those objects need a compatibility patch. UI mods occupying the same top-right screen space may require a positioning adjustment.

Target: EU5 1.3.x.
