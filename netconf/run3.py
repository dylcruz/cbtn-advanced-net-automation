from ncclient import manager
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from xml.dom.minidom import parseString

nr = InitNornir('config.yaml')

def get_yang(task):
    DEVICE = {
    "host": task.host.hostname,
    "port": 830,
    "username": task.host.username,
    "password": task.host.password,
    "hostkey_verify": False
    }
    with manager.connect(**DEVICE) as m:
        response = m.get(filter=('xpath', 'interfaces-state//statistics[in-unicast-pkts > 0]'))
        pretty_xml = parseString(response.xml).toprettyxml()
        return pretty_xml

results = nr.run(get_yang)

print_result(results)
