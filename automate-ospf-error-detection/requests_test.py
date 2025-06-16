from collections import defaultdict
from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
from rich import print as rprint
import ipaddress
import requests

nr = InitNornir('config.yaml')
requests.packages.urllib3.disable_warnings()

headers = { 'Accept': 'application/yang-data+json' }

config_dict = defaultdict(dict)
facts_dict = defaultdict(dict)
network_error = []
area_error = []
timer_error = []

def get_ospf(task):
    ospf_url = f'https://{task.host.hostname}:443/restconf/data/ospf-oper-data'
    ospf_send = requests.get(
        url=ospf_url, 
        headers=headers, 
        auth=(f'{task.host.username}', f'{task.host.password}'), 
        verify=False
        )
    
    inter_url = f'https://{task.host.hostname}:443/restconf/data/native/interface'
    inter_send = requests.get(
        url=inter_url, 
        headers=headers, 
        auth=(f'{task.host.username}', f'{task.host.password}'), 
        verify=False
        )
    
    task.host['ospf-facts'] = ospf_send.json()
    task.host['ospf-config'] = inter_send.json()

    config_interfaces = task.host['ospf-config']['Cisco-IOS-XE-native:interface']
    for inter_type in config_interfaces:
        interfaces = config_interfaces[inter_type]
        for intf in interfaces:
            try:
                name = intf['name']
                intlink = inter_type + str(name)
                ip = intf['ip']['address']['primary']['address']
                mask = intf['ip']['address']['primary']['mask']
                config_dict[f'{task.host}'][intlink] = [ip, mask]
            except KeyError:
                pass

    instances = task.host['ospf-facts']['Cisco-IOS-XE-ospf-oper:ospf-oper-data']['ospf-state']['ospf-instance']
    for instance in instances:
        areas = instance['ospf-area']
        for area in areas:
            try:
                area_id = area['area-id']
                ospf_interfaces = area['ospf-interface']
                for ospf_interface in ospf_interfaces:
                    intf_name = ospf_interface['name']
                    dead_intv = ospf_interface['dead-interval']
                    hello_intv = ospf_interface['hello-interval']
                    facts_dict[f'{task.host}'][intf_name] = [dead_intv, hello_intv, area_id]
            except KeyError:
                pass    

def get_cdp(task):
    cdp_url = f'https://{task.host.hostname}:443/restconf/data/cdp-neighbor-details'
    cdp_send = requests.get(
        url=cdp_url, 
        headers=headers, 
        auth=(f'{task.host.username}', f'{task.host.password}'), 
        verify=False
        )
    task.host['cdp-facts'] = cdp_send.json()
    cdp_neighbors = task.host['cdp-facts']['Cisco-IOS-XE-cdp-oper:cdp-neighbor-details']['cdp-neighbor-detail']
    for neighbor in cdp_neighbors:
        dev_name = neighbor['device-name']
        local_intf = neighbor['local-intf-name']
        port_id = neighbor['port-id']
        if local_intf.startswith('Gi'):
            try:
                local_ip = config_dict[f'{task.host}'][local_intf][0]
                local_mask = config_dict[f'{task.host}'][local_intf][1]
                local_network = ipaddress.ip_network(local_ip + '/' + local_mask, strict=False)
                remote_ip = config_dict[dev_name][port_id][0]
                remote_mask = config_dict[dev_name][port_id][1]
                remote_network = ipaddress.ip_network(remote_ip + '/' + remote_mask, strict=False)
                
                local_area = facts_dict[f'{task.host}'][local_intf][2]
                remote_area = facts_dict[dev_name][port_id][2]
                local_hello = facts_dict[f'{task.host}'][local_intf][1]
                remote_hello = facts_dict[dev_name][port_id][1]
                local_dead = facts_dict[f'{task.host}'][local_intf][0]
                remote_dead = facts_dict[dev_name][port_id][0]

                if not local_network == remote_network:
                    network_error.append(
                        (
                        f'NETWORK MISMATCH: {task.host} {local_intf} {local_network} -'
                        f' {dev_name} {port_id} {remote_network}'
                        )
                    )
                
                if not local_area == remote_area:
                    area_error.append(
                        (
                        f'AREA MISMATCH: {task.host} {local_intf} area {local_area} -'
                        f' {dev_name} {port_id} area {remote_area}'
                        )
                    )

                if not local_hello == remote_hello:
                    timer_error.append(
                        (
                        f'TIMER MISMATCH: {task.host} {local_intf} hello interval {local_hello} -'
                        f' {dev_name} {port_id} hello interval {remote_hello}'
                        )
                    )
                
                if not local_dead == remote_dead:
                    timer_error.append(
                        (
                        f'TIMER MISMATCH: {task.host} {local_intf} dead interval {local_dead} -'
                        f' {dev_name} {port_id} dead interval {remote_dead}'
                        )
                    )

            except KeyError:
                pass

ospf_results = nr.run(get_ospf)
cdp_results = nr.run(get_cdp)
# print_result(results)
# import ipdb
# ipdb.set_trace()

if network_error:
    for error in sorted(network_error): rprint(error)
if area_error:
    for error in sorted(area_error): rprint(error)
if timer_error:
    for error in sorted(timer_error): rprint(error)

rprint("\n[yellow]*** SCAN COMPLETED ***[/yellow]\n")