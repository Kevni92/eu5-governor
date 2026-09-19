# Changelog

## 0.2.1

- Changed the Governor UI from an active-character roster to an office-slot roster keyed by Governor's Residence location.
- Every owned Governor's Residence now appears in the Governors outliner, even when no Governor is appointed.
- Vacant offices render as an empty Cabinet-style slot with the Residence location and a clear `Vacant` state.
- Occupied offices render with a compact Governor portrait, character name, location, Governor role and Entrenchment.
- The header now displays serving Governors / total Governor's Residences.
- Building completion immediately registers a new vacant office; demolition removes the office and vacates a serving Governor.
- The yearly integrity pass rebuilds the complete office map, providing save migration and recovery after ownership/state changes.
- Left-clicking a row opens the Governor's Residence; double-clicking pans to it. The character portrait keeps standard character behavior.
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
- The Governor UI is additive and does not replace the complete vanilla `outliner.gui` file.

## 0.1.0

- Unified Local and Naval Governor capacity.
- Reworked `local_governor` into Governor's Residence with 50 base Proximity Source.
- Removed road-to-capital and land-vs-maritime placement split.
- Retired the separate `naval_governor` building while preserving its capacity contribution.
- Added character appointment and dismissal interactions.
- Added ADM/DIP/MIL-scaled governor contribution to local Proximity Source.
- Added death cleanup and yearly integrity/ability refresh.
- Added EU5 Workshop metadata and English localization.
