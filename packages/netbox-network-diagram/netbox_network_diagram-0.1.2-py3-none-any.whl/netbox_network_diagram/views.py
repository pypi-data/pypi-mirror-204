import json
from django.shortcuts import render
from django.views.generic import View
from dcim.models import (
    Device, 
    Cable, 
    Interface,
)


#
# NetworkDiagram views
#
class NetworkDiagramView(View):
    def get(self, request):
        # 全ての Device を nodes に追加します。
        nodes = []
        device_list = Device.objects.all()
        for d in device_list:
            location = ""
            if d.location != None:
                location = d.location.name

            nodes.append({ 
                "name": d.name, 
                "group": location, 
                "meta": {
                    "description": d.description,
                }, 
                "icon": "/static/netbox_network_diagram/img/switch.png" 
            })
        
        # Cable の接続情報を元に Device 間の接続を links に追加します。
        links = []
        cable_list = Cable.objects.all()
        for c in cable_list:
            if len(c.a_terminations) != 1 and len(c.b_terminations) != 1:
                continue

            a_termination = c.a_terminations[0]
            b_termination = c.b_terminations[0]

            if not isinstance(a_termination, Interface) or not isinstance(b_termination, Interface):
                continue

            if_source = a_termination.name
            if_target = b_termination.name

            if a_termination.device == None or b_termination.device == None:
                continue

            source = a_termination.device.name
            target = b_termination.device.name

            links.append({
                "source": source,
                "target": target,
                "meta": {
                    "interface": {
                        "source": if_source,
                        "target": if_target,
                    },
                    "description": "",
                }
            })
        
        # inet-henge で描画できる形式にします。
        data = { "nodes": nodes, "links": links}

        return render(
            request,
            "netbox_network_diagram/index.html",
            {"data": json.dumps(data)},
        )
