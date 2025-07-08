import xmltodict
from ncclient import manager
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from pprint import pprint

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
        # pretty_xml = parseString(response.xml).toprettyxml()
        # return pretty_xml
        dict_result = xmltodict.parse(response.xml)
        task.host['facts'] = dict_result
        interfaces = task.host['facts']['rpc-reply']['data']['interfaces-state']['interface']
        try:
            for intf in interfaces:
                interface_name = intf['name']
                print(f'{interface_name}\'s in-unicast-packets is greater than zero.')
        except TypeError:
                interface_name = interfaces['name']
                print(f'{interface_name}\'s in-unicast-packets are greater than zero.')

results = nr.run(get_yang)
print_result(results)
