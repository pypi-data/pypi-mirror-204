from extras.plugins import PluginMenu, PluginMenuItem

menu = PluginMenu(
    label='Network Diagram',
    icon_class='mdi mdi-sitemap',
    groups=(
        ('Network Diagram', (
            PluginMenuItem(
                link='plugins:netbox_network_diagram:network_diagram',
                link_text='Network Diagram',
            ),
        ),),
    ),
)