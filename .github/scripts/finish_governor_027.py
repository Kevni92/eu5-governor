from pathlib import Path
import json


def read(path):
    return Path(path).read_text(encoding='utf-8-sig')


def write_bom(path, text):
    Path(path).write_text('\ufeff' + text, encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one match, found {count}')
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# German localization
# ---------------------------------------------------------------------------
p = 'main_menu/localization/german/zz_eu5gov_l_german.yml'
t = read(p)

t = replace_once(
    t,
    ' eu5gov_dismiss_governor_desc: "Entfernt einen Gouverneur aus seinem Amt. Bei Nicht-Kron-Gouverneuren skalieren Standeszufriedenheit und Legitimitätskosten mit der Verankerung: Bei 100 Verankerung verliert sein Stand 100 Prozentpunkte Zufriedenheit und das Land 50 Stabilität. Kron-Gouverneure können kostenlos entlassen werden."',
    ' eu5gov_dismiss_governor_desc: "Entfernt einen Gouverneur aus seinem Amt. Bei Nicht-Kron-Gouverneuren betragen die politischen Kosten mindestens #R -10 Standeszufriedenheit#! und #R -5 Stabilität#!. Oberhalb von 10 Verankerung skalieren sie linear: 50 Verankerung kosten -50 Zufriedenheit und -25 Stabilität; 100 Verankerung kosten -100 Zufriedenheit und -50 Stabilität. Kron-Gouverneure können kostenlos entlassen werden."',
    'german dismissal desc',
)

t = replace_once(
    t,
    ' EU5GOV_OUTLINER_HEADER_TT: "Gouverneursposten. Aufgeführt werden alle eigenen Gouverneursresidenzen, einschließlich unbesetzter Ämter. Der Zähler zeigt amtierende Gouverneure / gesamte Gouverneursresidenzen. Klickt auf die Überschrift, um die Liste ein- oder auszuklappen."',
    ' EU5GOV_OUTLINER_HEADER_TT: "Verwaltet Eure [eu5gov_governor|e]. Aufgeführt werden alle eigenen Gouverneursresidenzen, einschließlich unbesetzter Ämter. Der Zähler zeigt amtierende Gouverneure / gesamte Gouverneursresidenzen. Klickt auf die Überschrift, um die Liste ein- oder auszuklappen."',
    'german outliner header',
)

t = replace_once(
    t,
    ' EU5GOV_OUTLINER_RIGHT_CLICK: "Gouverneur verwalten"',
    ' EU5GOV_OUTLINER_RIGHT_CLICK: "Gouverneur verwalten"\n EU5GOV_OUTLINER_RIGHT_CLICK_DESC: "Ändert die Amtsausrichtung dieses [eu5gov_governor|e] oder entlasst ihn."',
    'german outliner right click',
)

t = replace_once(
    t,
    ' EU5GOV_EMPTY_SLOT_TT: "Diese Gouverneursresidenz hat keinen Gouverneur. Klickt auf das leere Porträt, um einen geeigneten Gouverneur auszuwählen. Ein Klick auf den restlichen Eintrag öffnet den Ort."',
    ' EU5GOV_EMPTY_SLOT_TT: "Diese Gouverneursresidenz hat keinen [eu5gov_governor|e]. Klickt auf das leere Porträt, um einen geeigneten Charakter auszuwählen. Die Residenz selbst liefert #G 30#! Nähequelle; ein Gouverneur ergänzt #G ADM × 0,50#!."',
    'german empty slot tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_OCCUPIED_SLOT_TT: "Diese Gouverneursresidenz ist besetzt. Klickt auf das Porträt, um den Gouverneur zu ersetzen; ein Klick auf den restlichen Eintrag öffnet den Ort; per Rechtsklick könnt Ihr Amtsausrichtung oder Entlassung verwalten."',
    ' EU5GOV_OCCUPIED_SLOT_TT: "Dieser [eu5gov_governor|e] verwaltet die Gouverneursresidenz. Die Residenz liefert #G 30#! Nähequelle und der Gouverneur zusätzlich #G ADM × 0,50#!. Klickt auf das Porträt zum Ersetzen; Rechtsklick öffnet Amtsausrichtung und Entlassung."',
    'german occupied slot tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ROLE_NORMAL_TT: "Überträgt die allgemeine Provinzverwaltung. Dies ist die Standardausrichtung für Kern- und Heimatgebiete. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
    ' EU5GOV_ROLE_NORMAL_TT: "[eu5gov_provincial_governor|E]: allgemeine Provinzverwaltung ohne zusätzlichen Spezialmodifikator. Der Gouverneur behält den Grundeffekt von #G ADM × 0,50#! Nähequelle zusätzlich zu den #G 30#! der Residenz. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
    'german normal role tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ROLE_INTEGRATION_TT: "Überträgt die Integrationsverwaltung. Sie ist verfügbar, wenn die vorherrschende Kultur des Gouverneurssitzes von der Kultur des Besitzers abweicht, und gewährt #G +25 %#! lokale Assimilationsgeschwindigkeit. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
    ' EU5GOV_ROLE_INTEGRATION_TT: "[eu5gov_integration_governor_role|E]: verfügbar, wenn die vorherrschende Kultur des Gouverneurssitzes von der Kultur des Besitzers abweicht. Gewährt am Sitz #G +25 % lokale Assimilationsgeschwindigkeit#! und behält den normalen ADM-basierten Nähebonus. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
    'german integration role tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ROLE_COLONIAL_TT: "Überträgt die Kolonialverwaltung. Sie ist nur in überseeischen Gebieten verfügbar und gewährt #G +0,25#! lokale Migrationsattraktivität und #G +0,001#! lokales Bevölkerungswachstum. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
    ' EU5GOV_ROLE_COLONIAL_TT: "[eu5gov_colonial_governor_role|E]: nur in überseeischen Gebieten verfügbar. Gewährt am Sitz #G +0,25 lokale Migrationsattraktivität#! und #G +0,001 lokales Bevölkerungswachstum#! zusätzlich zum normalen ADM-basierten Nähebonus. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
    'german colonial role tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_DISMISS_TT: "Entlasst diesen Gouverneur. Bei einem Nicht-Kron-Gouverneur skalieren die Kosten linear mit der Verankerung: Bei 100 verliert sein Stand #R 100 Prozentpunkte Zufriedenheit#! und das Land #R 50 Stabilität#!. Kron-Gouverneure können kostenlos entlassen werden."',
    ' EU5GOV_DISMISS_TT: "Entlasst diesen [eu5gov_governor|e]. Nicht-Kron-Gouverneure kosten mindestens #R -10 Standeszufriedenheit#! und #R -5 Stabilität#!. Ab 10 [eu5gov_entrenchment|e] skaliert der Preis linear bis #R -100 Zufriedenheit#! und #R -50 Stabilität#! bei 100. Kron-Gouverneure sind kostenlos."',
    'german dismiss tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ENTRENCHMENT_TT: "Die Verankerung beschreibt, wie fest der Gouverneur ein persönliches Verwaltungsnetzwerk aufgebaut hat. Sie steigt jährlich um #Y 2 + (ADM + DIP + MIL) / 100#! bis maximal 100. Jeder Gouverneur erhöht die Macht seines Standes um die Hälfte seiner Verankerung: 100 Verankerung bedeuten #Y +50 % Standesmacht#!. Außerdem bestimmt sie bei Nicht-Kron-Gouverneuren die Kosten einer freiwilligen Entlassung oder Ersetzung."',
    ' EU5GOV_ENTRENCHMENT_TT: "[eu5gov_entrenchment|E] steigt jährlich um #Y 2 + (ADM + DIP + MIL) / 100#! bis maximal 100. Ein Gouverneur erhöht die Macht seines Standes um die Hälfte seiner Verankerung: 100 bedeuten #Y +50 % Standesmacht#!. Bei Nicht-Kron-Gouverneuren bestimmt sie außerdem die Entlassungskosten; diese haben immer mindestens den 10-%-Sockel."',
    'german entrenchment tooltip',
)

if ' STATIC_MODIFIER_NAME_eu5gov_governor_administration:' not in t:
    anchor = ' eu5gov_colonial_governor_desc: "Dieser Gouverneur ist mit der Entwicklung eines überseeischen Besitzes betraut und gewährt #G +0,25#! lokale Migrationsattraktivität und #G +0,001#! lokales Bevölkerungswachstum."\n'
    block = '''\n STATIC_MODIFIER_NAME_eu5gov_governor_administration: "Gouverneursverwaltung"\n STATIC_MODIFIER_DESC_eu5gov_governor_administration: "Die Verwaltungsfähigkeit des amtierenden Gouverneurs erhöht die lokale Nähequelle."\n STATIC_MODIFIER_NAME_eu5gov_integration_governor: "Integrationsverwaltung"\n STATIC_MODIFIER_DESC_eu5gov_integration_governor: "Der Integrationsgouverneur beschleunigt die lokale kulturelle Assimilation."\n STATIC_MODIFIER_NAME_eu5gov_colonial_governor: "Kolonialverwaltung"\n STATIC_MODIFIER_DESC_eu5gov_colonial_governor: "Der Kolonialgouverneur fördert Migration und Bevölkerungswachstum am Gouverneurssitz."\n STATIC_MODIFIER_NAME_eu5gov_governor_crown_estate_power: "Gouverneurseinfluss: Krone"\n STATIC_MODIFIER_NAME_eu5gov_governor_nobles_estate_power: "Gouverneurseinfluss: Adel"\n STATIC_MODIFIER_NAME_eu5gov_governor_clergy_estate_power: "Gouverneurseinfluss: Klerus"\n STATIC_MODIFIER_NAME_eu5gov_governor_burghers_estate_power: "Gouverneurseinfluss: Bürger"\n STATIC_MODIFIER_NAME_eu5gov_governor_peasants_estate_power: "Gouverneurseinfluss: Bauern"\n STATIC_MODIFIER_NAME_eu5gov_governor_tribes_estate_power: "Gouverneurseinfluss: Stämme"\n STATIC_MODIFIER_NAME_eu5gov_governor_cossacks_estate_power: "Gouverneurseinfluss: Kosaken"\n STATIC_MODIFIER_NAME_eu5gov_governor_dhimmi_estate_power: "Gouverneurseinfluss: Dhimmi"\n'''
    t = replace_once(t, anchor, anchor + block, 'german static modifier loc insert')

if ' game_concept_eu5gov_governor:' not in t:
    t += '''\n\n game_concept_eu5gov_governor: "Gouverneur"\n game_concept_eu5gov_governor_desc: "Ein [eu5gov_governor|E] ist ein Charakter, der eine Gouverneursresidenz verwaltet. Die Residenz stellt #G 30 Nähequelle#! bereit; der Gouverneur ergänzt #G 0,50 Nähequelle je ADM#!, sodass 100 ADM weitere +50 und insgesamt 80 ergeben. Jeder Gouverneur besitzt außerdem [eu5gov_entrenchment|e] und eine Amtsausrichtung."\n game_concept_eu5gov_provincial_governor: "Provinzgouverneur"\n game_concept_eu5gov_provincial_governor_desc: "Der [eu5gov_provincial_governor|E] ist die allgemeine Verwaltungsrolle. Er besitzt keinen zusätzlichen Spezialmodifikator und konzentriert sich auf den normalen ADM-basierten Nähebonus der Gouverneursresidenz."\n game_concept_eu5gov_integration_governor_role: "Integrationsgouverneur"\n game_concept_eu5gov_integration_governor_role_desc: "Der [eu5gov_integration_governor_role|E] kann an einem Gouverneurssitz mit fremder vorherrschender Kultur eingesetzt werden. Er gewährt dort #G +25 % lokale Assimilationsgeschwindigkeit#! zusätzlich zum normalen Gouverneurs-Nähebonus."\n game_concept_eu5gov_colonial_governor_role: "Kolonialgouverneur"\n game_concept_eu5gov_colonial_governor_role_desc: "Der [eu5gov_colonial_governor_role|E] ist für überseeische Gouverneurssitze bestimmt. Er gewährt dort #G +0,25 lokale Migrationsattraktivität#! und #G +0,001 lokales Bevölkerungswachstum#! zusätzlich zum normalen Gouverneurs-Nähebonus."\n game_concept_eu5gov_entrenchment: "Verankerung"\n game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] misst die politische und administrative Verfestigung eines Gouverneurs von 0 bis 100. Sie steigt jährlich um #Y 2 + (ADM + DIP + MIL) / 100#!. Jeder Gouverneur erhöht die Macht seines Standes um die Hälfte seiner Verankerung. Bei einer freiwilligen Entlassung oder Ersetzung eines Nicht-Kron-Gouverneurs gilt als Kostenwert mindestens 10 und ansonsten seine Verankerung: daraus entstehen gleich viele negative Prozentpunkte Standeszufriedenheit und halb so viel negative Stabilität. Kron-Gouverneure sind davon ausgenommen."\n'''

write_bom(p, t)


# ---------------------------------------------------------------------------
# English localization
# ---------------------------------------------------------------------------
p = 'main_menu/localization/english/zz_eu5gov_l_english.yml'
t = read(p)

t = replace_once(
    t,
    ' eu5gov_dismiss_governor_desc: "Remove a Governor from office. Non-Crown Governors cost Estate Satisfaction and Stability in proportion to Entrenchment: at 100 Entrenchment the Governor\'s Estate loses 100 percentage points of Satisfaction and the country loses 50 Stability. Crown Governors are free to dismiss."',
    ' eu5gov_dismiss_governor_desc: "Remove a Governor from office. Non-Crown Governors always cost at least #R -10 Estate Satisfaction#! and #R -5 Stability#!. Above 10 Entrenchment the cost scales linearly: 50 Entrenchment costs -50 Satisfaction and -25 Stability; 100 Entrenchment costs -100 Satisfaction and -50 Stability. Crown Governors are free to dismiss."',
    'english dismissal desc',
)

t = replace_once(
    t,
    ' EU5GOV_OUTLINER_HEADER_TT: "Governor offices. Every owned Governor\'s Residence is listed, including vacant residences. The counter shows serving Governors / total Residences. Click the header to collapse or expand the list."',
    ' EU5GOV_OUTLINER_HEADER_TT: "Manage your [eu5gov_governor|e] offices. Every owned Governor\'s Residence is listed, including vacant residences. The counter shows serving Governors / total Residences. Click the header to collapse or expand the list."',
    'english outliner header',
)

t = replace_once(
    t,
    ' EU5GOV_OUTLINER_RIGHT_CLICK: "Manage Governor"',
    ' EU5GOV_OUTLINER_RIGHT_CLICK: "Manage Governor"\n EU5GOV_OUTLINER_RIGHT_CLICK_DESC: "Change this [eu5gov_governor|e] role or dismiss the office holder."',
    'english outliner right click',
)

t = replace_once(
    t,
    ' EU5GOV_EMPTY_SLOT_TT: "This Governor\'s Residence has no Governor. Click the empty portrait to choose an eligible Governor. Left-click elsewhere on the row opens the location."',
    ' EU5GOV_EMPTY_SLOT_TT: "This Governor\'s Residence has no [eu5gov_governor|e]. Click the empty portrait to choose an eligible character. The Residence itself supplies #G 30#! Proximity Source; an appointed Governor adds #G ADM × 0.50#!."',
    'english empty slot tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_OCCUPIED_SLOT_TT: "This Governor\'s Residence is occupied. Click the portrait to replace the Governor; left-click elsewhere on the row opens the location; right-click the row to change Governor type or dismiss the Governor."',
    ' EU5GOV_OCCUPIED_SLOT_TT: "This [eu5gov_governor|e] administers the Governor\'s Residence. The Residence supplies #G 30#! Proximity Source and the Governor adds #G ADM × 0.50#!. Click the portrait to replace them; right-click for role and dismissal options."',
    'english occupied slot tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ROLE_NORMAL_TT: "Assign the normal provincial administration role. This is the default role for governing core territories. The currently active role cannot be selected again."',
    ' EU5GOV_ROLE_NORMAL_TT: "[eu5gov_provincial_governor|E]: general provincial administration with no additional specialist modifier. The Governor retains the base #G ADM × 0.50#! Proximity contribution on top of the Residence\'s #G 30#!. The active role cannot be selected again."',
    'english normal role tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ROLE_INTEGRATION_TT: "Assign the integration role. It is available when the Governor\'s location has a different dominant culture from its owner and grants #G +25%#! local assimilation speed. The currently active role cannot be selected again."',
    ' EU5GOV_ROLE_INTEGRATION_TT: "[eu5gov_integration_governor_role|E]: available when the Governor seat has a different dominant culture from its owner. Grants #G +25% local assimilation speed#! at the seat in addition to the normal ADM-based Proximity contribution. The active role cannot be selected again."',
    'english integration role tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ROLE_COLONIAL_TT: "Assign the colonial role. It is available only in an overseas location and grants #G +0.25#! local migration attraction and #G +0.001#! local population growth. The currently active role cannot be selected again."',
    ' EU5GOV_ROLE_COLONIAL_TT: "[eu5gov_colonial_governor_role|E]: available only at overseas Governor seats. Grants #G +0.25 local migration attraction#! and #G +0.001 local population growth#! at the seat in addition to the normal ADM-based Proximity contribution. The active role cannot be selected again."',
    'english colonial role tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_DISMISS_TT: "Dismiss this Governor. For a non-Crown Governor, the cost scales linearly with Entrenchment: at 100, their Estate loses #R 100 percentage points#! of Satisfaction and the country loses #R 50 Stability#!. Crown Governors can be dismissed for free."',
    ' EU5GOV_DISMISS_TT: "Dismiss this [eu5gov_governor|e]. Non-Crown Governors cost at least #R -10 Estate Satisfaction#! and #R -5 Stability#!. From 10 [eu5gov_entrenchment|e] upward the price scales linearly to #R -100 Satisfaction#! and #R -50 Stability#! at 100. Crown Governors are free."',
    'english dismiss tooltip',
)

t = replace_once(
    t,
    ' EU5GOV_ENTRENCHMENT_TT: "Entrenchment measures how firmly this Governor has established a personal administrative network. It rises yearly by #Y 2 + (ADM + DIP + MIL) / 100#!, up to 100. A Governor increases the power of their Estate by half their Entrenchment: 100 Entrenchment means #Y +50% Estate power#!. It also determines voluntary dismissal/replacement costs for non-Crown Governors."',
    ' EU5GOV_ENTRENCHMENT_TT: "[eu5gov_entrenchment|E] rises yearly by #Y 2 + (ADM + DIP + MIL) / 100#!, up to 100. A Governor increases the power of their Estate by half their Entrenchment: 100 means #Y +50% Estate power#!. It also determines voluntary dismissal/replacement costs for non-Crown Governors, with a permanent 10% minimum floor."',
    'english entrenchment tooltip',
)

if ' STATIC_MODIFIER_NAME_eu5gov_governor_administration:' not in t:
    anchor = ' eu5gov_colonial_governor_desc: "This Governor is tasked with developing an overseas possession and grants #G +0.25#! local migration attraction and #G +0.001#! local population growth."\n'
    block = '''\n STATIC_MODIFIER_NAME_eu5gov_governor_administration: "Governor Administration"\n STATIC_MODIFIER_DESC_eu5gov_governor_administration: "The serving Governor's Administrative ability increases this location's Proximity Source."\n STATIC_MODIFIER_NAME_eu5gov_integration_governor: "Integration Administration"\n STATIC_MODIFIER_DESC_eu5gov_integration_governor: "The Integration Governor accelerates local cultural assimilation."\n STATIC_MODIFIER_NAME_eu5gov_colonial_governor: "Colonial Administration"\n STATIC_MODIFIER_DESC_eu5gov_colonial_governor: "The Colonial Governor promotes migration and population growth at the Governor seat."\n STATIC_MODIFIER_NAME_eu5gov_governor_crown_estate_power: "Governor Influence: Crown"\n STATIC_MODIFIER_NAME_eu5gov_governor_nobles_estate_power: "Governor Influence: Nobility"\n STATIC_MODIFIER_NAME_eu5gov_governor_clergy_estate_power: "Governor Influence: Clergy"\n STATIC_MODIFIER_NAME_eu5gov_governor_burghers_estate_power: "Governor Influence: Burghers"\n STATIC_MODIFIER_NAME_eu5gov_governor_peasants_estate_power: "Governor Influence: Peasants"\n STATIC_MODIFIER_NAME_eu5gov_governor_tribes_estate_power: "Governor Influence: Tribes"\n STATIC_MODIFIER_NAME_eu5gov_governor_cossacks_estate_power: "Governor Influence: Cossacks"\n STATIC_MODIFIER_NAME_eu5gov_governor_dhimmi_estate_power: "Governor Influence: Dhimmi"\n'''
    t = replace_once(t, anchor, anchor + block, 'english static modifier loc insert')

if ' game_concept_eu5gov_governor:' not in t:
    t += '''\n\n game_concept_eu5gov_governor: "Governor"\n game_concept_eu5gov_governor_desc: "A [eu5gov_governor|E] is a character appointed to administer a Governor's Residence. The Residence provides #G 30 Proximity Source#!; the Governor adds #G 0.50 Proximity Source per ADM#!, so 100 ADM adds another +50 for a total of 80. Every Governor also has [eu5gov_entrenchment|e] and a Governor role."\n game_concept_eu5gov_provincial_governor: "Provincial Governor"\n game_concept_eu5gov_provincial_governor_desc: "The [eu5gov_provincial_governor|E] is the general administrative role. It has no additional specialist modifier and focuses on the normal ADM-based Proximity contribution of the Governor's Residence."\n game_concept_eu5gov_integration_governor_role: "Integration Governor"\n game_concept_eu5gov_integration_governor_role_desc: "The [eu5gov_integration_governor_role|E] can be assigned at a Governor seat whose dominant culture differs from the owner's culture. It grants #G +25% local assimilation speed#! there in addition to the normal Governor Proximity contribution."\n game_concept_eu5gov_colonial_governor_role: "Colonial Governor"\n game_concept_eu5gov_colonial_governor_role_desc: "The [eu5gov_colonial_governor_role|E] is intended for overseas Governor seats. It grants #G +0.25 local migration attraction#! and #G +0.001 local population growth#! there in addition to the normal Governor Proximity contribution."\n game_concept_eu5gov_entrenchment: "Entrenchment"\n game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] measures a Governor's political and administrative entrenchment from 0 to 100. It rises yearly by #Y 2 + (ADM + DIP + MIL) / 100#!. Each Governor increases their Estate's power by half their Entrenchment. Voluntarily dismissing or replacing a non-Crown Governor uses a minimum cost scale of 10 and otherwise their Entrenchment: the Estate loses that many percentage points of Satisfaction and the country loses half as much Stability. Crown Governors are exempt."\n'''

write_bom(p, t)


# Metadata version.
p = '.metadata/metadata.json'
data = json.loads(read(p))
data['version'] = '0.2.7'
Path(p).write_text('\ufeff' + json.dumps(data, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')


# Changelog entry.
p = 'CHANGELOG.md'
t = Path(p).read_text(encoding='utf-8')
if '## 0.2.7' not in t:
    entry = '''## 0.2.7\n\n- Added a 10% minimum political dismissal floor for non-Crown Governors: at 0-10 Entrenchment dismissal/replacement costs -10 Estate Satisfaction and -5 Stability; from 10 to 100 it scales linearly to -100/-50.\n- Added the required `STATIC_MODIFIER_NAME_*`/`STATIC_MODIFIER_DESC_*` localization for Governor administration and role modifiers.\n- Governor outliner now follows the native `Outliner.IsExpanded` state and disappears with the collapsed vanilla outliner instead of remaining full width.\n- Restyled the Governors header with the vanilla gold category frame, count box and round expand/collapse arrow.\n- Reduced Governor office rows to a 95%-width, 30px vanilla-like footprint.\n- Replaced free-form row tooltips with standard functional action tooltips.\n- Role context-menu tooltips now use a short title plus a detailed description containing the actual gameplay effects.\n- Added Game Concepts for Governor, Provincial Governor, Integration Governor, Colonial Governor and Entrenchment in English and German.\n\n'''
    t = t.replace('# Changelog\n\n', '# Changelog\n\n' + entry, 1)
    Path(p).write_text(t, encoding='utf-8')
