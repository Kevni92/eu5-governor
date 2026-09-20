from pathlib import Path

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8-sig')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    return text.replace(old, new, 1)


def replace_loc_line(text, key, new_line):
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if line.lstrip().startswith(key + ':')]
    if len(matches) != 1:
        raise SystemExit(f'{key}: expected 1 localization line, found {len(matches)}')
    lines[matches[0]] = ' ' + new_line
    return '\n'.join(lines) + '\n'


def insert_loc_after(text, anchor_key, new_lines):
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if line.lstrip().startswith(anchor_key + ':')]
    if len(matches) != 1:
        raise SystemExit(f'{anchor_key}: expected 1 anchor line, found {len(matches)}')
    idx = matches[0] + 1
    lines[idx:idx] = [' ' + line for line in new_lines]
    return '\n'.join(lines) + '\n'

# 1) Component script values for the live monthly Entrenchment breakdown.
values_path = 'in_game/common/script_values/eu5gov_governor_values.txt'
values = read(values_path)
if 'eu5gov_monthly_entrenchment_base_gain' not in values:
    values += '''\n\neu5gov_monthly_entrenchment_base_gain = {\n    value = 2\n    divide = 12\n}\n\neu5gov_monthly_entrenchment_adm_gain = {\n    value = adm\n    divide = 1200\n}\n\neu5gov_monthly_entrenchment_dip_gain = {\n    value = dip\n    divide = 1200\n}\n\neu5gov_monthly_entrenchment_mil_gain = {\n    value = mil\n    divide = 1200\n}\n'''
write(values_path, values)

# 2) Native confirmation before replacement, role changes and dismissal.
actions_path = 'in_game/common/generic_actions/eu5gov_governor_outliner_actions.txt'
actions = read(actions_path)
for action_id in [
    'eu5gov_change_governor_from_outliner',
    'eu5gov_set_role_normal_from_outliner',
    'eu5gov_set_role_integration_from_outliner',
    'eu5gov_set_role_colonial_from_outliner',
    'eu5gov_dismiss_governor_from_outliner',
]:
    marker = f'{action_id} = {{\n\ttype = owncountry\n'
    replacement = f'{action_id} = {{\n\ttype = owncountry\n\tforce_click_and_confirm_or_hold = yes\n'
    if replacement not in actions:
        actions = replace_once(actions, marker, replacement, f'confirm {action_id}')
write(actions_path, actions)

# 3) Occupied portrait: suppress the vanilla Character right-click handler entirely.
outliner_path = 'in_game/gui/outliner.gui'
outliner = read(outliner_path)
occupied_portrait = '''                                portrait_standard_head_button = {\n                                    datacontext = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter]"\n                                    size = { 28 28 }\n                                    alwaystransparent = yes\n                                    blockoverride "character_contextmenu" {}\n                                }\n'''
occupied_portrait_fixed = '''                                portrait_standard_head_button = {\n                                    datacontext = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter]"\n                                    size = { 28 28 }\n                                    alwaystransparent = yes\n                                    blockoverride "character_contextmenu" {}\n                                    blockoverride "rightclick" {}\n                                    blockoverride "portrait_click" {}\n                                }\n'''
if occupied_portrait_fixed not in outliner:
    outliner = replace_once(outliner, occupied_portrait, occupied_portrait_fixed, 'occupied portrait handlers')

# 4) Split the Entrenchment tooltip into spaced, readable sections.
old_tooltip_content = '''                                            blockoverride "tooltip_content" {\n                                                TooltipTextBlock = {\n                                                    blockoverride "text" {\n                                                        text = "EU5GOV_ENTRENCHMENT_TT_DYNAMIC"\n                                                    }\n                                                }\n                                            }\n'''
new_tooltip_content = '''                                            blockoverride "tooltip_content" {\n                                                TooltipTextBlock = {\n                                                    blockoverride "text" {\n                                                        text = "EU5GOV_ENTRENCHMENT_TT_GROWTH"\n                                                    }\n                                                }\n                                                TooltipTextBlock = {\n                                                    blockoverride "text" {\n                                                        text = "EU5GOV_ENTRENCHMENT_TT_EFFECTS"\n                                                    }\n                                                }\n                                                TooltipTextBlock = {\n                                                    blockoverride "text" {\n                                                        text = "EU5GOV_ENTRENCHMENT_TT_DISMISSAL"\n                                                    }\n                                                }\n                                            }\n'''
if new_tooltip_content not in outliner:
    outliner = replace_once(outliner, old_tooltip_content, new_tooltip_content, 'structured entrenchment tooltip')
write(outliner_path, outliner)

# 5) German and English localization. Existing vanilla concepts are nested inside the custom concept.
loc_specs = {
    'main_menu/localization/german/zz_eu5gov_l_german.yml': {
        'growth': 'EU5GOV_ENTRENCHMENT_TT_GROWTH: "#T Monatliches Wachstum#!\\nAktuell: #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_gain\')|2]#!\\n$BULLET$Zeit im Amt: #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_base_gain\')|2]#!\\n$BULLET$@adm![adm|e] ([Character.GetAbility(\'adm\')]): #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_adm_gain\')|2]#!\\n$BULLET$@dip![dip|e] ([Character.GetAbility(\'dip\')]): #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_dip_gain\')|2]#!\\n$BULLET$@mil![mil|e] ([Character.GetAbility(\'mil\')]): #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_mil_gain\')|2]#!"',
        'effects': 'EU5GOV_ENTRENCHMENT_TT_EFFECTS: "#T Politische Auswirkungen#!\\n$BULLET$Die [estate_power|e] des [estate|e] des Gouverneurs steigt je Punkt [eu5gov_entrenchment|e] um #Y 0,5 %#!.\\n$BULLET$Bei 100 Verankerung entspricht das #Y +50 % Standesmacht#!.\\n$BULLET$Die Verankerung kann höchstens #Y 100#! erreichen."',
        'dismissal': 'EU5GOV_ENTRENCHMENT_TT_DISMISSAL: "#T Entlassung und Ersetzung#!\\n$BULLET$Bei Nicht-Kron-Gouverneuren gilt mindestens eine Kostenbasis von #Y 10#!, darüber die aktuelle [eu5gov_entrenchment|e].\\n$BULLET$[estate_satisfaction|e]: #R −max(10, Verankerung)#! Prozentpunkte.\\n$BULLET$[stability|e]: #R −0,5 × max(10, Verankerung)#!.\\n$BULLET$Gouverneure des Kronstandes können ohne diese politischen Kosten entlassen oder ersetzt werden."',
        'concept': 'game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] misst, wie fest ein [eu5gov_governor|e] politisch und administrativ in seinem Amt verankert ist.\\n\\n#T Wachstum#!\\nSie steigt monatlich um #Y (2 + ([adm|e] + [dip|e] + [mil|e]) / 100) / 12#! und ist auf 100 begrenzt.\\n\\n#T Auswirkungen#!\\n$BULLET$Jeder Punkt erhöht die [estate_power|e] des [estate|e] des Gouverneurs um #Y 0,5 %#!.\\n$BULLET$Eine freiwillige Entlassung oder Ersetzung eines Nicht-Kron-Gouverneurs senkt die [estate_satisfaction|e] um mindestens 10 Prozentpunkte beziehungsweise um seine Verankerung, falls diese höher ist.\\n$BULLET$Zusätzlich verliert das Land halb so viel [stability|e].\\n$BULLET$Gouverneure des Kronstandes sind von diesen Entlassungskosten ausgenommen."',
        'replace_title': 'eu5gov_change_governor_from_outliner: "Gouverneur ersetzen"',
        'replace_desc': 'eu5gov_change_governor_from_outliner_desc: "Wählt einen neuen geeigneten Gouverneur. Vor der Ersetzung erscheint eine Bestätigung mit den politischen Kosten des bisherigen Amtsinhabers. Bei Nicht-Kron-Gouverneuren richten sie sich nach seiner [eu5gov_entrenchment|e]; Gouverneure des Kronstandes sind kostenlos zu ersetzen."',
        'dismiss_desc': 'eu5gov_dismiss_governor_from_outliner_desc: "Entlässt den amtierenden Gouverneur. Vor der Entlassung erscheint eine Bestätigung mit den tatsächlichen politischen Auswirkungen auf [estate_satisfaction|e] und [stability|e]. Die Kosten richten sich nach seiner [eu5gov_entrenchment|e]."',
    },
    'main_menu/localization/english/zz_eu5gov_l_english.yml': {
        'growth': 'EU5GOV_ENTRENCHMENT_TT_GROWTH: "#T Monthly Growth#!\\nCurrent: #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_gain\')|2]#!\\n$BULLET$Time in office: #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_base_gain\')|2]#!\\n$BULLET$@adm![adm|e] ([Character.GetAbility(\'adm\')]): #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_adm_gain\')|2]#!\\n$BULLET$@dip![dip|e] ([Character.GetAbility(\'dip\')]): #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_dip_gain\')|2]#!\\n$BULLET$@mil![mil|e] ([Character.GetAbility(\'mil\')]): #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_mil_gain\')|2]#!"',
        'effects': 'EU5GOV_ENTRENCHMENT_TT_EFFECTS: "#T Political Effects#!\\n$BULLET$The Governor\'s [estate|e] gains #Y +0.5% [estate_power|e]#! for each point of [eu5gov_entrenchment|e].\\n$BULLET$At 100 Entrenchment this is #Y +50% Estate Power#!.\\n$BULLET$Entrenchment is capped at #Y 100#!."',
        'dismissal': 'EU5GOV_ENTRENCHMENT_TT_DISMISSAL: "#T Dismissal and Replacement#!\\n$BULLET$For non-Crown Governors, the cost scale is at least #Y 10#! and otherwise their current [eu5gov_entrenchment|e].\\n$BULLET$[estate_satisfaction|e]: #R −max(10, Entrenchment)#! percentage points.\\n$BULLET$[stability|e]: #R −0.5 × max(10, Entrenchment)#!.\\n$BULLET$Crown Estate Governors can be dismissed or replaced without these political costs."',
        'concept': 'game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] measures how firmly a [eu5gov_governor|e] is politically and administratively established in office.\\n\\n#T Growth#!\\nIt rises monthly by #Y (2 + ([adm|e] + [dip|e] + [mil|e]) / 100) / 12#! and is capped at 100.\\n\\n#T Effects#!\\n$BULLET$Each point increases the [estate_power|e] of the Governor\'s [estate|e] by #Y 0.5%#!.\\n$BULLET$Voluntarily dismissing or replacing a non-Crown Governor reduces [estate_satisfaction|e] by at least 10 percentage points or by their Entrenchment if higher.\\n$BULLET$The country also loses half as much [stability|e].\\n$BULLET$Crown Estate Governors are exempt from these dismissal costs."',
        'replace_title': 'eu5gov_change_governor_from_outliner: "Change Governor"',
        'replace_desc': 'eu5gov_change_governor_from_outliner_desc: "Choose a new eligible Governor. A confirmation dialog shows the outgoing office holder\'s political costs before replacement. For non-Crown Governors these depend on their [eu5gov_entrenchment|e]; Crown Estate Governors are free to replace."',
        'dismiss_desc': 'eu5gov_dismiss_governor_from_outliner_desc: "Dismiss the serving Governor. A confirmation dialog shows the actual effects on [estate_satisfaction|e] and [stability|e] before dismissal. The cost depends on their [eu5gov_entrenchment|e]."',
    },
}

for path, spec in loc_specs.items():
    loc = read(path)
    if 'EU5GOV_ENTRENCHMENT_TT_GROWTH:' not in loc:
        loc = insert_loc_after(loc, 'EU5GOV_ENTRENCHMENT_TT_DYNAMIC', [spec['growth'], spec['effects'], spec['dismissal']])
    else:
        loc = replace_loc_line(loc, 'EU5GOV_ENTRENCHMENT_TT_GROWTH', spec['growth'])
        loc = replace_loc_line(loc, 'EU5GOV_ENTRENCHMENT_TT_EFFECTS', spec['effects'])
        loc = replace_loc_line(loc, 'EU5GOV_ENTRENCHMENT_TT_DISMISSAL', spec['dismissal'])
    loc = replace_loc_line(loc, 'game_concept_eu5gov_entrenchment_desc', spec['concept'])
    if 'eu5gov_change_governor_from_outliner:' not in loc:
        loc = insert_loc_after(loc, 'EU5GOV_PORTRAIT_CHANGE_DESC', [spec['replace_title'], spec['replace_desc']])
    else:
        loc = replace_loc_line(loc, 'eu5gov_change_governor_from_outliner', spec['replace_title'])
        loc = replace_loc_line(loc, 'eu5gov_change_governor_from_outliner_desc', spec['replace_desc'])
    loc = replace_loc_line(loc, 'eu5gov_dismiss_governor_from_outliner_desc', spec['dismiss_desc'])
    write(path, loc)

# 6) README corrections relevant to the now-monthly mechanic.
readme_path = 'README.md'
readme = read(readme_path)
readme = readme.replace(
    '- A yearly integrity pass refreshes bonuses, Machtbasis, Estate-power contributions, the complete Governor-office roster and stale assignments.',
    '- A monthly pulse advances Entrenchment and refreshes Estate-power contributions; a yearly integrity pass repairs bonuses, the complete Governor-office roster and stale assignments.'
)
readme = readme.replace(
    'Entrenchment advances once per yearly country pulse using:\n\n`2 + (ADM + DIP + MIL) / 100`',
    'Entrenchment advances every monthly country pulse using:\n\n`(2 + (ADM + DIP + MIL) / 100) / 12`'
)
readme = readme.replace('+2.9 per year.', '+0.24 per month (about +2.9 per year).')
readme = readme.replace('+3.5 per year.', '+0.29 per month (about +3.5 per year).')
readme = readme.replace('+5.0 per year.', '+0.42 per month (about +5.0 per year).')
write(readme_path, readme)

# 7) Version and changelog.
metadata_path = '.metadata/metadata.json'
metadata = read(metadata_path)
if '"version": "0.2.10"' not in metadata:
    metadata = replace_once(metadata, '"version": "0.2.9"', '"version": "0.2.10"', 'metadata version')
write(metadata_path, metadata)

changelog_path = 'CHANGELOG.md'
changelog = read(changelog_path)
entry = '''## 0.2.10\n\n- Fixed the occupied Governor portrait's vanilla right-click handler, which was opening an empty Character context menu after the context-menu contents had been suppressed.\n- Right-clicking an occupied Governor portrait now reaches the Governor dismissal action cleanly.\n- Added native EU5 confirmation dialogs to Governor replacement, voluntary dismissal and all three Governor role changes via `force_click_and_confirm_or_hold`.\n- Confirmation dialogs use the Generic Action effect preview so the action's actual political/stability effects are shown before committing.\n- Split the Entrenchment tooltip into Monthly Growth, Political Effects, and Dismissal/Replacement sections.\n- Added live component breakdowns for the base, ADM, DIP and MIL contributions to monthly Entrenchment growth.\n- Entrenchment tooltips and the Game Concept now link vanilla concepts for ADM, DIP, MIL, Estate, Estate Power, Estate Satisfaction and Stability.\n\n'''
if '## 0.2.10' not in changelog:
    changelog = changelog.replace('# Changelog\n\n', '# Changelog\n\n' + entry, 1)
write(changelog_path, changelog)

print('Governor 0.2.10 patch applied successfully')
