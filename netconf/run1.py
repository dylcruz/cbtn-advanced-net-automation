from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from ncclient import manager
from xml.dom.minidom import parseString

nr = InitNornir('config.yaml')

filt = """
 <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>
      </name>
    </interface>
 </interfaces>
"""

def get_device_config(task):
    DEVICE = {
    "host": task.host.hostname,
    "port": 830,
    "username": task.host.username,
    "password": task.host.password,
    "hostkey_verify": False
    }
    with manager.connect(**DEVICE) as m:
        response = m.get_config(source='running', filter=('subtree', filt))
        pretty_xml = parseString(response.xml).toprettyxml()
        return pretty_xml

results = nr.run(get_device_config)
print_result(results)
