from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.tasks.data import load_yaml
import pytest

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
    task.host['loaded_vars'] = result.result

def get_vlans(task):
    vlan_list = []
    result = task.run(task=send_command, command='show vlan')
    task.host['vlan_data'] = result.scrapli_response.genie_parse_output()

def get_dev_names():
    devices = nr.inventory.hosts.keys()
    return devices

class TestVLANs:
    @pytest.fixture(scope='class', autouse=True)
    def setup_teardown(self, pytestnr):
        pytestnr.run(task=load_vars)
        pytestnr.run(task=get_vlans)
        yield
        for host in pytestnr.inventory.hosts.values():
            host.data.pop('vlan_data')
        
    @pytest.mark.parametrize('device_name', get_dev_names())
    def test_vlans_for_consistency(self, pytestnr, device_name):
        vlan_list = []
        nr_host = pytestnr.inventory.hosts[device_name]
        expected_vlans = nr_host['loaded_vars']['vlans']
        vlans = nr_host['vlan_data']['vlans']
        for vlan in vlans:
            if vlan in IGNORE_VLANS:
                continue
            vlan_id = int(vlan)
            vlan_name = vlans[vlan]['name']
            vlan_dict = {'id': vlan_id, 'name': vlan_name}
            vlan_list.append(vlan_dict)
        assert expected_vlans == vlan_list, f'{nr_host} FAILED'
