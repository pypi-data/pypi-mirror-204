from extras.plugins import PluginMenu, PluginMenuItem, PluginMenuButton
from utilities.choices import ButtonColorChoices

menu = PluginMenu(
    label="Risk Assessment",
    icon_class="mdi mdi-spider",
    groups=(
        (
            "Threat",
            (
                PluginMenuItem(
                    permissions=["nb_risk.view_threatsource"],
                    link="plugins:nb_risk:threatsource_list",
                    link_text="Threat Sources",
                    buttons=(
                        PluginMenuButton(
                            "plugins:nb_risk:threatsource_add",
                            "Add",
                            "mdi mdi-plus-thick",
                            ButtonColorChoices.GREEN,
                            permissions=["nb_risk.add_threatsource"],
                        ),
                    ),
                ),
                PluginMenuItem(
                    permissions=["nb_risk.view_threatevent"],
                    link="plugins:nb_risk:threatevent_list",
                    link_text="Threat Events",
                    buttons=(
                        PluginMenuButton(
                            "plugins:nb_risk:threatevent_add",
                            "Add",
                            "mdi mdi-plus-thick",
                            ButtonColorChoices.GREEN,
                            permissions=["nb_risk.add_threatevent"],
                        ),
                    ),
                ),
            ),
        ),
        (
            "Vulnerability",
            (
                PluginMenuItem(
                    permissions=["nb_risk.view_vulnerability"],
                    link="plugins:nb_risk:vulnerability_list",
                    link_text="Vulnerabilities",
                    buttons=(
                        PluginMenuButton(
                            "plugins:nb_risk:vulnerability_add",
                            "Add",
                            "mdi mdi-plus-thick",
                            ButtonColorChoices.GREEN,
                            permissions=["nb_risk.add_vulnerability"],
                        ),
                        PluginMenuButton(
                            "plugins:nb_risk:vulnerability_search",
                            "Search",
                            "mdi mdi-magnify",
                            ButtonColorChoices.BLUE,
                            permissions=["nb_risk.view_vulnerability"],
                        ),
                    ),
                ),
            ),
        ),
        (
            "Risk",
            (
                PluginMenuItem(
                    permissions=["nb_risk.view_risk"],
                    link="plugins:nb_risk:risk_list",
                    link_text="Risks",
                    buttons=(
                        PluginMenuButton(
                            "plugins:nb_risk:risk_add",
                            "Add",
                            "mdi mdi-plus-thick",
                            ButtonColorChoices.GREEN,
                            permissions=["nb_risk.add_risk"],
                        ),
                    ),
                ),
            ),
        ),
    ),
)
