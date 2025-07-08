from ncclient import manager
from xml.dom.minidom import parseString

DEVICE = {
    "host": "10.0.0.29",
    "port": 830,
    "username": "dylan",
    "password": "password1",
    "hostkey_verify": False
}

with manager.connect(**DEVICE) as m:
    response = m.get_config(source='running')
    pretty_xml = parseString(response.xml).toprettyxml()
    print(pretty_xml)
