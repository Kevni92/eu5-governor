# Character Governors for Europa Universalis V

Character Governors replaces the split between **Local Governor** and **Naval Governor** buildings with one character-driven provincial administration system.

## Gameplay

- The vanilla `local_governor` building becomes a **Governor's Residence**.
- It can be built in towns, cities and megalopolises without the vanilla road-to-capital or maritime/land-connectivity split.
- Local and Naval Governor capacity are pooled into one shared limit; Lieutenancies still consume that administrative capacity.
- A Residence provides **30 Proximity Source** on its own.
- Every owned Governor's Residence appears as an office slot in the normal EU5 outliner, including vacant offices.
- Appointed Governors contribute `ADM × 0.50` additional Proximity Source.
- New appointments start as **Normal Governor** with 0 Entrenchment.
- Governors can be switched between Normal, Integration and Colonial roles where their territorial requirements are met.
- Serving Governors increase the power of their Estate by half their Entrenchment.
- Voluntary dismissal/replacement of a non-Crown Governor costs Estate Satisfaction and Stability according to Entrenchment; Crown Governors are free to dismiss or replace.
- Death and demolition vacate the office without voluntary-dismissal penalties.
- English and German localization are included.

## Vacancy warning

If at least one owned Governor's Residence has no Governor, the top-bar alert area shows a yellow Governor warning using the Residence building icon.

The country keeps `eu5gov_next_vacant_office` as an explicit Location-scope variable. The warning exists only while that variable is set. Clicking it calls the same `eu5gov_appoint_governor_from_outliner` Generic Action used by a vacant outliner slot and passes the stored Residence as `scope:target_1`, so the player goes directly to the normal eligible-character chooser without first selecting a location.

The next vacancy is selected deterministically by development. After an appointment, dismissal, death, construction, demolition, monthly pulse or yearly repair pass, vacancy state is refreshed immediately.

The alert is implemented as a small GUI wrapper around the vanilla `alert_manager` rather than by replacing the full vanilla alert manager. The native alert list remains engine-backed; the Governor warning is rendered beside it with vanilla `yellow_alert` styling.

## Automatic Governor Appointments

The Governors outliner section contains an optional **Automatic Governor Appointments** checkbox.

When enabled, vacant Governor's Residences are filled automatically. The system does not open the player character selector. It uses the same shared eligibility trigger as manual appointment:

`eu5gov_can_serve_as_governor`

Vacant offices are processed deterministically by development. For each office the best still-eligible character is selected with the Governor AI score:

`ADM + DIP / 5 + MIL / 5`

The assignment itself is centralized in `eu5gov_assign_governor_to_office_effect`, which is shared by manual interaction, outliner appointment and automatic appointment. It initializes the Governor state, busy modifier, office/roster maps, role, Entrenchment, dismissal-cost scale, proximity bonus, role effect, Estate-power refresh and vacancy refresh.

Automatic filling is triggered after relevant lifecycle changes and on the monthly country pulse as a repair/safety net. If no eligible character exists, the Residence remains vacant and the warning stays visible.

The mod intentionally does **not** add a fabricated native `AutomatedSystemsItem`: the same-version GUI exposes engine-known automation system names, but no proven script/database registration path for a new Governors category. The outliner checkbox therefore uses a mod-owned country variable, `eu5gov_auto_appoint_governors`.

## How to use it

1. Build a **Governor's Residence** in an eligible owned location.
2. The Residence appears under **Governors** in the right-side outliner.
3. Click the empty portrait, or click the top-bar vacancy warning, to open the eligible-character chooser directly for a vacant Residence.
4. Select an eligible character.
5. Right-click an occupied office to change Governor role or dismiss the Governor.
6. Enable **Automatic Governor Appointments** in the Governors outliner section if you want eligible characters assigned automatically.

The original **Appoint Governor** character interaction remains available as an alternate path and uses the same eligibility rules.

## Governor eligibility

Governor appointment mirrors the script-visible vanilla Cabinet restrictions before applying Governor-specific exclusivity.

A candidate must be alive, adult and loyal, must not be blocked from Cabinet service, and must belong to an Estate that the country may legally use in the Cabinet. Gender follows the country's Cabinet law, including individual Cabinet-right exceptions.

Governorship is more exclusive than ordinary Cabinet eligibility: the candidate must also be free from an existing Cabinet post, military command, exploration assignment or another governorship.

## Governor roles

### Normal Governor

Default provincial administration role. It retains the standard Governor administration and character-scaled Proximity contribution.

### Integration Governor

- Available only where the governed location's dominant culture differs from the owner's culture.
- Grants **+25% local pop assimilation speed** at the Residence location.

### Colonial Governor

- Available only where `is_overseas_for_owner = yes`.
- Grants the mod's Colonial Governor migration/population effects at the Residence location.

Changing role does not reset Entrenchment.

## Entrenchment

Each serving Governor and the corresponding Residence track the same Entrenchment value from 0 to 100.

Monthly gain:

`(2 + (ADM + DIP + MIL) / 100) / 12`

A serving Governor increases the power of their Estate by half their Entrenchment. At 100 Entrenchment this is +50% Estate power.

For non-Crown Governors, voluntary dismissal or replacement uses a minimum effective dismissal scale of 10 and then scales with Entrenchment. At the minimum this costs -10 Estate Satisfaction and -5 Stability; at 100 it reaches -100 Estate Satisfaction and -50 Stability. Crown Governors are exempt.

Death, demolition and integrity cleanup are not voluntary dismissals and therefore do not pay those costs.

## Governor management UI

The Governors section is integrated directly into the vanilla outliner. Country-side state is maintained with:

- `eu5gov_governor_offices` — all owned Governor's Residence locations.
- `eu5gov_governor_roster` — serving Governors and their Residence locations.
- `eu5gov_next_vacant_office` — the deterministic current target for the vacancy alert.
- `eu5gov_auto_appoint_governors` — whether player Governor automation is enabled.

The header displays serving Governors / total Governor's Residences. Construction and demolition update the office map immediately; the yearly integrity pass rebuilds it for save migration and repair.

## Character role display

EU5's `CharacterRoleMask` is engine-backed and the same-version script/game files expose no supported effect for registering a new custom role in that mask. The mod therefore keeps `eu5gov_governorship` as authoritative gameplay state and displays **Governor / Gouverneur** for office holders in the character view.

## Compatibility

The mod replaces the database objects `local_governor` and `naval_governor`. Mods replacing either building require a compatibility patch.

For seamless UI integration the mod also supplies same-version UI overrides/additions for the outliner, character role display, Governor automation row and alert-manager wrapper. UI mods that replace the same vanilla files or redefine the same GUI types may require a compatibility patch.

The current UI references are based on EU5 1.3.x and should be re-audited after patches that change the relevant vanilla GUI files.

## Installation / Workshop

The repository root is the playable mod root. It includes `.metadata/metadata.json` and can be copied directly into an EU5 mod workspace or used as the source for a Steam Workshop upload.

Target metadata: **EU5 1.3.x**.

## Verification status

The implementation follows same-version EU5 1.3 vanilla/community-tested patterns for building lifecycle hooks, character interactions, Generic Actions with selectors, scripted GUI execution, ordered iterators, scope variables, variable maps exposed to GUI, outliner integration, alert-banner templates, character-death on-actions, monthly/yearly country pulses and Governor eligibility.

The release still needs an exact-patch runtime smoke test with `script_docs`, `dump_data_types`, `error.log` and in-game UI behavior. In particular verify:

- vacancy warning visibility and disappearance;
- warning click opens the selector for the intended Residence;
- `local_governor.dds` resolves correctly in the installed 1.3.x build;
- automation checkbox toggles and persists correctly;
- automatic appointment selects only eligible characters and fills multiple vacancies without reuse;
- no eligible character leaves the vacancy intact without script errors;
- construction, death, dismissal, demolition, monthly pulse and yearly repair all refresh the next-vacancy target correctly.
