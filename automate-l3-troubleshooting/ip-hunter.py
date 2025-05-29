from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from collections import Counter

nr = InitNornir(config_file="config.yaml")

ip_addresses = []


def get_ip(task):
    get_interfaces_result = task.run(task=napalm_get, getters="get_interfaces_ip")
    task.host["interfaces"] = get_interfaces_result.result

    host_interfaces = task.host["interfaces"]["get_interfaces_ip"]
    for interface in host_interfaces.keys():
        intf_ipv4 = host_interfaces[interface]["ipv4"]
        for address, prefix in intf_ipv4.items():
            ip_addresses.append(f"{address}")

def locate_ip(task, addresses):
    get_interfaces_result = task.run(task=napalm_get, getters="get_interfaces_ip")
    task.host["interfaces"] = get_interfaces_result.result

    host_interfaces = task.host["interfaces"]["get_interfaces_ip"]
    for interface in host_interfaces.keys():
        intf_ipv4 = host_interfaces[interface]["ipv4"]
        for address, prefix in intf_ipv4.items():
            if address in addresses:
                print(f'DUPE FOUND - {task.host} - {interface} - {address}')

results = nr.run(get_ip)

dupes = [k for k, v in Counter(ip_addresses).items() if v > 1]

if dupes:
    nr.run(task=locate_ip, addresses=dupes)
else:
    print('No dupes found!')