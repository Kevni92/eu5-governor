# Steam Workshop Description

## Character Governors

Turn provincial administration into a personnel decision.

Character Governors merges EU5's Local Governor and Naval Governor concepts into one **Governor's Residence**. Build it where your realm needs a provincial administrative center, appoint an actual character to run it, then specialize that Governor for the territory.

### Features

- One unified Governor system instead of separate land/naval buildings.
- No road-to-capital or disconnected-island placement split.
- Governor's Residence: 30 base Proximity Source.
- Every Governor's Residence appears directly in the normal **right-side outliner**, including vacant offices.
- Vacant Residences are shown as **Empty Governor Slot** entries inspired by vanilla Cabinet slots.
- Click an empty portrait to choose a Governor directly for that Residence; click an occupied portrait to replace the office holder.
- Governor candidates follow the country's Cabinet legal restrictions for gender and Estate access, including individually granted Cabinet rights.
- Serving characters are displayed as **Governor** rather than **Courtier** in the character view.
- Occupied rows show a compact Governor portrait, location, Governor role and Entrenchment / Machtbasis.
- The outliner header shows **serving Governors / total Governor's Residences**.
- Appointed characters add Proximity based on ADM, with smaller DIP and MIL contributions.
- Three Governor roles:
  - **Normal Governor** for ordinary provincial administration.
  - **Integration Governor** for culturally distinct territory: +25% local pop assimilation speed.
  - **Colonial Governor** for overseas possessions: +0.25 local migration attraction and +0.001 local population growth.
- Integration Governor is only available when the location's dominant culture differs from its owner.
- Colonial Governor is only available in overseas territory.
- The currently active Governor role is disabled in the role menu and cannot be selected again.
- **Dismiss Governor** uses a red destructive-action button.
- Governors track **Entrenchment / Machtbasis** from 0 to 100.
- Machtbasis grows yearly by `2 + (ADM + DIP + MIL) / 100`, so more capable Governors establish themselves faster.
- Every Governor increases the power of their Estate by **half their Machtbasis**. At 100 Machtbasis: **+50% Estate power**.
- Governor Estate power stacks additively for Crown, Nobility, Clergy, Burghers, Peasants, Tribes, Cossacks and Dhimmi.
- Voluntarily dismissing or replacing a non-Crown Governor costs political capital in proportion to Machtbasis. At 100: **-25 percentage points Estate Satisfaction** and **-10 Legitimacy**.
- Governors belonging to the **Crown Estate** can be dismissed or replaced for free.
- Death or demolition does not count as a voluntary dismissal and does not charge the political penalty.
- Left-click elsewhere on an office row to open its location; double-click to pan there; right-click an occupied row to change role or dismiss the Governor.
- Governors are occupied by their office and cannot freely double as other busy roles.
- Local + Naval Governor capacity is pooled, so existing advances and bonuses remain useful.
- Governor death or dismissal returns the Residence to a visible vacant slot.
- Building construction/destruction updates the office list, while the yearly integrity pass repairs save/ownership state and refreshes Estate-power contributions.
- Full **English and German localization** is included. German terminology uses *Gouverneursresidenz*, *Provinzgouverneur*, *Integrationsgouverneur*, *Kolonialgouverneur* and *Machtbasis*.

### Basic workflow

1. Build a **Governor's Residence**.
2. Its vacant office appears under **Governors** in the normal outliner.
3. Click its **empty portrait** and choose an eligible character from the native selector.
4. Click an occupied portrait whenever you want to replace the Governor. Replacing an established non-Crown Governor pays the same cost as dismissing them.
5. Right-click the occupied outliner row to select another Governor role or use the red dismissal action.

### Compatibility

Replaces the vanilla `local_governor` and `naval_governor` building objects. Mods that also replace those objects need a compatibility patch.

For seamless integration, Character Governors also overrides the same-version vanilla `in_game/gui/outliner.gui` and `in_game/gui/character_lateralview.gui`. UI mods replacing either file require a compatibility patch.

Target: EU5 1.3.x. Current mod version: **0.2.4**.
