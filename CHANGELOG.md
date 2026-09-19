# Changelog

## 0.2.0

- Added three Governor roles: Normal Governor, Integration Governor and Colonial Governor.
- New appointments default to Normal Governor.
- Added country-side Governor roster state for UI consumption and save migration.
- Added Entrenchment (0-100) to serving Governors.
- Entrenchment increases yearly by `2 + (ADM + DIP + MIL) / 100`, capped at 100.
- Entrenchment is display-only in 0.2.0; dismissal/rebellion/estate consequences are intentionally deferred.
- Added a dedicated Governor outliner-style UI listing the Governor, governed location, role and Entrenchment.
- Right-clicking a Governor entry opens direct actions to change role or dismiss the Governor.
- Integration Governors currently add local assimilation speed; Colonial Governors add local migration attraction.

## 0.1.0

- Unified Local and Naval Governor capacity.
- Reworked `local_governor` into Governor's Residence with 50 base Proximity Source.
- Removed road-to-capital and land-vs-maritime placement split.
- Retired the separate `naval_governor` building while preserving its capacity contribution.
- Added character appointment and dismissal interactions.
- Added ADM/DIP/MIL-scaled governor contribution to local Proximity Source.
- Added death cleanup and yearly integrity/ability refresh.
- Added EU5 Workshop metadata and English localization.
