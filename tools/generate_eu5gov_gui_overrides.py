from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen

VANILLA_REF = "879fb81040a873a5eeb9a9a034621fc6572571e5"
RAW_BASE = (
    "https://raw.githubusercontent.com/HLJSXK/eu5-towards-victory/"
    f"{VANILLA_REF}/reference_game_files/game/in_game/gui"
)
ROOT = Path(__file__).resolve().parents[1]
GUI_DIR = ROOT / "in_game" / "gui"


def fetch_vanilla(name: str) -> str:
    with urlopen(f"{RAW_BASE}/{name}", timeout=30) as response:
        return response.read().decode("utf-8-sig")


GOVERNOR_OUTLINER_TYPE = r'''

# Character Governors: native-outliner section.  This type is instantiated inside
# the vanilla outliner's own scroll widget below the engine-managed entries.
types EU5GovOutlinerTypes
{
    type eu5gov_governor_outliner_section = vbox {
        layoutpolicy_horizontal = expanding
        spacing = 0

        button = {
            parentanchor = right
            size = { 405 31 }
            using = button_outliner_category_texture
            using = button_common_template
            tooltip = "EU5GOV_OUTLINER_HEADER_TT"
            onclick = "[GetVariableSystem.Toggle('eu5gov_governor_outliner_collapsed')]"

            modify_texture = {
                using = color_government_texture
                blend_mode = overlay
                alpha = 0.45
            }

            hbox = {
                margin = { 10 3 }
                spacing = 6

                icon = {
                    size = { 22 22 }
                    texture = "gfx/interface/icons/character_roles/regent.dds"
                }

                text_single = {
                    layoutpolicy_horizontal = expanding
                    align = left|nobaseline
                    using = Font_Type_Headers
                    text = "EU5GOV_OUTLINER_CATEGORY"
                }

                text_single = {
                    autoresize = yes
                    raw_text = "[GetDataModelSize(GetPlayer.MakeScope.GetMapKeys('eu5gov_governor_roster'))]/[GetDataModelSize(GetPlayer.MakeScope.GetMapKeys('eu5gov_governor_offices'))]"
                    tooltip = "EU5GOV_OUTLINER_COUNT_TT"
                }

                text_single = {
                    autoresize = yes
                    text = "[SelectLocalization(GetVariableSystem.Exists('eu5gov_governor_outliner_collapsed'), 'EU5GOV_OUTLINER_EXPAND_MARK', 'EU5GOV_OUTLINER_COLLAPSE_MARK')]"
                }
            }
        }

        vbox = {
            visible = "[Not(GetVariableSystem.Exists('eu5gov_governor_outliner_collapsed'))]"
            layoutpolicy_horizontal = expanding
            spacing = 0
            datamodel = "[GetPlayer.MakeScope.GetMapKeys('eu5gov_governor_offices')]"

            item = {
                OutlinerButtonBase = {
                    parentanchor = right
                    size = { 405 31 }
                    datacontext = "[Scope.GetLocation]"

                    hbox = {
                        visible = "[Not(Location.MakeScope.GetVariable('eu5gov_governor').IsSet)]"
                        using = outliner_entry_margin
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
                                maximumsize = { 245 -1 }
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
                        using = outliner_entry_margin
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
                                maximumsize = { 185 -1 }
                                autoresize = yes
                                text = "[Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.GetName]"
                                default_format = "#L"
                            }
                            OutlinerTextBase = {
                                layoutpolicy_horizontal = expanding
                                align = left
                                fontsize = 12
                                maximumsize = { 185 -1 }
                                text = "[Location.GetName]"
                            }
                        }

                        vbox = {
                            min_width = 145
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
                                tooltip = "EU5GOV_ENTRENCHMENT_TT"
                            }
                        }
                    }

                    blockoverride "button_setup" {
                        action_tooltip = {
                            click_type = left
                            click_mode = single
                            title = "EU5GOV_OPEN_RESIDENCE"
                            on_action = "[ShowLocation(Location.Self)]"
                        }

                        action_tooltip = {
                            visible = "[Location.MakeScope.GetVariable('eu5gov_governor').IsSet]"
                            click_type = right
                            click_mode = single
                            cursor = "country_menu"
                            title = "EU5GOV_OUTLINER_RIGHT_CLICK"
                            on_action = "[PdxGuiWidget.ToggleContextMenu]"
                        }

                        tooltip_enabled = yes
                        tooltip = "[SelectLocalization(Location.MakeScope.GetVariable('eu5gov_governor').IsSet, 'EU5GOV_OCCUPIED_SLOT_TT', 'EU5GOV_EMPTY_SLOT_TT')]"

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
                                                enabled = "[GetScriptedGui('eu5gov_set_role_normal').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                blockoverride "click_action" {
                                                    title = "EU5GOV_ROLE_NORMAL_TT"
                                                    on_action = "[GetScriptedGui('eu5gov_set_role_normal').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                }
                                                blockoverride "entry_text" { text = "EU5GOV_ROLE_NORMAL" }
                                            }
                                            ContextMenuEntry = {
                                                enabled = "[GetScriptedGui('eu5gov_set_role_integration').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                blockoverride "click_action" {
                                                    title = "EU5GOV_ROLE_INTEGRATION_TT"
                                                    on_action = "[GetScriptedGui('eu5gov_set_role_integration').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                }
                                                blockoverride "entry_text" { text = "EU5GOV_ROLE_INTEGRATION" }
                                            }
                                            ContextMenuEntry = {
                                                enabled = "[GetScriptedGui('eu5gov_set_role_colonial').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                blockoverride "click_action" {
                                                    title = "EU5GOV_ROLE_COLONIAL_TT"
                                                    on_action = "[GetScriptedGui('eu5gov_set_role_colonial').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                }
                                                blockoverride "entry_text" { text = "EU5GOV_ROLE_COLONIAL" }
                                            }
                                            ContextMenuEntry = {
                                                enabled = "[GetScriptedGui('eu5gov_dismiss_governor_sgui').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                blockoverride "click_action" {
                                                    title = "EU5GOV_DISMISS_TT"
                                                    on_action = "[GetScriptedGui('eu5gov_dismiss_governor_sgui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('governor', Location.MakeScope.GetVariable('eu5gov_governor').GetCharacter.MakeScope).End)]"
                                                }
                                                blockoverride "entry_text" { text = "EU5GOV_DISMISS" }
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
'''.strip("\n")


def patch_outliner(source: str) -> str:
    window_marker = 'window = {\n\tname = "outliner"'
    if source.count(window_marker) != 1:
        raise RuntimeError("Could not uniquely locate vanilla outliner window")
    source = source.replace(
        window_marker,
        GOVERNOR_OUTLINER_TYPE + "\n\n" + window_marker,
        1,
    )

    native_entries_marker = '''\t\t\t\t\t\t\t\t\t\t\tcontainer = {
\t\t\t\t\t\t\t\t\t\t\t\tvisible = no
\t\t\t\t\t\t\t\t\t\t\t\tname = "outliner_outside_scrollarea_entries"
\t\t\t\t\t\t\t\t\t\t\t}
'''
    if source.count(native_entries_marker) != 1:
        raise RuntimeError("Could not uniquely locate vanilla outliner entry container")
    source = source.replace(
        native_entries_marker,
        native_entries_marker
        + "\n\t\t\t\t\t\t\t\t\t\t\teu5gov_governor_outliner_section = {}\n",
        1,
    )
    return source


def patch_character_lateralview(source: str) -> str:
    role_text = 'text = "[CharacterRoleMask.GetRolesName]"'
    if source.count(role_text) != 1:
        raise RuntimeError("Could not uniquely locate CharacterRoleMask role text")

    role_pos = source.index(role_text)
    block_start = source.rfind("\t\t\t\t\t\t\ttext_single = {", 0, role_pos)
    if block_start < 0:
        raise RuntimeError("Could not locate role text widget start")

    open_brace = source.index("{", block_start)
    depth = 0
    block_end = None
    for idx in range(open_brace, len(source)):
        char = source[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                block_end = idx + 1
                break
    if block_end is None:
        raise RuntimeError("Could not locate role text widget end")

    vanilla_block = source[block_start:block_end]
    if "visible =" in vanilla_block:
        raise RuntimeError("Vanilla role text block unexpectedly already has visibility logic")

    vanilla_block = vanilla_block.replace(
        "\n\t\t\t\t\t\t\t\ttext = \"[CharacterRoleMask.GetRolesName]\"",
        "\n\t\t\t\t\t\t\t\tvisible = \"[Not(CharacterLateralview.GetCharacter.MakeScope.GetVariable('eu5gov_governorship').IsSet)]\""
        "\n\t\t\t\t\t\t\t\ttext = \"[CharacterRoleMask.GetRolesName]\"",
        1,
    )

    governor_block = '''
\t\t\t\t\t\t\ttext_single = {
\t\t\t\t\t\t\t\tminimumsize = { -1 20 }
\t\t\t\t\t\t\t\tautoresize = yes
\t\t\t\t\t\t\t\tvisible = "[CharacterLateralview.GetCharacter.MakeScope.GetVariable('eu5gov_governorship').IsSet]"
\t\t\t\t\t\t\t\ttext = "EU5GOV_CHARACTER_ROLE_GOVERNOR"
\t\t\t\t\t\t\t\ttooltip = "EU5GOV_CHARACTER_ROLE_GOVERNOR_TT"
\t\t\t\t\t\t\t}'''

    return source[:block_start] + vanilla_block + governor_block + source[block_end:]


def main() -> None:
    GUI_DIR.mkdir(parents=True, exist_ok=True)

    outliner = patch_outliner(fetch_vanilla("outliner.gui"))
    character_view = patch_character_lateralview(fetch_vanilla("character_lateralview.gui"))

    (GUI_DIR / "outliner.gui").write_text("\ufeff" + outliner, encoding="utf-8")
    (GUI_DIR / "character_lateralview.gui").write_text("\ufeff" + character_view, encoding="utf-8")


if __name__ == "__main__":
    main()
