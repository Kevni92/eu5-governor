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

# 1) Monthly Entrenchment script value for GUI + gameplay consistency.
write('in_game/common/script_values/eu5gov_governor_values.txt', '''eu5gov_monthly_entrenchment_gain = {
    value = 2
    add = {
        value = adm
        divide = 100
    }
    add = {
        value = dip
        divide = 100
    }
    add = {
        value = mil
        divide = 100
    }
    divide = 12
}
''')

# 2) Change the actual tick from yearly-sized increments to monthly increments.
effects_path = 'in_game/common/scripted_effects/eu5gov_governor_effects.txt'
effects = read(effects_path)
start_marker = '# Current scope: serving governor character. Time alone entrenches an office holder;'
end_marker = '# Current scope: serving governor character.\n# Voluntary dismissal/replacement is free for Crown characters.'
start = effects.index(start_marker)
end = effects.index(end_marker, start)
new_tick = '''# Current scope: serving governor character. Time alone entrenches an office holder;
# high total ADM+DIP+MIL accelerates the monthly gain. The former yearly rate is
# divided by 12 so the long-run balance is unchanged while progress is visible monthly.
# The same value is mirrored onto the governed location.
eu5gov_tick_governor_entrenchment_effect = {
    if = {
        limit = { NOT = { has_variable = eu5gov_entrenchment } }
        set_variable = { name = eu5gov_entrenchment value = 0 }
    }

    change_variable = {
        name = eu5gov_entrenchment
        add = {
            value = 2
            divide = 12
        }
    }
    change_variable = {
        name = eu5gov_entrenchment
        add = {
            value = adm
            divide = 1200
        }
    }
    change_variable = {
        name = eu5gov_entrenchment
        add = {
            value = dip
            divide = 1200
        }
    }
    change_variable = {
        name = eu5gov_entrenchment
        add = {
            value = mil
            divide = 1200
        }
    }
    clamp_variable = { name = eu5gov_entrenchment min = 0 max = 100 }

    save_scope_as = eu5gov_entrenchment_governor
    var:eu5gov_governorship ?= {
        set_variable = {
            name = eu5gov_entrenchment
            value = scope:eu5gov_entrenchment_governor.var:eu5gov_entrenchment
        }
        set_variable = {
            name = eu5gov_governor_role
            value = scope:eu5gov_entrenchment_governor.var:eu5gov_governor_role
        }
    }
}

'''
effects = effects[:start] + new_tick + effects[end:]
write(effects_path, effects)

# 3) Tick Entrenchment monthly. Keep yearly pulse as integrity/bonus repair only.
on_action_path = 'in_game/common/on_action/eu5gov_governor_on_actions.txt'
on_action = read(on_action_path)
on_action = replace_once(
    on_action,
    '''yearly_country_pulse = {
\ton_actions = {
\t\teu5gov_governor_yearly_refresh
\t}
}
''',
    '''monthly_country_pulse = {
\ton_actions = {
\t\teu5gov_governor_monthly_entrenchment
\t}
}

yearly_country_pulse = {
\ton_actions = {
\t\teu5gov_governor_yearly_refresh
\t}
}
''',
    'monthly bridge',
)
on_action = replace_once(
    on_action,
    '''\t\t\t\t\tif = {
\t\t\t\t\t\tlimit = { NOT = { has_variable = eu5gov_entrenchment } }
\t\t\t\t\t\tset_variable = { name = eu5gov_entrenchment value = 0 }
\t\t\t\t\t}
\t\t\t\t\teu5gov_tick_governor_entrenchment_effect = yes
''',
    '''\t\t\t\t\tif = {
\t\t\t\t\t\tlimit = { NOT = { has_variable = eu5gov_entrenchment } }
\t\t\t\t\t\tset_variable = { name = eu5gov_entrenchment value = 0 }
\t\t\t\t\t}
''',
    'remove yearly entrenchment tick',
)
monthly_effect = '''
# root = country. Advance serving Governors once per monthly country pulse using
# (2 + (ADM + DIP + MIL) / 100) / 12, preserving the previous annual balance.
eu5gov_governor_monthly_entrenchment = {
\teffect = {
\t\tsave_scope_as = eu5gov_monthly_country
\t\tevery_owned_location = {
\t\t\tlimit = {
\t\t\t\thas_building = building_type:local_governor
\t\t\t\thas_variable = eu5gov_governor
\t\t\t\tvar:eu5gov_governor ?= { is_alive = yes }
\t\t\t\tvar:eu5gov_governor_country ?= { this = scope:eu5gov_monthly_country }
\t\t\t}
\t\t\tvar:eu5gov_governor ?= {
\t\t\t\tif = {
\t\t\t\t\tlimit = { NOT = { has_variable = eu5gov_entrenchment } }
\t\t\t\t\tset_variable = { name = eu5gov_entrenchment value = 0 }
\t\t\t\t}
\t\t\t\teu5gov_tick_governor_entrenchment_effect = yes
\t\t\t}
\t\t}
\t\teu5gov_refresh_governor_estate_power_effect = yes
\t}
}

'''
insert_at = on_action.index('# Rebuild the complete office roster')
on_action = on_action[:insert_at] + monthly_effect + on_action[insert_at:]
on_action = on_action.replace('advance Machtbasis,\n# recalculate Estate power', 'repair Entrenchment state,\n# recalculate Estate power')
write(on_action_path, on_action)

# 4) Outliner: two decimal places, no /100, and a contextual Game Concept tooltip
# with the live monthly rate and current ADM/DIP/MIL breakdown.
outliner_path = 'in_game/gui/outliner.gui'
outliner = read(outliner_path)
outliner = replace_once(
    outliner,
    '''                                    tooltip = "[eu5gov_entrenchment|e]"
                                    tagtooltip_enabled = yes
''',
    '''                                    tooltipwidget = {
                                        ContextualTooltipType = {
                                            datacontext = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter]"
                                            blockoverride "concept_link" {
                                                text = "[eu5gov_entrenchment|e]"
                                            }
                                            blockoverride "title_text" {
                                                text = "game_concept_eu5gov_entrenchment"
                                            }
                                            blockoverride "title_icon" {
                                                icon = {
                                                    using = tooltip_title_icon_size
                                                    texture = "gfx/interface/icons/flat_icons/lock.dds"
                                                }
                                            }
                                            blockoverride "tooltip_content" {
                                                TooltipTextBlock = {
                                                    blockoverride "text" {
                                                        text = "EU5GOV_ENTRENCHMENT_TT_DYNAMIC"
                                                    }
                                                }
                                            }
                                        }
                                    }
''',
    'entrenchment tooltip widget',
)
outliner = replace_once(
    outliner,
    '''                                        raw_text = "[Location.MakeScope.GetVariable('eu5gov_entrenchment').GetValue|0]/100"
''',
    '''                                        raw_text = "[Location.MakeScope.GetVariable('eu5gov_entrenchment').GetValue|2]"
''',
    'entrenchment display precision',
)
write(outliner_path, outliner)

# 5) Localizations: static concept + dynamic character-scoped tooltip.
for path, language in [
    ('main_menu/localization/english/zz_eu5gov_l_english.yml', 'english'),
    ('main_menu/localization/german/zz_eu5gov_l_german.yml', 'german'),
]:
    loc = read(path)
    if language == 'english':
        static = 'EU5GOV_ENTRENCHMENT_TT: "[eu5gov_entrenchment|E] rises every month by #Y (2 + (ADM + DIP + MIL) / 100) / 12#!, up to 100. This preserves the former yearly rate while making growth visible monthly. A Governor increases the power of their Estate by half their Entrenchment and Entrenchment determines voluntary dismissal/replacement costs for non-Crown Governors."'
        dynamic = 'EU5GOV_ENTRENCHMENT_TT_DYNAMIC: "Current monthly growth: #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_gain\')|2]#!\\n\\nCalculation: (#Y 2#! base + (@adm![Character.GetAbility(\'adm\')] + @dip![Character.GetAbility(\'dip\')] + @mil![Character.GetAbility(\'mil\')]) / 100) / 12.\\n\\nEntrenchment is capped at 100. Each point contributes #Y +0.5% Estate power#! for the Governor\'s Estate. Voluntary dismissal or replacement of a non-Crown Governor costs at least -10 Estate Satisfaction / -5 Stability and otherwise scales with Entrenchment up to -100 / -50 at 100. Crown Governors are exempt."'
        concept = 'game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] measures a Governor\'s political and administrative entrenchment from 0 to 100. It grows monthly by #Y (2 + (ADM + DIP + MIL) / 100) / 12#!. This is the previous annual growth formula spread evenly across twelve months. Each Governor increases their Estate\'s power by half their Entrenchment. Voluntarily dismissing or replacing a non-Crown Governor uses a minimum cost scale of 10 and otherwise their Entrenchment: the Estate loses that many percentage points of Satisfaction and the country loses half as much Stability. Crown Governors are exempt."'
    else:
        static = 'EU5GOV_ENTRENCHMENT_TT: "[eu5gov_entrenchment|E] wächst jeden Monat um #Y (2 + (ADM + DIP + MIL) / 100) / 12#! bis maximal 100. Damit bleibt die bisherige Jahresrate unverändert, wird aber monatlich sichtbar. Ein Gouverneur erhöht die Macht seines Standes um die Hälfte seiner Verankerung; außerdem bestimmt die Verankerung die Kosten einer freiwilligen Entlassung oder Ersetzung bei Nicht-Kron-Gouverneuren."'
        dynamic = 'EU5GOV_ENTRENCHMENT_TT_DYNAMIC: "Aktueller monatlicher Zuwachs: #G +[Character.MakeScope.ScriptValue(\'eu5gov_monthly_entrenchment_gain\')|2]#!\\n\\nBerechnung: (#Y 2#! Grundwert + (@adm![Character.GetAbility(\'adm\')] + @dip![Character.GetAbility(\'dip\')] + @mil![Character.GetAbility(\'mil\')]) / 100) / 12.\\n\\nDie Verankerung ist auf 100 begrenzt. Jeder Punkt verleiht dem Stand des Gouverneurs #Y +0,5 % Standesmacht#!. Die freiwillige Entlassung oder Ersetzung eines Nicht-Kron-Gouverneurs kostet mindestens -10 Standeszufriedenheit / -5 Stabilität und skaliert danach mit der Verankerung bis -100 / -50 bei 100. Kron-Gouverneure sind davon ausgenommen."'
        concept = 'game_concept_eu5gov_entrenchment_desc: "[eu5gov_entrenchment|E] misst die politische und administrative Verankerung eines Gouverneurs von 0 bis 100. Sie wächst monatlich um #Y (2 + (ADM + DIP + MIL) / 100) / 12#!. Das entspricht der bisherigen Jahresrate, gleichmäßig auf zwölf Monate verteilt. Jeder Gouverneur erhöht die Macht seines Standes um die Hälfte seiner Verankerung. Bei einer freiwilligen Entlassung oder Ersetzung eines Nicht-Kron-Gouverneurs gilt mindestens ein Kostenwert von 10, darüber seine Verankerung: Der Stand verliert entsprechend viele Prozentpunkte Zufriedenheit und das Land halb so viel Stabilität. Kron-Gouverneure sind ausgenommen."'
    loc = replace_loc_line(loc, 'EU5GOV_ENTRENCHMENT_TT', static)
    # Insert dynamic key directly after the static tooltip if not present yet.
    if 'EU5GOV_ENTRENCHMENT_TT_DYNAMIC:' not in loc:
        loc = loc.replace(' ' + static + '\n', ' ' + static + '\n ' + dynamic + '\n', 1)
    else:
        loc = replace_loc_line(loc, 'EU5GOV_ENTRENCHMENT_TT_DYNAMIC', dynamic)
    loc = replace_loc_line(loc, 'game_concept_eu5gov_entrenchment_desc', concept)
    write(path, loc)

# 6) Version + changelog.
metadata_path = '.metadata/metadata.json'
metadata = read(metadata_path)
metadata = replace_once(metadata, '"version": "0.2.8"', '"version": "0.2.9"', 'metadata version')
write(metadata_path, metadata)

changelog_path = 'CHANGELOG.md'
changelog = read(changelog_path)
entry = '''## 0.2.9

- Entrenchment now advances on the monthly country pulse instead of jumping once per year; the former annual balance is preserved by using `(2 + (ADM + DIP + MIL) / 100) / 12` each month.
- Added a shared `eu5gov_monthly_entrenchment_gain` script value so gameplay and GUI use the same formula.
- The Entrenchment lock tooltip now shows the Governor's live monthly gain and the current ADM/DIP/MIL values that produce it.
- Entrenchment in the Governor outliner is now displayed as a plain value with two decimals (for example `12.34`) instead of `12/100`.

'''
if '## 0.2.9' not in changelog:
    changelog = changelog.replace('# Changelog\n\n', '# Changelog\n\n' + entry, 1)
write(changelog_path, changelog)

print('Governor 0.2.9 patch applied successfully')
