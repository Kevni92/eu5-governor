from pathlib import Path


def read(path):
    return Path(path).read_text(encoding='utf-8-sig')


def write_bom(path, text):
    Path(path).write_text('\ufeff' + text, encoding='utf-8')


# Dismissal floor: minimum 10% of max for non-Crown Governors.
p = 'in_game/common/scripted_effects/eu5gov_governor_effects.txt'
t = read(p)
old = '''# Current scope: serving governor character.\n# Voluntary dismissal/replacement is free for Crown characters. Otherwise the\n# Governor's Estate loses up to 100 percentage points of satisfaction and the\n# country loses up to 50 Stability, linearly scaled by Entrenchment.\neu5gov_apply_governor_dismissal_cost_effect = {\n\tif = {\n\t\tlimit = {\n\t\t\thas_variable = eu5gov_governorship\n\t\t\thas_variable = eu5gov_entrenchment\n\t\t\tNOT = { has_estate = estate_type:crown_estate }\n\t\t}\n\t\tsave_scope_as = eu5gov_dismissed_governor\n\t\tvar:eu5gov_governorship ?= {\n\t\t\towner ?= {\n\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\ttype = scope:eu5gov_dismissed_governor.estate_type\n\t\t\t\t\tvalue = {\n\t\t\t\t\t\tvalue = scope:eu5gov_dismissed_governor.var:eu5gov_entrenchment\n\t\t\t\t\t\tmultiply = -0.01\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tadd_stability = {\n\t\t\t\t\tvalue = scope:eu5gov_dismissed_governor.var:eu5gov_entrenchment\n\t\t\t\t\tmultiply = -0.50\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n'''
new = '''# Current scope: serving governor character.\n# Voluntary dismissal/replacement is free for Crown characters. Otherwise the\n# effective dismissal scale is max(10, Entrenchment): at the floor the Estate\n# loses 10 satisfaction and the country 5 Stability; at 100 the cost is 100/50.\neu5gov_apply_governor_dismissal_cost_effect = {\n\tif = {\n\t\tlimit = {\n\t\t\thas_variable = eu5gov_governorship\n\t\t\thas_variable = eu5gov_entrenchment\n\t\t\tNOT = { has_estate = estate_type:crown_estate }\n\t\t}\n\n\t\tset_variable = {\n\t\t\tname = eu5gov_dismissal_cost_scale\n\t\t\tvalue = var:eu5gov_entrenchment\n\t\t}\n\t\tif = {\n\t\t\tlimit = { var:eu5gov_dismissal_cost_scale < 10 }\n\t\t\tset_variable = { name = eu5gov_dismissal_cost_scale value = 10 }\n\t\t}\n\n\t\tsave_scope_as = eu5gov_dismissed_governor\n\t\tvar:eu5gov_governorship ?= {\n\t\t\towner ?= {\n\t\t\t\tadd_estate_satisfaction = {\n\t\t\t\t\ttype = scope:eu5gov_dismissed_governor.estate_type\n\t\t\t\t\tvalue = {\n\t\t\t\t\t\tvalue = scope:eu5gov_dismissed_governor.var:eu5gov_dismissal_cost_scale\n\t\t\t\t\t\tmultiply = -0.01\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tadd_stability = {\n\t\t\t\t\tvalue = scope:eu5gov_dismissed_governor.var:eu5gov_dismissal_cost_scale\n\t\t\t\t\tmultiply = -0.50\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\n\t\tremove_variable = eu5gov_dismissal_cost_scale\n\t}\n}\n'''
if t.count(old) != 1:
    raise SystemExit(f'dismissal effect match count: {t.count(old)}')
t = t.replace(old, new, 1)
write_bom(p, t)


# Replace the Governor outliner section with a vanilla-shaped version.
p = 'in_game/gui/outliner.gui'
t = read(p)
marker = 'types EU5GovOutlinerTypes'
start = t.index(marker)
brace = t.index('{', start)
depth = 0
end = None
for i in range(brace, len(t)):
    if t[i] == '{':
        depth += 1
    elif t[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break
if end is None:
    raise SystemExit('Could not find end of EU5GovOutlinerTypes')

replacement = r'''types EU5GovOutlinerTypes
{
    type eu5gov_governor_outliner_section = vbox {
        visible = "[Outliner.IsExpanded]"
        layoutpolicy_horizontal = expanding
        spacing = 0

        widget = {
            parentanchor = right
            size = { 405 31 }
            alwaystransparent = no

            button = {
                size = { 100% 100% }
                using = button_outliner_category_texture
                using = button_common_template

                modify_texture = {
                    using = color_government_texture
                    blend_mode = overlay
                    alpha = 0.45
                }

                icon = {
                    size = { 100% 100% }
                    ignore_layout = yes
                    alwaystransparent = yes
                    texture = "gfx/interface/buttons/outliner/outliner_goldframe.dds"
                    texture_density = 2
                    spriteType = corneredstretched
                    spriteborder = { 30 0 }
                }

                hbox = {
                    using = outliner_entry_margin
                    margin_right = 0
                    margin_left = 15
                    spacing = 5

                    icon = {
                        size = { 20 20 }
                        texture = "gfx/interface/icons/character_roles/regent.dds"
                        glow = {
                            name = "drop_shadow"
                            glow_radius = 3
                            color = { 0.0 0.0 0.0 1.0 }
                            alpha = 0.3
                        }
                    }

                    OutlinerTextBase = {
                        using = layoutpolicy_expanding
                        autoresize = no
                        align = left
                        fontsize = 15
                        text = "EU5GOV_OUTLINER_CATEGORY"
                    }

                    hbox = {
                        layoutpolicy_vertical = expanding
                        spacing = -5
                        righttoleft = yes

                        widget = {
                            size = { 34 -1 }
                            layoutpolicy_vertical = expanding
                            background = {
                                texture = "gfx/interface/component_tiles/balance_card_bg.dds"
                                texture_density = 2
                            }
                            widget = {
                                size = { 100% 100% }
                                ignore_layout = yes
                                alwaystransparent = yes
                                using = bg_cabinet_card_frame
                            }
                            OutlinerTextBase = {
                                parentanchor = center
                                size = { 100% 100% }
                                autoresize = yes
                                raw_text = "[GetDataModelSize(GetPlayer.MakeScope.GetMapKeys('eu5gov_governor_roster'))]/[GetDataModelSize(GetPlayer.MakeScope.GetMapKeys('eu5gov_governor_offices'))]"
                                default_format = "#T"
                            }
                        }

                        widget = {
                            size = { 23 23 }
                            background = {
                                texture = "gfx/interface/buttons/checkbox_bg_round.dds"
                                texture_density = 2
                            }
                            icon = {
                                visible = "[GetVariableSystem.Exists('eu5gov_governor_outliner_collapsed')]"
                                parentanchor = center
                                size = { 16 16 }
                                texture = "gfx/interface/buttons/flats/button_simple_right.dds"
                                using = color_gold
                                modify_texture = {
                                    using = overlay_window_texture
                                    blend_mode = overlay
                                    alpha = 1
                                }
                            }
                            icon = {
                                visible = "[Not(GetVariableSystem.Exists('eu5gov_governor_outliner_collapsed'))]"
                                parentanchor = center
                                size = { 16 16 }
                                position = { 0 2 }
                                texture = "gfx/interface/buttons/flats/button_simple_down.dds"
                                using = color_gold
                                modify_texture = {
                                    using = overlay_window_texture
                                    blend_mode = overlay
                                    alpha = 1
                                }
                            }
                            widget = {
                                size = { 100% 100% }
                                ignore_layout = yes
                                alwaystransparent = yes
                                using = circular_wood_frame
                            }
                        }
                    }
                }

                action_tooltip = {
                    click_type = left
                    click_mode = single
                    title = "EU5GOV_OUTLINER_CATEGORY"
                    description = "EU5GOV_OUTLINER_HEADER_TT"
                    on_action = "[GetVariableSystem.Toggle('eu5gov_governor_outliner_collapsed')]"
                }
                tooltipwidget = { BasicFunctionalTooltip = {} }
            }
        }

        vbox = {
            visible = "[Not(GetVariableSystem.Exists('eu5gov_governor_outliner_collapsed'))]"
            layoutpolicy_horizontal = expanding
            spacing = 0
            datamodel = "[GetPlayer.MakeScope.GetMapKeys('eu5gov_governor_offices')]"

            item = {
                widget = {
                    parentanchor = right
                    size = { 405 30 }
                    alwaystransparent = yes
                    datacontext = "[Scope.GetLocation]"

                    OutlinerButtonBase = {
                        parentanchor = right
                        size = { 95% 30 }

                        hbox = {
                            visible = "[Not(Location.MakeScope.GetVariable('eu5gov_governor').IsSet)]"
                            margin = { 10 0 }
                            spacing = 5

                            widget = {
                                size = { 28 28 }
                                portrait_standard_head_button = {
                                    datacontext = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter]"
                                    size = { 28 28 }
                                    alwaystransparent = yes
                                    blockoverride "character_tooltip" { tooltip_enabled = no }
                                    blockoverride "character_contextmenu" {}
                                    blockoverride "button_setup" {}
                                    blockoverride "rightclick" {}
                                    blockoverride "hover" {}
                                }
                                action_button = {
                                    size = { 28 28 }
                                    ignore_layout = yes
                                    parentanchor = center
                                    title = "EU5GOV_PORTRAIT_APPOINT_TT"
                                    description = "EU5GOV_PORTRAIT_APPOINT_DESC"
                                    actor = "[GetPlayer]"
                                    parameter = {
                                        parameter_name = "target_1"
                                        parameter_value = "[Scope.GetLocation]"
                                    }
                                    left_action = { action_name = "eu5gov_appoint_governor_from_outliner" }
                                    tooltipwidget = { BasicFunctionalTooltip = {} }
                                }
                            }

                            vbox = {
                                layoutpolicy_horizontal = expanding
                                spacing = 0
                                OutlinerTextBase = {
                                    layoutpolicy_horizontal = expanding
                                    align = left
                                    text = "EU5GOV_EMPTY_SLOT"
                                    default_format = "#S"
                                }
                                OutlinerTextBase = {
                                    layoutpolicy_horizontal = expanding
                                    align = left
                                    fontsize = 12
                                    maximumsize = { 230 -1 }
                                    text = "[Location.GetName]"
                                }
                            }

                            OutlinerTextBase = {
                                autoresize = yes
                                text = "EU5GOV_EMPTY_SLOT_STATUS"
                                default_format = "#N"
                            }
                        }

                        hbox = {
                            visible = "[Location.MakeScope.GetVariable('eu5gov_governor').IsSet]"
                            margin = { 10 0 }
                            spacing = 5

                            widget = {
                                size = { 28 28 }
                                portrait_standard_head_button = {
                                    datacontext = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter]"
                                    size = { 28 28 }
                                    alwaystransparent = yes
                                    blockoverride "character_contextmenu" {}
                                }
                                action_button = {
                                    size = { 28 28 }
                                    ignore_layout = yes
                                    parentanchor = center
                                    title = "EU5GOV_PORTRAIT_CHANGE_TT"
                                    description = "EU5GOV_PORTRAIT_CHANGE_DESC"
                                    actor = "[GetPlayer]"
                                    parameter = {
                                        parameter_name = "target_1"
                                        parameter_value = "[Scope.GetLocation]"
                                    }
                                    left_action = { action_name = "eu5gov_change_governor_from_outliner" }
                                    tooltipwidget = { BasicFunctionalTooltip = {} }
                                }
                            }

                            vbox = {
                                layoutpolicy_horizontal = expanding
                                spacing = 0
                                OutlinerTextBase = {
                                    layoutpolicy_horizontal = expanding
                                    align = left
                                    maximumsize = { 155 -1 }
                                    autoresize = yes
                                    text = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.GetName]"
                                    default_format = "#L"
                                }
                                OutlinerTextBase = {
                                    layoutpolicy_horizontal = expanding
                                    align = left
                                    fontsize = 12
                                    maximumsize = { 155 -1 }
                                    text = "[Location.GetName]"
                                }
                            }

                            vbox = {
                                min_width = 135
                                align = right
                                spacing = 0
                                OutlinerTextBase = {
                                    align = right
                                    autoresize = yes
                                    text = "[SelectLocalization(EqualTo_CFixedPoint(Location.MakeScope.GetVariable('eu5gov_governor_role').GetValue, '(CFixedPoint)2'), 'EU5GOV_ROLE_INTEGRATION', SelectLocalization(EqualTo_CFixedPoint(Location.MakeScope.GetVariable('eu5gov_governor_role').GetValue, '(CFixedPoint)3'), 'EU5GOV_ROLE_COLONIAL', 'EU5GOV_ROLE_NORMAL'))]"
                                }
                                OutlinerTextBase = {
                                    align = right
                                    autoresize = yes
                                    fontsize = 12
                                    raw_text = "[Localize('EU5GOV_ENTRENCHMENT_SHORT')] [Location.MakeScope.GetVariable('eu5gov_entrenchment').GetValue|0]/100"
                                }
                            }
                        }

                        blockoverride "button_setup" {
                            action_tooltip = {
                                visible = "[Not(Location.MakeScope.GetVariable('eu5gov_governor').IsSet)]"
                                click_type = left
                                click_mode = single
                                title = "EU5GOV_OPEN_RESIDENCE"
                                description = "EU5GOV_EMPTY_SLOT_TT"
                                on_action = "[ShowLocation(Location.Self)]"
                            }
                            action_tooltip = {
                                visible = "[Location.MakeScope.GetVariable('eu5gov_governor').IsSet]"
                                click_type = left
                                click_mode = single
                                title = "EU5GOV_OPEN_RESIDENCE"
                                description = "EU5GOV_OCCUPIED_SLOT_TT"
                                on_action = "[ShowLocation(Location.Self)]"
                            }
                            action_tooltip = {
                                visible = "[Location.MakeScope.GetVariable('eu5gov_governor').IsSet]"
                                click_type = right
                                click_mode = single
                                cursor = "country_menu"
                                title = "EU5GOV_OUTLINER_RIGHT_CLICK"
                                description = "EU5GOV_OUTLINER_RIGHT_CLICK_DESC"
                                on_action = "[PdxGuiWidget.ToggleContextMenu]"
                            }
                            tooltipwidget = { BasicFunctionalTooltip = {} }

                            contextmenu_enabled = "[Location.MakeScope.GetVariable('eu5gov_governor').IsSet]"
                            contextmenu_widget = {
                                ContextMenuBase = {
                                    blockoverride "contextmenu_content" {
                                        ContextMenuSection = {
                                            blockoverride "title_icon" {
                                                portrait_standard_head_button = {
                                                    datacontext = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter]"
                                                    size = { 24 24 }
                                                    blockoverride "character_contextmenu" {}
                                                }
                                            }
                                            blockoverride "title_text" {
                                                raw_text = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.GetName]"
                                            }
                                            blockoverride "contextmenu_entries" {
                                                ContextMenuEntry = {
                                                    blockoverride "entry_button" {
                                                        button = {
                                                            using = contextmenu_entry_button_template
                                                            enabled = "[Not(EqualTo_CFixedPoint(Location.MakeScope.GetVariable('eu5gov_governor_role').GetValue, '(CFixedPoint)1'))]"
                                                            blockoverride "click_action" {
                                                                title = "EU5GOV_ROLE_NORMAL"
                                                                description = "EU5GOV_ROLE_NORMAL_TT"
                                                                on_action = "[GetScriptedGui('eu5gov_set_role_normal').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('office', Location.MakeScope).End)]"
                                                            }
                                                            blockoverride "entry_text" { text = "EU5GOV_ROLE_NORMAL" }
                                                        }
                                                    }
                                                }
                                                ContextMenuEntry = {
                                                    blockoverride "entry_button" {
                                                        button = {
                                                            using = contextmenu_entry_button_template
                                                            enabled = "[Not(EqualTo_CFixedPoint(Location.MakeScope.GetVariable('eu5gov_governor_role').GetValue, '(CFixedPoint)2'))]"
                                                            blockoverride "click_action" {
                                                                title = "EU5GOV_ROLE_INTEGRATION"
                                                                description = "EU5GOV_ROLE_INTEGRATION_TT"
                                                                on_action = "[GetScriptedGui('eu5gov_set_role_integration').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('office', Location.MakeScope).End)]"
                                                            }
                                                            blockoverride "entry_text" { text = "EU5GOV_ROLE_INTEGRATION" }
                                                        }
                                                    }
                                                }
                                                ContextMenuEntry = {
                                                    blockoverride "entry_button" {
                                                        button = {
                                                            using = contextmenu_entry_button_template
                                                            enabled = "[Not(EqualTo_CFixedPoint(Location.MakeScope.GetVariable('eu5gov_governor_role').GetValue, '(CFixedPoint)3'))]"
                                                            blockoverride "click_action" {
                                                                title = "EU5GOV_ROLE_COLONIAL"
                                                                description = "EU5GOV_ROLE_COLONIAL_TT"
                                                                on_action = "[GetScriptedGui('eu5gov_set_role_colonial').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('office', Location.MakeScope).End)]"
                                                            }
                                                            blockoverride "entry_text" { text = "EU5GOV_ROLE_COLONIAL" }
                                                        }
                                                    }
                                                }
                                                ContextMenuEntry = {
                                                    blockoverride "entry_button" {
                                                        button = {
                                                            using = contextmenu_entry_button_template
                                                            enabled = "[Location.MakeScope.GetVariable('eu5gov_governor').IsSet]"
                                                            blockoverride "button_texture" { using = button_regular_red_texture }
                                                            blockoverride "click_action" {
                                                                title = "EU5GOV_DISMISS"
                                                                description = "EU5GOV_DISMISS_TT"
                                                                on_action = "[GetScriptedGui('eu5gov_dismiss_governor_sgui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('office', Location.MakeScope).End)]"
                                                            }
                                                            blockoverride "entry_text" { text = "EU5GOV_DISMISS" }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }

                            ondoubleclick = "[PanToLocation(Location.Self)]"
                            onmousehierarchyenter = "[PdxGuiWidget.SetHighlightLocation(Location.Self)]"
                        }
                    }
                }
            }
        }
    }
}'''

t = t[:start] + replacement + t[end:]
write_bom(p, t)
