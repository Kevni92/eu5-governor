# Changelog

## 0.2.4

- Fixed the Governor role context menu so its entries use the actual clickable inner `ContextMenuEntry` button instead of placing enabled state on the non-interactive wrapper widget.
- The currently active Governor role is now disabled and cannot be selected again.
- `Dismiss Governor` now uses the vanilla red/destructive button texture.
- A serving Governor now increases the power of their Estate by half their Machtbasis/Entrenchment: 100 Machtbasis grants +50% Estate power.
- Governor Estate-power contributions stack additively per Estate and are aggregated into one country modifier for Crown, Nobility, Clergy, Burghers, Peasants, Tribes, Cossacks and Dhimmi.
- Estate-power modifiers are recalculated after the yearly Machtbasis tick and removed immediately when a Governor dies, is dismissed, is replaced or loses their Residence through demolition.
- Voluntarily dismissing a non-Crown Governor now reduces their Estate Satisfaction and the country's Legitimacy in proportion to Machtbasis. At 100 Machtbasis the cost is -25 percentage points Estate Satisfaction and -10 Legitimacy; at 50 it is half that, and at 0 it is free.
- Crown-Estate Governors can be dismissed without Satisfaction or Legitimacy cost.
- Replacing a Governor counts as dismissing the outgoing office holder and pays the same political cost, preventing replacement from bypassing the dismissal mechanic.
- Updated English and German tooltips for Machtbasis, replacement, dismissal and Governor Estate influence.

## 0.2.3

- Added complete German localization for Governor buildings, interactions, selectors, outliner entries, role menu, tooltips and character-role display.
- Replaced the free-standing Governor scripted widget with a native `outliner.gui` integration inside the vanilla outliner scroll container.
- Removed the obsolete floating widget that could appear at the upper-left corner of the screen.
- Vacant and occupied Governor portraits now invoke dedicated generic actions, so clicking the portrait opens the native character chooser for that exact Governor's Residence.
- The portrait chooser retains the shared Cabinet-law eligibility rules introduced in 0.2.2.
- Serving Governors are now displayed as `Governor` / `Gouverneur` in the character view instead of `Courtier` / `Höfling`.
- Added a targeted `character_lateralview.gui` override for the Governor role label; the underlying engine role mask remains non-extensible, while the mod office state is authoritative for Governor gameplay.
- The seamless UI integration now intentionally overrides same-version vanilla `outliner.gui` and `character_lateralview.gui`; UI mods replacing those files require a compatibility patch.

## 0.2.2

- Clicking a vacant Governor portrait in the Governors outliner now opens a native character chooser for that exact Governor's Residence.
- Clicking an occupied Governor portrait opens the same chooser to replace the current office holder, matching the vanilla Cabinet replacement workflow.
- Added a shared Governor candidate trigger so all appointment paths use the same eligibility rules.
- Governor eligibility now mirrors the script-visible vanilla Cabinet legal restrictions for gender and Estate access, including `gender_equality`, male/female Cabinet allow/block modifiers and individually granted Cabinet rights.
- Candidates blocked from Cabinet service are also blocked from governorship.
- Governor-specific exclusivity remains stricter than Cabinet service: candidates must be free from Cabinet duty, military command, exploration and another governorship.
- Replacing a Governor releases the outgoing character and starts the replacement as a Normal Governor with 0 Entrenchment.

## 0.2.1

- Changed the Governor UI from an active-character roster to an office-slot roster keyed by Governor's Residence location.
- Every owned Governor's Residence now appears in the Governors outliner, even when no Governor is appointed.
- Vacant offices render as an empty Cabinet-style slot with the Residence location and a clear `Vacant` state.
- Occupied offices render with a compact Governor portrait, character name, location, Governor role and Entrenchment.
- The header now displays serving Governors / total Governor's Residences.
- Building completion immediately registers a new vacant office; demolition removes the office and vacates a serving Governor.
- The yearly integrity pass rebuilds the complete office map, providing save migration and recovery after ownership/state changes.
- Left-clicking a row opens the Governor's Residence; double-clicking pans to it. The portrait is the office-holder control.
- Right-clicking an occupied row continues to change role or dismiss the Governor.

## 0.2.0

- Added three Governor roles: Normal Governor, Integration Governor and Colonial Governor.
- New appointments default to Normal Governor.
- Integration Governor is selectable only where the dominant culture differs from the owner's culture and grants +25% local pop assimilation speed.
- Colonial Governor is selectable only in overseas locations and grants +0.25 local migration attraction.
- Added country-side Governor roster state for UI consumption and save migration.
- Added Entrenchment (0-100) to serving Governors and mirrored the value on the governed office/location.
- Entrenchment increases yearly by `2 + (ADM + DIP + MIL) / 100`, capped at 100.
- Entrenchment is display-only in 0.2.0; dismissal/rebellion/estate consequences are intentionally deferred.
- Added a dedicated Governor outliner-style scripted widget listing the Governor, governed location, role and Entrenchment.
- Left-clicking a Governor opens the character; right-clicking opens direct actions to change role or dismiss the Governor.
- The Governor UI was initially additive and did not replace the complete vanilla `outliner.gui` file; this approach was replaced by native outliner integration in 0.2.3.

## 0.1.0

- Unified Local and Naval Governor capacity.
- Reworked `local_governor` into Governor's Residence with 50 base Proximity Source.
- Removed road-to-capital and land-vs-maritime placement split.
- Retired the separate `naval_governor` building while preserving its capacity contribution.
- Added character appointment and dismissal interactions.
- Added ADM/DIP/MIL-scaled governor contribution to local Proximity Source.
- Added death cleanup and yearly integrity/ability refresh.
- Added EU5 Workshop metadata and English localization.
