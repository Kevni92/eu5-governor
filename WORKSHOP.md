# Steam Workshop Description

## Character Governors

Turn provincial administration into a personnel decision.

Character Governors merges EU5's Local Governor and Naval Governor concepts into one **Governor's Residence**. Build it where your realm needs a provincial administrative center, appoint an actual character to run it, then specialize that Governor for the territory.

### Features

- One unified Governor system instead of separate land/naval buildings.
- No road-to-capital or disconnected-island placement split.
- Governor's Residence: 50 base Proximity Source.
- Every Governor's Residence appears in the **Governors** outliner, including vacant offices.
- Vacant Residences are shown as **Empty Governor Slot** entries inspired by vanilla Cabinet slots.
- Occupied rows show a compact Governor portrait, location, Governor role and Entrenchment.
- The outliner header shows **serving Governors / total Governor's Residences**.
- Appointed characters add Proximity based on ADM, with smaller DIP and MIL contributions.
- Three Governor roles:
  - **Normal Governor** for ordinary provincial administration.
  - **Integration Governor** for culturally distinct territory: +25% local pop assimilation speed.
  - **Colonial Governor** for overseas possessions: +0.25 local migration attraction.
- Integration Governor is only available when the location's dominant culture differs from its owner.
- Colonial Governor is only available in overseas territory.
- Governors track **Entrenchment** from 0 to 100.
- Entrenchment grows yearly by `2 + (ADM + DIP + MIL) / 100`, so more capable Governors establish themselves faster.
- Entrenchment is informational in version 0.2.x; political and dismissal consequences are planned for the next balance step.
- Left-click an office row to open its location; double-click to pan there; use the portrait for the character; right-click an occupied row to change role or dismiss the Governor.
- Governors are occupied by their office and cannot freely double as other busy roles.
- Local + Naval Governor capacity is pooled, so existing advances and bonuses remain useful.
- Governor death or dismissal returns the Residence to a visible vacant slot.
- Building construction/destruction updates the office list, while the yearly integrity pass repairs save/ownership state.
- The Governor UI is an additive scripted widget and does not replace the full vanilla `outliner.gui` file.

### Basic workflow

1. Build a **Governor's Residence**.
2. Its vacant office appears in the **Governors** outliner.
3. Use **Appoint Governor** and choose an eligible character and a vacant Residence.
4. Right-click the occupied outliner row to select its Governor role or dismiss the Governor.

### Compatibility

Replaces the vanilla `local_governor` and `naval_governor` building objects. Mods that also replace those objects need a compatibility patch. UI mods occupying the same top-right screen space may require a positioning adjustment.

Target: EU5 1.3.x.
