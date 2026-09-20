from pathlib import Path

ROOT = Path('.')

def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8-sig')

def replace_once(text, old, new, label):
    c = text.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 match, found {c}')
    return text.replace(old, new, 1)

def replace_loc_line(text, key, new_line):
    lines = text.splitlines()
    idxs = [i for i,l in enumerate(lines) if l.lstrip().startswith(key + ':')]
    if len(idxs) != 1:
        raise SystemExit(f'{key}: expected 1 localization line, found {len(idxs)}')
    lines[idxs[0]] = ' ' + new_line
    return '\n'.join(lines) + '\n'

def append_after_key(text, key, lines_to_add):
    if all((ln.split(':',1)[0].strip()+':') in text for ln in lines_to_add):
        return text
    lines = text.splitlines()
    idxs = [i for i,l in enumerate(lines) if l.lstrip().startswith(key + ':')]
    if len(idxs) != 1:
        raise SystemExit(f'{key}: anchor not unique')
    lines[idxs[0]+1:idxs[0]+1] = [' ' + ln for ln in lines_to_add]
    return '\n'.join(lines) + '\n'

def find_matching_brace(text, open_pos):
    depth = 0
    in_string = False
    esc = False
    for i in range(open_pos, len(text)):
        ch = text[i]
        if in_string:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return i
    raise SystemExit('unmatched brace')

def replace_action_effect(text, action_id, new_effect):
    start = text.index(action_id + ' = {')
    open_action = text.index('{', start)
    end = find_matching_brace(text, open_action)
    block = text[start:end+1]
    marker = '\n\teffect = {'
    ep = block.index(marker) + 1
    open_eff = block.index('{', ep)
    close_eff = find_matching_brace(block, open_eff)
    old_eff = block[ep:close_eff+1]
    new_block = block.replace(old_eff, new_effect, 1)
    return text[:start] + new_block + text[end+1:]

# 1) Preview-safe dismissal cost Script Values.
values_path = 'in_game/common/script_values/eu5gov_governor_values.txt'
values = read(values_path)
if 'eu5gov_dismissal_cost_scale' not in values:
    values += '''\n\n# Preview-safe political dismissal scale. Minimum 10, otherwise current Entrenchment.\neu5gov_dismissal_cost_scale = {\n    value = 10\n    if = {\n        limit = {\n            has_variable = eu5gov_entrenchment\n            var:eu5gov_entrenchment > 10\n        }\n        subtract = 10\n        add = var:eu5gov_entrenchment\n    }\n}\n\neu5gov_dismissal_satisfaction_delta = {\n    value = eu5gov_dismissal_cost_scale\n    multiply = -0.01\n}\n\neu5gov_dismissal_stability_delta = {\n    value = eu5gov_dismissal_cost_scale\n    multiply = -0.50\n}\n'''
write(values_path, values)

# 2) Make the shared dismissal effect use Script Values directly rather than a temporary variable.
effects_path = 'in_game/common/scripted_effects/eu5gov_governor_effects.txt'
effects = read(effects_path)
start = effects.index('eu5gov_apply_governor_dismissal_cost_effect = {')
end_marker = '\n\n# Current scope: country.\n# Each serving Governor increases'
end = effects.index(end_marker, start)
new_dismiss_helper = '''eu5gov_apply_governor_dismissal_cost_effect = {\n\tif = {\n\t\tlimit = {\n\t\t\thas_variable = eu5gov_governorship\n\t\t\tNOT = { has_estate = estate_type:crown_estate }\n\t\t}\n\n\t\tsave_scope_as = eu5gov_dismissed_governor\n\t\tvar:eu5gov_governorship ?= {\n\t\t\towner ?= {\n\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\ttype = scope:eu5gov_dismissed_governor.estate_type\n\t\t\t\t\tvalue = scope:eu5gov_dismissed_governor.eu5gov_dismissal_satisfaction_delta\n\t\t\t\t}\n\t\t\t\tadd_stability = scope:eu5gov_dismissed_governor.eu5gov_dismissal_stability_delta\n\t\t\t}\n\t\t}\n\t}\n}\n'''
effects = effects[:start] + new_dismiss_helper + effects[end:]
write(effects_path, effects)

# 3) Generic actions: explicit confirmation previews and no empty role-change confirmation.
actions_path = 'in_game/common/generic_actions/eu5gov_governor_outliner_actions.txt'
actions = read(actions_path)

replacement_effect = r'''effect = {
		if = {
			limit = {
				exists = scope:target
				exists = scope:target_1
			}

			scope:target_1 = {
				var:eu5gov_governor ?= {
					if = {
						limit = { has_estate = estate_type:crown_estate }
						custom_tooltip = EU5GOV_REPLACE_CONFIRM_CROWN_FREE
					}
					else = {
						custom_tooltip = {
							text = EU5GOV_REPLACE_CONFIRM_COSTS
							save_scope_as = eu5gov_replaced_governor
							var:eu5gov_governorship ?= {
								owner ?= {
									add_estate_satisfaction = {
										type = scope:eu5gov_replaced_governor.estate_type
										value = scope:eu5gov_replaced_governor.eu5gov_dismissal_satisfaction_delta
									}
									add_stability = scope:eu5gov_replaced_governor.eu5gov_dismissal_stability_delta
								}
							}
						}
					}
				}
			}

			hidden_effect = {
				scope:target_1 = { eu5gov_clear_governor_location_effect = yes }
				scope:target_1 = {
					set_variable = { name = eu5gov_governor value = scope:target }
					set_variable = { name = eu5gov_governor_country value = scope:actor }
					set_variable = { name = eu5gov_governor_role value = 1 }
					set_variable = { name = eu5gov_entrenchment value = 0 }
					eu5gov_apply_governor_bonus_effect = yes
				}
				scope:target = {
					set_variable = { name = eu5gov_governorship value = scope:target_1 }
					set_variable = { name = eu5gov_governor_role value = 1 }
					set_variable = { name = eu5gov_entrenchment value = 0 }
					add_character_modifier = { modifier = busy_modifier years = -1 mode = add_and_extend }
				}
				scope:actor = {
					remove_from_variable_map = { name = eu5gov_governor_roster key = scope:target }
					add_to_variable_map = { name = eu5gov_governor_roster key = scope:target value = scope:target_1 }
					remove_from_variable_map = { name = eu5gov_governor_offices key = scope:target_1 }
					add_to_variable_map = { name = eu5gov_governor_offices key = scope:target_1 value = 1 }
				}
				scope:target_1 = { eu5gov_apply_governor_role_effect = yes }
				scope:actor = { eu5gov_refresh_governor_estate_power_effect = yes }
			}
		}
	}'''
actions = replace_action_effect(actions, 'eu5gov_change_governor_from_outliner', replacement_effect)

role_effects = {
'eu5gov_set_role_normal_from_outliner': ('EU5GOV_ROLE_CHANGE_CONFIRM_NORMAL', '1'),
'eu5gov_set_role_integration_from_outliner': ('EU5GOV_ROLE_CHANGE_CONFIRM_INTEGRATION', '2'),
'eu5gov_set_role_colonial_from_outliner': ('EU5GOV_ROLE_CHANGE_CONFIRM_COLONIAL', '3'),
}
for aid, (tt, role) in role_effects.items():
    eff = f'''effect = {{\n\t\tcustom_tooltip = {{\n\t\t\ttext = {tt}\n\t\t\tscope:actor = {{ add_stability = -20 }}\n\t\t}}\n\t\thidden_effect = {{\n\t\t\tscope:target_1 = {{\n\t\t\t\tset_variable = {{ name = eu5gov_governor_role value = {role} }}\n\t\t\t\tvar:eu5gov_governor ?= {{ set_variable = {{ name = eu5gov_governor_role value = {role} }} }}\n\t\t\t\teu5gov_apply_governor_role_effect = yes\n\t\t\t}}\n\t\t}}\n\t}}'''
    actions = replace_action_effect(actions, aid, eff)

dismiss_effect = r'''effect = {
		scope:target_1 = {
			var:eu5gov_governor ?= {
				if = {
					limit = { has_estate = estate_type:crown_estate }
					custom_tooltip = EU5GOV_DISMISS_CONFIRM_CROWN_FREE
				}
				else = {
					custom_tooltip = {
						text = EU5GOV_DISMISS_CONFIRM_COSTS
						save_scope_as = eu5gov_action_dismissed_governor
						var:eu5gov_governorship ?= {
							owner ?= {
								add_estate_satisfaction = {
									type = scope:eu5gov_action_dismissed_governor.estate_type
									value = scope:eu5gov_action_dismissed_governor.eu5gov_dismissal_satisfaction_delta
								}
								add_stability = scope:eu5gov_action_dismissed_governor.eu5gov_dismissal_stability_delta
							}
						}
					}
				}
			}
		}
		hidden_effect = {
			scope:target_1 = { eu5gov_clear_governor_location_effect = yes }
			scope:actor = { eu5gov_refresh_governor_estate_power_effect = yes }
		}
	}'''
actions = replace_action_effect(actions, 'eu5gov_dismiss_governor_from_outliner', dismiss_effect)

actions = actions.replace('Replacing an office holder is a voluntary dismissal of the outgoing', 'Replacing an office holder removes the outgoing Governor from office and')
actions = actions.replace('# Governor and therefore pays the same Machtbasis-scaled political cost.', '# therefore applies the same Entrenchment-scaled political cost.')
write(actions_path, actions)

# 4) Localization: clearer terminology + explicit confirmation effect lines.
locs = {
'main_menu/localization/german/zz_eu5gov_l_german.yml': {
'EU5GOV_PORTRAIT_CHANGE_DESC': 'EU5GOV_PORTRAIT_CHANGE_DESC: "Linksklick: Nachfolger wählen. Rechtsklick: Gouverneur direkt entlassen. Gehört der bisherige Gouverneur einem anderen Stand als dem Kronstand an, entstehen bei Ersetzung dieselben nach [eu5gov_entrenchment|e] skalierten politischen Kosten wie bei einer Entlassung."',
'eu5gov_change_governor_from_outliner_desc': 'eu5gov_change_governor_from_outliner_desc: "Wählt einen neuen geeigneten Gouverneur. Vor der Ersetzung zeigt eine Bestätigung die politischen Kosten des bisherigen Amtsinhabers. Gehört er dem Kronstand an, fallen keine Entlassungskosten an; andernfalls richten sie sich nach seiner [eu5gov_entrenchment|e]."',
'eu5gov_dismiss_governor_from_outliner_desc': 'eu5gov_dismiss_governor_from_outliner_desc: "Entlässt den amtierenden Gouverneur. Die Bestätigung zeigt die tatsächlichen Auswirkungen auf [estate_satisfaction|e] und [stability|e]. Gehört der Gouverneur dem Kronstand an, fallen keine politischen Entlassungskosten an."',
'EU5GOV_DISMISS_TT': 'EU5GOV_DISMISS_TT: "Entlasst diesen [eu5gov_governor|e]. Gehört er einem anderen Stand als dem Kronstand an, kostet die Entlassung mindestens #R -10 Standeszufriedenheit#! und #R -5 Stabilität#!. Ab 10 [eu5gov_entrenchment|e] skaliert der Preis linear bis #R -100 Zufriedenheit#! und #R -50 Stabilität#! bei 100. Für Gouverneure des Kronstands entfallen diese Kosten."',
'EU5GOV_ENTRENCHMENT_TT': 'EU5GOV_ENTRENCHMENT_TT: "[eu5gov_entrenchment|E] wächst jeden Monat um #Y (2 + ([adm|e] + [dip|e] + [mil|e]) / 100) / 12#! bis maximal 100. Jeder Gouverneur erhöht die [estate_power|e] seines [estate|e] um die Hälfte seiner Verankerung. Wird ein Gouverneur entlassen oder ersetzt, bestimmen Verankerung und Stand die politischen Kosten."',
'EU5GOV_ENTRENCHMENT_TT_EFFECTS': 'EU5GOV_ENTRENCHMENT_TT_EFFECTS: "#T Politische Auswirkungen#!\\n$BULLET$Die [estate_power|e] des [estate|e] des Gouverneurs steigt je Punkt [eu5gov_entrenchment|e] um #Y 0,5 %#!.\\n$BULLET$Bei 100 Verankerung entspricht das #Y +50 % Standesmacht#!.\\n$BULLET$Die Verankerung kann höchstens #Y 100#! erreichen."',
'EU5GOV_ENTRENCHMENT_TT_DISMISSAL': 'EU5GOV_ENTRENCHMENT_TT_DISMISSAL: "#T Entlassung und Ersetzung#!\\n$BULLET$Gehört der Gouverneur einem anderen [estate|e] als dem Kronstand an, gilt mindestens eine Kostenbasis von #Y 10#!; oberhalb davon entspricht sie der aktuellen [eu5gov_entrenchment|e].\\n$BULLET$[estate_satisfaction|e]: #R −max(10, Verankerung)#! Prozentpunkte.\\n$BULLET$[stability|e]: #R −0,5 × max(10, Verankerung)#!.\\n$BULLET$Für Gouverneure des Kronstands entfallen diese politischen Kosten."',
'game_concept_eu5gov_entrenchment_desc': 'game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] misst, wie fest ein [eu5gov_governor|e] politisch und administrativ in seinem Amt verankert ist.\\n\\n#T Wachstum#!\\nSie steigt monatlich um #Y (2 + ([adm|e] + [dip|e] + [mil|e]) / 100) / 12#! und ist auf 100 begrenzt.\\n\\n#T Auswirkungen#!\\n$BULLET$Jeder Punkt erhöht die [estate_power|e] des [estate|e] des Gouverneurs um #Y 0,5 %#!.\\n$BULLET$Wird ein Gouverneur aus einem Stand außerhalb des Kronstands entlassen oder ersetzt, sinkt die [estate_satisfaction|e] um mindestens 10 Prozentpunkte beziehungsweise um seine Verankerung, falls diese höher ist.\\n$BULLET$Zusätzlich verliert das Land halb so viel [stability|e].\\n$BULLET$Für Gouverneure des Kronstands entfallen diese Entlassungskosten."',
},
'main_menu/localization/english/zz_eu5gov_l_english.yml': {
'EU5GOV_PORTRAIT_CHANGE_DESC': 'EU5GOV_PORTRAIT_CHANGE_DESC: "Left-click: choose a replacement. Right-click: dismiss the Governor directly. If the outgoing Governor belongs to an Estate other than the Crown Estate, replacement applies the same Entrenchment-scaled political cost as dismissal."',
'eu5gov_change_governor_from_outliner_desc': 'eu5gov_change_governor_from_outliner_desc: "Choose a new eligible Governor. The confirmation shows the outgoing office holder’s political cost. Governors of the Crown Estate have no dismissal cost; for other Estates the cost depends on [eu5gov_entrenchment|e]."',
'eu5gov_dismiss_governor_from_outliner_desc': 'eu5gov_dismiss_governor_from_outliner_desc: "Dismiss the serving Governor. The confirmation shows the actual effects on [estate_satisfaction|e] and [stability|e]. Governors of the Crown Estate have no political dismissal cost."',
'EU5GOV_DISMISS_TT': 'EU5GOV_DISMISS_TT: "Dismiss this [eu5gov_governor|e]. If they belong to an Estate other than the Crown Estate, dismissal costs at least #R -10 Estate Satisfaction#! and #R -5 Stability#!. From 10 [eu5gov_entrenchment|e] upward the price scales linearly to #R -100 Satisfaction#! and #R -50 Stability#! at 100. Crown Estate Governors do not pay these costs."',
'EU5GOV_ENTRENCHMENT_TT': 'EU5GOV_ENTRENCHMENT_TT: "[eu5gov_entrenchment|E] rises every month by #Y (2 + ([adm|e] + [dip|e] + [mil|e]) / 100) / 12#!, up to 100. Each Governor increases the [estate_power|e] of their [estate|e] by half their Entrenchment. When a Governor is dismissed or replaced, Entrenchment and Estate membership determine the political cost."',
'EU5GOV_ENTRENCHMENT_TT_EFFECTS': 'EU5GOV_ENTRENCHMENT_TT_EFFECTS: "#T Political Effects#!\\n$BULLET$The Governor’s [estate|e] gains #Y +0.5% [estate_power|e]#! for each point of [eu5gov_entrenchment|e].\\n$BULLET$At 100 Entrenchment this is #Y +50% Estate Power#!.\\n$BULLET$Entrenchment is capped at #Y 100#!."',
'EU5GOV_ENTRENCHMENT_TT_DISMISSAL': 'EU5GOV_ENTRENCHMENT_TT_DISMISSAL: "#T Dismissal and Replacement#!\\n$BULLET$If the Governor belongs to an [estate|e] other than the Crown Estate, the cost scale is at least #Y 10#! and otherwise equals current [eu5gov_entrenchment|e].\\n$BULLET$[estate_satisfaction|e]: #R −max(10, Entrenchment)#! percentage points.\\n$BULLET$[stability|e]: #R −0.5 × max(10, Entrenchment)#!.\\n$BULLET$Crown Estate Governors do not pay these political costs."',
'game_concept_eu5gov_entrenchment_desc': 'game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] measures how firmly a [eu5gov_governor|e] is politically and administratively established in office.\\n\\n#T Growth#!\\nIt rises monthly by #Y (2 + ([adm|e] + [dip|e] + [mil|e]) / 100) / 12#! and is capped at 100.\\n\\n#T Effects#!\\n$BULLET$Each point increases the [estate_power|e] of the Governor’s [estate|e] by #Y 0.5%#!.\\n$BULLET$If a Governor belonging to an Estate other than the Crown Estate is dismissed or replaced, [estate_satisfaction|e] falls by at least 10 percentage points or by their Entrenchment if higher.\\n$BULLET$The country also loses half as much [stability|e].\\n$BULLET$Crown Estate Governors do not pay these dismissal costs."',
}
}

new_lines = {
'main_menu/localization/german/zz_eu5gov_l_german.yml': [
'EU5GOV_DISMISS_CONFIRM_COSTS: "#T Politische Kosten#!\\nDer Gouverneur gehört einem Stand außerhalb des Kronstands an. Die folgenden Kosten werden bei der Entlassung sofort angewendet:"',
'EU5GOV_DISMISS_CONFIRM_CROWN_FREE: "#T Keine politischen Entlassungskosten#!\\nDieser Gouverneur gehört dem Kronstand an. [estate_satisfaction|e] und [stability|e] werden durch die Entlassung nicht gesenkt."',
'EU5GOV_REPLACE_CONFIRM_COSTS: "#T Politische Kosten des Austauschs#!\\nDer bisherige Gouverneur gehört einem Stand außerhalb des Kronstands an. Die folgenden Kosten werden angewendet, bevor der Nachfolger sein Amt antritt:"',
'EU5GOV_REPLACE_CONFIRM_CROWN_FREE: "#T Keine politischen Austauschkosten#!\\nDer bisherige Gouverneur gehört dem Kronstand an. Für seine Ersetzung fallen keine Kosten auf [estate_satisfaction|e] oder [stability|e] an."',
'EU5GOV_ROLE_CHANGE_CONFIRM_NORMAL: "#T Amtsausrichtung ändern#!\\nDer Gouverneur wird zum [eu5gov_provincial_governor|e].\\nKosten: #R -20 [stability|e]#!."',
'EU5GOV_ROLE_CHANGE_CONFIRM_INTEGRATION: "#T Amtsausrichtung ändern#!\\nDer Gouverneur wird zum [eu5gov_integration_governor_role|e].\\nKosten: #R -20 [stability|e]#!."',
'EU5GOV_ROLE_CHANGE_CONFIRM_COLONIAL: "#T Amtsausrichtung ändern#!\\nDer Gouverneur wird zum [eu5gov_colonial_governor_role|e].\\nKosten: #R -20 [stability|e]#!."',
],
'main_menu/localization/english/zz_eu5gov_l_english.yml': [
'EU5GOV_DISMISS_CONFIRM_COSTS: "#T Political Cost#!\\nThe Governor belongs to an Estate other than the Crown Estate. The following costs are applied immediately on dismissal:"',
'EU5GOV_DISMISS_CONFIRM_CROWN_FREE: "#T No Political Dismissal Cost#!\\nThis Governor belongs to the Crown Estate. Dismissal does not reduce [estate_satisfaction|e] or [stability|e]."',
'EU5GOV_REPLACE_CONFIRM_COSTS: "#T Political Cost of Replacement#!\\nThe outgoing Governor belongs to an Estate other than the Crown Estate. The following costs are applied before the successor takes office:"',
'EU5GOV_REPLACE_CONFIRM_CROWN_FREE: "#T No Political Replacement Cost#!\\nThe outgoing Governor belongs to the Crown Estate. Replacing them does not reduce [estate_satisfaction|e] or [stability|e]."',
'EU5GOV_ROLE_CHANGE_CONFIRM_NORMAL: "#T Change Governor Role#!\\nThe Governor becomes a [eu5gov_provincial_governor|e].\\nCost: #R -20 [stability|e]#!."',
'EU5GOV_ROLE_CHANGE_CONFIRM_INTEGRATION: "#T Change Governor Role#!\\nThe Governor becomes an [eu5gov_integration_governor_role|e].\\nCost: #R -20 [stability|e]#!."',
'EU5GOV_ROLE_CHANGE_CONFIRM_COLONIAL: "#T Change Governor Role#!\\nThe Governor becomes a [eu5gov_colonial_governor_role|e].\\nCost: #R -20 [stability|e]#!."',
]
}

for path, repls in locs.items():
    loc = read(path)
    for key, line in repls.items():
        loc = replace_loc_line(loc, key, line)
    loc = append_after_key(loc, 'eu5gov_dismiss_governor_from_outliner_desc', new_lines[path])
    # Also clean legacy phrases wherever still present.
    loc = loc.replace('freiwillige Entlassung oder Ersetzung', 'Entlassung oder Ersetzung')
    loc = loc.replace('freiwilligen Entlassung oder Ersetzung', 'Entlassung oder Ersetzung')
    loc = loc.replace('Voluntary dismissal or replacement', 'Dismissal or replacement')
    loc = loc.replace('voluntary dismissal/replacement', 'dismissal/replacement')
    loc = loc.replace('voluntary dismissal or replacement', 'dismissal or replacement')
    write(path, loc)

# 5) Release metadata/changelog.
meta_path = '.metadata/metadata.json'
meta = read(meta_path)
meta = replace_once(meta, '"version": "0.2.10"', '"version": "0.2.11"', 'metadata version')
write(meta_path, meta)

ch_path = 'CHANGELOG.md'
ch = read(ch_path)
entry = '''## 0.2.11\n\n- Reworked Governor dismissal/replacement wording to avoid ambiguous “voluntary” and “non-Crown Governor” phrasing.\n- Added preview-safe dismissal cost Script Values with the 10-point minimum, so confirmation windows can show the real minimum cost instead of zero.\n- Dismissal and replacement confirmation previews now expose Estate Satisfaction and Stability effects directly.\n- Governor-role confirmations now contain an explicit role-change effect line plus the fixed -20 Stability cost instead of an empty effect panel.\n\n'''
if '## 0.2.11' not in ch:
    pos = ch.find('## ')
    ch = ch[:pos] + entry + ch[pos:] if pos >= 0 else entry + ch
write(ch_path, ch)
