# Changelog

## 0.2.7

- Added a 10% minimum political dismissal floor for non-Crown Governors: at 0-10 Entrenchment dismissal/replacement costs -10 Estate Satisfaction and -5 Stability; from 10 to 100 it scales linearly to -100/-50.
- Added the required `STATIC_MODIFIER_NAME_*`/`STATIC_MODIFIER_DESC_*` localization for Governor administration and role modifiers.
- Governor outliner now follows the native `Outliner.IsExpanded` state and disappears with the collapsed vanilla outliner instead of remaining full width.
- Restyled the Governors header with the vanilla gold category frame, count box and round expand/collapse arrow.
- Reduced Governor office rows to a 95%-width, 30px vanilla-like footprint.
- Replaced free-form row tooltips with standard functional action tooltips.
- Role context-menu tooltips now use a short title plus a detailed description containing the actual gameplay effects.
- Added Game Concepts for Governor, Provincial Governor, Integration Governor, Colonial Governor and Entrenchment in English and German.

## 0.2.6

- Fixed Governor role switching from the outliner context menu by removing the fragile character-scoped `ScriptedGui.IsValid` bridge.
- Role and dismissal actions now receive the Governor's Residence directly as saved `office` scope and resolve the serving Governor from that authoritative office state.
- Context-menu buttons determine their enabled state directly from the office role variable; the currently active role remains disabled.
- The scripted GUI actions themselves remain executable and enforce Integration/Colonial territorial requirements inside their effects.

## 0.2.5

- Reduced Governor's Residence base Proximity Source from 50 to 30.
- Governor Proximity contribution now scales only from ADM at `ADM × 0.50`; 100 ADM adds +50 for a maximum Residence total of 80.
- Voluntary dismissal/replacement of a non-Crown Governor now scales up to -100 percentage points Estate Satisfaction and -50 Stability at 100 Entrenchment; 50 Entrenchment costs half.
- Crown Governors remain free to dismiss or replace.
- German `Machtbasis` terminology renamed to `Verankerung`; English remains `Entrenchment`.
- Colonial Governors now also grant +0.001 local population growth in addition to migration attraction.

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
- Clicking an occupied Governor portrait opens the same chooser to replace the current office holder, matching the vanilla Cabinet slot workflow.
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
