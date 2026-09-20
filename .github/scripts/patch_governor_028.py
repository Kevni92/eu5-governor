from pathlib import Path


def read(path):
    return Path(path).read_text(encoding='utf-8-sig')


def write_bom(path, text):
    Path(path).write_text('\ufeff' + text, encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, got {count}')
    return text.replace(old, new, 1)

# -----------------------------------------------------------------------------
# Generic actions for reliable role switching and portrait right-click dismissal.
# -----------------------------------------------------------------------------
p = 'in_game/common/generic_actions/eu5gov_governor_outliner_actions.txt'
t = read(p)
if 'eu5gov_set_role_normal_from_outliner = {' not in t:
    t += r'''

# Direct outliner actions use the same Generic Action path as the portrait chooser.
# Role changes cost 20 Stability and are disabled when their territorial requirement
# is not met, instead of accepting a click and then silently doing nothing.
eu5gov_set_role_normal_from_outliner = {
	type = owncountry
	sound = UI_action_religion_generic
	show_message = no
	show_message_to_target = no
	show_in_gui_list = no
	ai_tick = never
	ai_tick_frequency = 99999

	potential = {
		exists = scope:target_1
		scope:target_1 = {
			owner ?= scope:actor
			has_building = building_type:local_governor
			has_variable = eu5gov_governor
			NOT = { var:eu5gov_governor_role = 1 }
		}
	}
	allow = { always = yes }
	effect = {
		scope:target_1 = {
			set_variable = { name = eu5gov_governor_role value = 1 }
			var:eu5gov_governor ?= { set_variable = { name = eu5gov_governor_role value = 1 } }
			eu5gov_apply_governor_role_effect = yes
		}
		scope:actor = { add_stability = -20 }
	}
	ai_will_do = { add = -100 }
}


eu5gov_set_role_integration_from_outliner = {
	type = owncountry
	sound = UI_action_religion_generic
	show_message = no
	show_message_to_target = no
	show_in_gui_list = no
	ai_tick = never
	ai_tick_frequency = 99999

	potential = {
		exists = scope:target_1
		scope:target_1 = {
			owner ?= scope:actor
			has_building = building_type:local_governor
			has_variable = eu5gov_governor
			NOT = { var:eu5gov_governor_role = 2 }
		}
	}
	allow = {
		scope:target_1 = {
			custom_tooltip = {
				text = EU5GOV_ROLE_INTEGRATION_REQUIREMENT
				NOT = { dominant_culture = owner.culture }
			}
		}
	}
	effect = {
		scope:target_1 = {
			set_variable = { name = eu5gov_governor_role value = 2 }
			var:eu5gov_governor ?= { set_variable = { name = eu5gov_governor_role value = 2 } }
			eu5gov_apply_governor_role_effect = yes
		}
		scope:actor = { add_stability = -20 }
	}
	ai_will_do = { add = -100 }
}


eu5gov_set_role_colonial_from_outliner = {
	type = owncountry
	sound = UI_action_religion_generic
	show_message = no
	show_message_to_target = no
	show_in_gui_list = no
	ai_tick = never
	ai_tick_frequency = 99999

	potential = {
		exists = scope:target_1
		scope:target_1 = {
			owner ?= scope:actor
			has_building = building_type:local_governor
			has_variable = eu5gov_governor
			NOT = { var:eu5gov_governor_role = 3 }
		}
	}
	allow = {
		scope:target_1 = {
			custom_tooltip = {
				text = EU5GOV_ROLE_COLONIAL_REQUIREMENT
				is_overseas_for_owner = yes
			}
		}
	}
	effect = {
		scope:target_1 = {
			set_variable = { name = eu5gov_governor_role value = 3 }
			var:eu5gov_governor ?= { set_variable = { name = eu5gov_governor_role value = 3 } }
			eu5gov_apply_governor_role_effect = yes
		}
		scope:actor = { add_stability = -20 }
	}
	ai_will_do = { add = -100 }
}


eu5gov_dismiss_governor_from_outliner = {
	type = owncountry
	sound = UI_action_religion_generic
	show_message = no
	show_message_to_target = no
	show_in_gui_list = no
	ai_tick = never
	ai_tick_frequency = 99999

	potential = {
		exists = scope:target_1
		scope:target_1 = {
			owner ?= scope:actor
			has_building = building_type:local_governor
			has_variable = eu5gov_governor
		}
	}
	allow = { always = yes }
	effect = {
		scope:target_1 = {
			var:eu5gov_governor ?= { eu5gov_apply_governor_dismissal_cost_effect = yes }
			eu5gov_clear_governor_location_effect = yes
		}
		scope:actor = { eu5gov_refresh_governor_estate_power_effect = yes }
	}
	ai_will_do = { add = -100 }
}
'''
write_bom(p, t)

# Register new actions in the AI list even though they never AI-tick.
p = 'in_game/common/generic_action_ai_lists/eu5gov_governor_actions.txt'
t = read(p)
old = '''\t\teu5gov_appoint_governor_from_outliner\n\t\teu5gov_change_governor_from_outliner\n'''
new = '''\t\teu5gov_appoint_governor_from_outliner\n\t\teu5gov_change_governor_from_outliner\n\t\teu5gov_set_role_normal_from_outliner\n\t\teu5gov_set_role_integration_from_outliner\n\t\teu5gov_set_role_colonial_from_outliner\n\t\teu5gov_dismiss_governor_from_outliner\n'''
if 'eu5gov_set_role_normal_from_outliner' not in t:
    t = replace_once(t, old, new, 'generic action AI list')
write_bom(p, t)

# -----------------------------------------------------------------------------
# Outliner: lock icon + concept tooltip; Generic Action role entries; RMB portrait
# dismissal. Invalid specialist roles are now disabled by Generic Action `allow`.
# -----------------------------------------------------------------------------
p = 'in_game/gui/outliner.gui'
t = read(p)

old = '''                                OutlinerTextBase = {\n                                    align = right\n                                    autoresize = yes\n                                    fontsize = 12\n                                    raw_text = "[Localize('EU5GOV_ENTRENCHMENT_SHORT')] [Location.MakeScope.GetVariable('eu5gov_entrenchment').GetValue|0]/100"\n                                }'''
new = '''                                hbox = {\n                                    align = right\n                                    spacing = 3\n                                    tooltip = "[eu5gov_entrenchment|e]"\n                                    tagtooltip_enabled = yes\n\n                                    icon = {\n                                        size = { 14 14 }\n                                        texture = "gfx/interface/icons/flat_icons/lock.dds"\n                                    }\n                                    OutlinerTextBase = {\n                                        align = right\n                                        autoresize = yes\n                                        fontsize = 12\n                                        raw_text = "[Location.MakeScope.GetVariable('eu5gov_entrenchment').GetValue|0]/100"\n                                    }\n                                }'''
t = replace_once(t, old, new, 'entrenchment line')

old = '''                                    left_action = { action_name = "eu5gov_change_governor_from_outliner" }\n                                    tooltipwidget = { BasicFunctionalTooltip = {} }'''
new = '''                                    left_action = { action_name = "eu5gov_change_governor_from_outliner" }\n                                    right_action = { action_name = "eu5gov_dismiss_governor_from_outliner" }\n                                    tooltipwidget = { BasicFunctionalTooltip = {} }'''
t = replace_once(t, old, new, 'occupied portrait action')

# Replace only the custom Governor context menu entry block.
custom_start = t.index('types EU5GovOutlinerTypes')
block_start = t.index('blockoverride "contextmenu_entries" {', custom_start)
brace = t.index('{', block_start)
depth = 0
block_end = None
for i in range(brace, len(t)):
    if t[i] == '{':
        depth += 1
    elif t[i] == '}':
        depth -= 1
        if depth == 0:
            block_end = i + 1
            break
if block_end is None:
    raise SystemExit('Could not locate end of Governor contextmenu_entries block')

replacement = r'''blockoverride "contextmenu_entries" {
                                            ContextMenuActionEntry = {
                                                title = "EU5GOV_ROLE_NORMAL"
                                                actor = "[GetPlayer]"
                                                parameter = {
                                                    parameter_name = "target_1"
                                                    parameter_value = "[Location.Self]"
                                                }
                                                left_action = {
                                                    action_name = "eu5gov_set_role_normal_from_outliner"
                                                    parameter = {
                                                        parameter_name = "target_1"
                                                        parameter_value = "[Location.Self]"
                                                    }
                                                }
                                                blockoverride "entry_text" { text = "EU5GOV_ROLE_NORMAL" }
                                            }

                                            ContextMenuActionEntry = {
                                                title = "EU5GOV_ROLE_INTEGRATION"
                                                actor = "[GetPlayer]"
                                                parameter = {
                                                    parameter_name = "target_1"
                                                    parameter_value = "[Location.Self]"
                                                }
                                                left_action = {
                                                    action_name = "eu5gov_set_role_integration_from_outliner"
                                                    parameter = {
                                                        parameter_name = "target_1"
                                                        parameter_value = "[Location.Self]"
                                                    }
                                                }
                                                blockoverride "entry_text" { text = "EU5GOV_ROLE_INTEGRATION" }
                                            }

                                            ContextMenuActionEntry = {
                                                title = "EU5GOV_ROLE_COLONIAL"
                                                actor = "[GetPlayer]"
                                                parameter = {
                                                    parameter_name = "target_1"
                                                    parameter_value = "[Location.Self]"
                                                }
                                                left_action = {
                                                    action_name = "eu5gov_set_role_colonial_from_outliner"
                                                    parameter = {
                                                        parameter_name = "target_1"
                                                        parameter_value = "[Location.Self]"
                                                    }
                                                }
                                                blockoverride "entry_text" { text = "EU5GOV_ROLE_COLONIAL" }
                                            }

                                            ContextMenuActionEntry = {
                                                title = "EU5GOV_DISMISS"
                                                actor = "[GetPlayer]"
                                                parameter = {
                                                    parameter_name = "target_1"
                                                    parameter_value = "[Location.Self]"
                                                }
                                                left_action = {
                                                    action_name = "eu5gov_dismiss_governor_from_outliner"
                                                    parameter = {
                                                        parameter_name = "target_1"
                                                        parameter_value = "[Location.Self]"
                                                    }
                                                }
                                                blockoverride "button_texture" { using = button_regular_red_texture }
                                                blockoverride "entry_text" { text = "EU5GOV_DISMISS" }
                                            }
                                        }'''
t = t[:block_start] + replacement + t[block_end:]
write_bom(p, t)

# -----------------------------------------------------------------------------
# Localization: modifier math, role-change cost/requirements, portrait RMB hint.
# -----------------------------------------------------------------------------
for p, lang in [
    ('main_menu/localization/german/zz_eu5gov_l_german.yml', 'de'),
    ('main_menu/localization/english/zz_eu5gov_l_english.yml', 'en'),
]:
    t = read(p)
    if lang == 'de':
        t = replace_once(
            t,
            ' STATIC_MODIFIER_DESC_eu5gov_governor_administration: "Die Verwaltungsfähigkeit des amtierenden Gouverneurs erhöht die lokale Nähequelle."',
            ' STATIC_MODIFIER_DESC_eu5gov_governor_administration: "Der angezeigte Wert #G +1,00#! ist die Basiseinheit des skalierbaren Modifikators. Die tatsächliche Nähequelle entspricht #Y ADM des Gouverneurs × 0,50#!. Beispiel: 55 ADM ergeben #G +27,50#! Nähequelle; zusammen mit den #G +30#! der Gouverneursresidenz sind das #G 57,50#!."',
            'German modifier description')
        t = t.replace(' EU5GOV_PORTRAIT_CHANGE_DESC: "Wählt einen Nachfolger. Das Ersetzen eines Nicht-Kron-Gouverneurs verursacht dieselben nach Verankerung skalierenden politischen Kosten wie eine Entlassung."',
                      ' EU5GOV_PORTRAIT_CHANGE_DESC: "Linksklick: Nachfolger wählen. Rechtsklick: Gouverneur direkt entlassen. Das Ersetzen eines Nicht-Kron-Gouverneurs verursacht dieselben nach Verankerung skalierenden politischen Kosten wie eine Entlassung."')
        t = t.replace(' EU5GOV_ROLE_NORMAL_TT: "[eu5gov_provincial_governor|E]: allgemeine Provinzverwaltung ohne zusätzlichen Spezialmodifikator. Der Gouverneur behält den Grundeffekt von #G ADM × 0,50#! Nähequelle zusätzlich zu den #G 30#! der Residenz. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
                      ' EU5GOV_ROLE_NORMAL_TT: "[eu5gov_provincial_governor|E]: allgemeine Provinzverwaltung ohne zusätzlichen Spezialmodifikator. Der Gouverneur behält den Grundeffekt von #G ADM × 0,50#! Nähequelle zusätzlich zu den #G 30#! der Residenz. Ein Wechsel der Amtsausrichtung kostet #R 20 Stabilität#!. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."')
        t = t.replace(' EU5GOV_ROLE_INTEGRATION_TT: "[eu5gov_integration_governor_role|E]: verfügbar, wenn die vorherrschende Kultur des Gouverneurssitzes von der Kultur des Besitzers abweicht. Gewährt am Sitz #G +25 % lokale Assimilationsgeschwindigkeit#! und behält den normalen ADM-basierten Nähebonus. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
                      ' EU5GOV_ROLE_INTEGRATION_TT: "[eu5gov_integration_governor_role|E]: verfügbar, wenn die vorherrschende Kultur des Gouverneurssitzes von der Kultur des Besitzers abweicht. Gewährt am Sitz #G +25 % lokale Assimilationsgeschwindigkeit#! und behält den normalen ADM-basierten Nähebonus. Ein Wechsel der Amtsausrichtung kostet #R 20 Stabilität#!."')
        t = t.replace(' EU5GOV_ROLE_COLONIAL_TT: "[eu5gov_colonial_governor_role|E]: nur in überseeischen Gebieten verfügbar. Gewährt dort #G +0,25 lokale Migrationsattraktivität#! und #G +0,001 lokales Bevölkerungswachstum#! und behält den normalen ADM-basierten Nähebonus. Die bereits aktive Amtsausrichtung kann nicht erneut gewählt werden."',
                      ' EU5GOV_ROLE_COLONIAL_TT: "[eu5gov_colonial_governor_role|E]: nur in überseeischen Gebieten verfügbar. Gewährt dort #G +0,25 lokale Migrationsattraktivität#! und #G +0,001 lokales Bevölkerungswachstum#! und behält den normalen ADM-basierten Nähebonus. Ein Wechsel der Amtsausrichtung kostet #R 20 Stabilität#!."')
        insert = '''\n eu5gov_set_role_normal_from_outliner: "Provinzgouverneur"\n eu5gov_set_role_normal_from_outliner_desc: "Wechselt zu [eu5gov_provincial_governor|e]. Kosten: #R 20 Stabilität#!."\n eu5gov_set_role_integration_from_outliner: "Integrationsgouverneur"\n eu5gov_set_role_integration_from_outliner_desc: "Wechselt zu [eu5gov_integration_governor_role|e]. Kosten: #R 20 Stabilität#!."\n eu5gov_set_role_colonial_from_outliner: "Kolonialgouverneur"\n eu5gov_set_role_colonial_from_outliner_desc: "Wechselt zu [eu5gov_colonial_governor_role|e]. Kosten: #R 20 Stabilität#!."\n eu5gov_dismiss_governor_from_outliner: "Gouverneur entlassen"\n eu5gov_dismiss_governor_from_outliner_desc: "Entlässt den amtierenden Gouverneur. Die politischen Kosten richten sich nach seiner [eu5gov_entrenchment|e]."\n EU5GOV_ROLE_INTEGRATION_REQUIREMENT: "Die vorherrschende Kultur des Gouverneurssitzes muss von der Kultur des Besitzers abweichen."\n EU5GOV_ROLE_COLONIAL_REQUIREMENT: "Der Gouverneurssitz muss für seinen Besitzer überseeisch sein."\n'''
    else:
        t = replace_once(
            t,
            ' STATIC_MODIFIER_DESC_eu5gov_governor_administration: "The serving Governor\'s Administrative ability increases this location\'s Proximity Source."',
            ' STATIC_MODIFIER_DESC_eu5gov_governor_administration: "The displayed #G +1.00#! is the base unit of this scalable modifier. The actual Proximity Source equals #Y Governor ADM × 0.50#!. Example: 55 ADM gives #G +27.50#! Proximity Source; together with the Residence\'s #G +30#! that is #G 57.50#!."',
            'English modifier description')
        t = t.replace(' EU5GOV_PORTRAIT_CHANGE_DESC: "Choose a replacement Governor. Replacing a non-Crown Governor pays the same Entrenchment-scaled political cost as dismissal."',
                      ' EU5GOV_PORTRAIT_CHANGE_DESC: "Left-click: choose a replacement. Right-click: dismiss the Governor directly. Replacing a non-Crown Governor pays the same Entrenchment-scaled political cost as dismissal."')
        t = t.replace(' EU5GOV_ROLE_NORMAL_TT: "[eu5gov_provincial_governor|E]: general provincial administration with no additional specialist modifier. The Governor retains the base #G ADM × 0.50#! Proximity contribution on top of the Residence\'s #G 30#!. The active role cannot be selected again."',
                      ' EU5GOV_ROLE_NORMAL_TT: "[eu5gov_provincial_governor|E]: general provincial administration with no additional specialist modifier. The Governor retains the base #G ADM × 0.50#! Proximity contribution on top of the Residence\'s #G 30#!. Changing role costs #R 20 Stability#!. The active role cannot be selected again."')
        t = t.replace(' EU5GOV_ROLE_INTEGRATION_TT: "[eu5gov_integration_governor_role|E]: available when the Governor seat has a different dominant culture from its owner. Grants #G +25% local assimilation speed#! at the seat in addition to the normal ADM-based Proximity contribution. The active role cannot be selected again."',
                      ' EU5GOV_ROLE_INTEGRATION_TT: "[eu5gov_integration_governor_role|E]: available when the Governor seat has a different dominant culture from its owner. Grants #G +25% local assimilation speed#! at the seat in addition to the normal ADM-based Proximity contribution. Changing role costs #R 20 Stability#!."')
        t = t.replace(' EU5GOV_ROLE_COLONIAL_TT: "[eu5gov_colonial_governor_role|E]: available only at overseas Governor seats. Grants #G +0.25 local migration attraction#! and #G +0.001 local population growth#! at the seat in addition to the normal ADM-based Proximity contribution. The active role cannot be selected again."',
                      ' EU5GOV_ROLE_COLONIAL_TT: "[eu5gov_colonial_governor_role|E]: available only at overseas Governor seats. Grants #G +0.25 local migration attraction#! and #G +0.001 local population growth#! at the seat in addition to the normal ADM-based Proximity contribution. Changing role costs #R 20 Stability#!."')
        insert = '''\n eu5gov_set_role_normal_from_outliner: "Provincial Governor"\n eu5gov_set_role_normal_from_outliner_desc: "Change to [eu5gov_provincial_governor|e]. Cost: #R 20 Stability#!."\n eu5gov_set_role_integration_from_outliner: "Integration Governor"\n eu5gov_set_role_integration_from_outliner_desc: "Change to [eu5gov_integration_governor_role|e]. Cost: #R 20 Stability#!."\n eu5gov_set_role_colonial_from_outliner: "Colonial Governor"\n eu5gov_set_role_colonial_from_outliner_desc: "Change to [eu5gov_colonial_governor_role|e]. Cost: #R 20 Stability#!."\n eu5gov_dismiss_governor_from_outliner: "Dismiss Governor"\n eu5gov_dismiss_governor_from_outliner_desc: "Dismiss the serving Governor. Political cost depends on their [eu5gov_entrenchment|e]."\n EU5GOV_ROLE_INTEGRATION_REQUIREMENT: "The Governor seat must have a different dominant culture from its owner."\n EU5GOV_ROLE_COLONIAL_REQUIREMENT: "The Governor seat must be overseas for its owner."\n'''

    if 'eu5gov_set_role_normal_from_outliner:' not in t:
        anchor = '\n EU5GOV_CONTEXT_TITLE:'
        if anchor not in t:
            raise SystemExit(f'Localization anchor missing in {p}')
        t = t.replace(anchor, insert + anchor, 1)
    write_bom(p, t)

# Metadata/changelog.
p = '.metadata/metadata.json'
t = read(p).replace('"version": "0.2.7"', '"version": "0.2.8"', 1)
write_bom(p, t)

p = 'CHANGELOG.md'
t = read(p)
if '## 0.2.8' not in t:
    entry = '''# Changelog\n\n## 0.2.8\n\n- Governor Administration modifier tooltip now explains why the static modifier shows +1 and how the effective value is calculated: Governor ADM × 0.50, with an explicit 55 ADM = +27.50 example.\n- Replaced the Entrenchment label in Governor outliner rows with a lock icon plus the numeric value; hovering it opens the Entrenchment Game Concept tooltip.\n- Added direct right-click dismissal to occupied Governor portraits through a dedicated Generic Action.\n- Replaced Governor role context-menu ScriptedGui calls with Generic Actions so successful role changes execute reliably and invalid specialist roles are actually disabled instead of silently doing nothing.\n- Changing Governor role now costs 20 Stability.\n- Integration Governor remains limited to culturally distinct seats and Colonial Governor remains limited to overseas seats; their disabled-state conditions are now surfaced by the action system.\n\n'''
    if not t.startswith('# Changelog\n\n'):
        raise SystemExit('Unexpected changelog header')
    t = entry + t[len('# Changelog\n\n'):]
Path(p).write_text(t, encoding='utf-8')
