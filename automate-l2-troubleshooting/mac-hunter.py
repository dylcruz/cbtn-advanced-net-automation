from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get

nr = InitNornir(config_file='config.yaml')
found_mac = False

target_mac = input('Enter the MAC address you wish to find: ')

def get_mac_addresses(task):
    global found_mac
    get_interfaces_result = task.run(task=napalm_get, getters='get_interfaces')
    task.host['interfaces'] = get_interfaces_result.result
    
    host_interfaces = task.host['interfaces']['get_interfaces']
    for interface in host_interfaces.keys():
        intf_mac = host_interfaces[interface]['mac_address']
        if intf_mac == target_mac:
            found_mac = True
            intf = interface
            print_info(task, intf)

def print_info(task, intf):
    print(f'Mac found on {task.host} - {intf}')
    get_lldp_result  = task.run(task=napalm_get, getters='get_lldp_neighbors')
    task.host['lldp_info'] = get_lldp_result.result
    
    neighbor_hostname = task.host['lldp_info']['get_lldp_neighbors'][intf][0]['hostname']
    neighbor_port = task.host['lldp_info']['get_lldp_neighbors'][intf][0]['port']
    print(f'Connected to host {neighbor_hostname} on their {neighbor_port} port.')

results = nr.run(get_mac_addresses)

if not found_mac:
    print(f'Mac address << {target_mac} >> not found on any switch in the inventory.')
