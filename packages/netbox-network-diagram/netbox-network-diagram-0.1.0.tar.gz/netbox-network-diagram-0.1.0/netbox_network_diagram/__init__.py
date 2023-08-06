from extras.plugins import PluginConfig


class NetBoxNetworkDiagramConfig(PluginConfig):
    name = 'netbox_network_diagram'
    verbose_name = ' NetBox Network Diagram'
    description = 'A plugin to render network diagram in NetBox'
    version = '0.1'
    base_url = 'network-diagram'
    min_version = '3.4.0'


config = NetBoxNetworkDiagramConfig
