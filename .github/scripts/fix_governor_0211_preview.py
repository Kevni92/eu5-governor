from pathlib import Path

ROOT = Path('.')

def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')

def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8-sig')

def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected one match, found {n}')
    return text.replace(old, new, 1)

# Remove the scope-qualified named Script Values from 0.2.11; generic-action previews
# are more reliable when they read a persistent variable that existed before hover/confirm.
values_path = 'in_game/common/script_values/eu5gov_governor_values.txt'
values = read(values_path)
marker = '\n\n# Preview-safe political dismissal scale. Minimum 10, otherwise current Entrenchment.\n'
if marker in values:
    values = values.split(marker, 1)[0].rstrip() + '\n'
write(values_path, values)

# Persist the effective dismissal scale on every Governor. This is deliberately state that
# exists before a generic action is rendered, so the effect preview does not depend on a
# variable written earlier in the same pre-evaluated action chain.
effects_path = 'in_game/common/scripted_effects/eu5gov_governor_effects.txt'
effects = read(effects_path)
clamp = '    clamp_variable = { name = eu5gov_entrenchment min = 0 max = 100 }\n'
scale_update = '''    clamp_variable = { name = eu5gov_entrenchment min = 0 max = 100 }\n\n    set_variable = { name = eu5gov_dismissal_cost_scale value = 10 }\n    if = {\n        limit = { var:eu5gov_entrenchment > 10 }\n        set_variable = { name = eu5gov_dismissal_cost_scale value = var:eu5gov_entrenchment }\n    }\n'''
if 'set_variable = { name = eu5gov_dismissal_cost_scale value = 10 }' not in effects.split('eu5gov_tick_governor_entrenchment_effect',1)[1].split('}',1)[0]:
    effects = replace_once(effects, clamp, scale_update, 'monthly dismissal scale update')

start = effects.index('eu5gov_apply_governor_dismissal_cost_effect = {')
end_marker = '\n\n# Current scope: country.\n# Each serving Governor increases'
end = effects.index(end_marker, start)
helper = '''eu5gov_apply_governor_dismissal_cost_effect = {\n\tif = {\n\t\tlimit = {\n\t\t\thas_variable = eu5gov_governorship\n\t\t\tNOT = { has_estate = estate_type:crown_estate }\n\t\t}\n\n\t\tsave_scope_as = eu5gov_dismissed_governor\n\t\tvar:eu5gov_governorship ?= {\n\t\t\towner ?= {\n\t\t\t\tif = {\n\t\t\t\t\tlimit = { scope:eu5gov_dismissed_governor = { has_variable = eu5gov_dismissal_cost_scale } }\n\t\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\t\ttype = scope:eu5gov_dismissed_governor.estate_type\n\t\t\t\t\t\tvalue = {\n\t\t\t\t\t\t\tvalue = scope:eu5gov_dismissed_governor.var:eu5gov_dismissal_cost_scale\n\t\t\t\t\t\t\tmultiply = -0.01\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t\tadd_stability = {\n\t\t\t\t\t\tvalue = scope:eu5gov_dismissed_governor.var:eu5gov_dismissal_cost_scale\n\t\t\t\t\t\tmultiply = -0.50\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\telse = {\n\t\t\t\t\t# Backward-compatible floor for a Governor from a 0.2.10-or-older save\n\t\t\t\t\t# before the first monthly integrity tick has created the persistent scale.\n\t\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\t\ttype = scope:eu5gov_dismissed_governor.estate_type\n\t\t\t\t\t\tvalue = -0.10\n\t\t\t\t\t}\n\t\t\t\t\tadd_stability = -5\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n'''
effects = effects[:start] + helper + effects[end:]
# Clear the cached scale together with the Governor state, on both the character and location.
effects = effects.replace('\t\t\tremove_variable = eu5gov_entrenchment\n\t\t}\n', '\t\t\tremove_variable = eu5gov_entrenchment\n\t\t\tremove_variable = eu5gov_dismissal_cost_scale\n\t\t}\n', 1)
if '\tremove_variable = eu5gov_dismissal_cost_scale\n}' not in effects:
    effects = effects.replace('\tremove_variable = eu5gov_entrenchment\n}', '\tremove_variable = eu5gov_entrenchment\n\tremove_variable = eu5gov_dismissal_cost_scale\n}', 1)
write(effects_path, effects)

# Initialize the persistent floor on all new appointments/replacements. Keeping it on the
# location too is harmless and makes office-state inspection easier; the character copy is authoritative.
for path in [
    'in_game/common/character_interactions/eu5gov_governor_interactions.txt',
    'in_game/common/generic_actions/eu5gov_governor_outliner_actions.txt',
]:
    text = read(path)
    text = text.replace(
        'set_variable = { name = eu5gov_entrenchment value = 0 }\n',
        'set_variable = { name = eu5gov_entrenchment value = 0 }\n\t\t\t\tset_variable = { name = eu5gov_dismissal_cost_scale value = 10 }\n'
    )
    write(path, text)

# Replace the two generic-action preview blocks that still used scope-qualified named values.
actions_path = 'in_game/common/generic_actions/eu5gov_governor_outliner_actions.txt'
actions = read(actions_path)
old_replace = '''\t\t\t\t\t\t\tvar:eu5gov_governorship ?= {\n\t\t\t\t\t\t\t\towner ?= {\n\t\t\t\t\t\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\t\t\t\t\t\ttype = scope:eu5gov_replaced_governor.estate_type\n\t\t\t\t\t\t\t\t\t\tvalue = scope:eu5gov_replaced_governor.eu5gov_dismissal_satisfaction_delta\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\tadd_stability = scope:eu5gov_replaced_governor.eu5gov_dismissal_stability_delta\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n'''
new_replace = '''\t\t\t\t\t\t\tvar:eu5gov_governorship ?= {\n\t\t\t\t\t\t\t\towner ?= {\n\t\t\t\t\t\t\t\t\tif = {\n\t\t\t\t\t\t\t\t\t\tlimit = { scope:eu5gov_replaced_governor = { has_variable = eu5gov_dismissal_cost_scale } }\n\t\t\t\t\t\t\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\t\t\t\t\t\t\ttype = scope:eu5gov_replaced_governor.estate_type\n\t\t\t\t\t\t\t\t\t\t\tvalue = { value = scope:eu5gov_replaced_governor.var:eu5gov_dismissal_cost_scale multiply = -0.01 }\n\t\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\t\tadd_stability = { value = scope:eu5gov_replaced_governor.var:eu5gov_dismissal_cost_scale multiply = -0.50 }\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\telse = {\n\t\t\t\t\t\t\t\t\t\tadd_estate_satisfaction = { type = scope:eu5gov_replaced_governor.estate_type value = -0.10 }\n\t\t\t\t\t\t\t\t\t\tadd_stability = -5\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n'''
actions = replace_once(actions, old_replace, new_replace, 'replacement preview costs')
old_dismiss = '''\t\t\t\t\t\tvar:eu5gov_governorship ?= {\n\t\t\t\t\t\t\towner ?= {\n\t\t\t\t\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\t\t\t\t\ttype = scope:eu5gov_action_dismissed_governor.estate_type\n\t\t\t\t\t\t\t\t\tvalue = scope:eu5gov_action_dismissed_governor.eu5gov_dismissal_satisfaction_delta\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\tadd_stability = scope:eu5gov_action_dismissed_governor.eu5gov_dismissal_stability_delta\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t}\n'''
new_dismiss = '''\t\t\t\t\t\tvar:eu5gov_governorship ?= {\n\t\t\t\t\t\t\towner ?= {\n\t\t\t\t\t\t\t\tif = {\n\t\t\t\t\t\t\t\t\tlimit = { scope:eu5gov_action_dismissed_governor = { has_variable = eu5gov_dismissal_cost_scale } }\n\t\t\t\t\t\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\t\t\t\t\t\ttype = scope:eu5gov_action_dismissed_governor.estate_type\n\t\t\t\t\t\t\t\t\t\tvalue = { value = scope:eu5gov_action_dismissed_governor.var:eu5gov_dismissal_cost_scale multiply = -0.01 }\n\t\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\t\tadd_stability = { value = scope:eu5gov_action_dismissed_governor.var:eu5gov_dismissal_cost_scale multiply = -0.50 }\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t\telse = {\n\t\t\t\t\t\t\t\t\tadd_estate_satisfaction = { type = scope:eu5gov_action_dismissed_governor.estate_type value = -0.10 }\n\t\t\t\t\t\t\t\t\tadd_stability = -5\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t}\n'''
actions = replace_once(actions, old_dismiss, new_dismiss, 'dismissal preview costs')
write(actions_path, actions)

# Correct the changelog wording for the final implementation.
ch_path = 'CHANGELOG.md'
ch = read(ch_path)
ch = ch.replace(
    '- Added preview-safe dismissal cost Script Values with the 10-point minimum, so confirmation windows can show the real minimum cost instead of zero.',
    '- Added a persistent preview-safe dismissal-cost scale with a 10-point minimum, so confirmation windows can show the real minimum cost instead of zero.'
)
write(ch_path, ch)
