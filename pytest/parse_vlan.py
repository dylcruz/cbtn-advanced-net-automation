from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file='config.yaml')

IGNORE_VLANS = [
    '1',
    '1002',
    '1003',
    '1004',
    '1005'
]

def load_vars(task):
    result = task.run(task=load_yaml, file=f'desired-state/vlans/{task.host}.yaml')
    loaded = result.result
    return loaded

def get_vlans(task):
    vlan_list = []
    
    result = task.run(task=send_command, command='show vlan')
    task.host['facts'] = result.scrapli_response.genie_parse_output()
    vlans = task.host['facts']['vlans']
    
    for vlan in vlans:
        if vlan in IGNORE_VLANS:
            continue
        
        vlan_id = int(vlan)
        vlan_name = vlans[vlan]['name']
        vlan_dict = {'id': vlan_id, 'name': vlan_name}
        vlan_list.append(vlan_dict)
    
    expected = load_vars(task)
    print(expected['vlans'])

nr.run(task=get_vlans)
# import ipdb
# ipdb.set_trace()
