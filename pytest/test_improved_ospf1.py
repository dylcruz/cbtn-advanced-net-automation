from nornir import InitNornir
from nornir.core.filter import F
from nornir_scrapli.tasks import send_command
import pytest

nr = InitNornir(config_file='config.yaml')

def check_ospf_neighbors_data_task(task):
    result = task.run(task=send_command, command="show ip ospf neighbor")
    task.host["ospf_neighbor_data"] = result.scrapli_response.genie_parse_output()

def get_spine_leaf_dev_names():
    devices = nr.filter(F(role='Spine') | F(role='Leaf')).inventory.hosts.keys()
    return devices

class TestOSPFNeighbors:
    NEIGHBOR_COUNT = {
        "Spine": 4,
        "Leaf": 2
    }

    @pytest.fixture(scope='class', autouse=True)
    def setup_teardown(self, pytestnr):
        pytestnr_filtered = pytestnr.filter(F(role='Spine') | F(role='Leaf'))
        pytestnr_filtered.run(task=check_ospf_neighbors_data_task)
        yield
        for host in pytestnr_filtered.inventory.hosts.values():
            host.data.pop('ospf_neighbor_data')

    @pytest.mark.parametrize(
        'device_name', get_spine_leaf_dev_names()
    )
    def test_ospf_neighbor_count(self, pytestnr, device_name):
        neighbors = []
        nr_host = pytestnr.inventory.hosts[device_name]
        role = nr_host['role']
        interfaces = nr_host['ospf_neighbor_data']['interfaces']
        for intf in interfaces:
            ospf_neighbor = interfaces[intf]['neighbors']
            for key in ospf_neighbor:
                neighbors.append(key)
        num_neighbors = len(neighbors)
        expected_neighbors = TestOSPFNeighbors.NEIGHBOR_COUNT[role]
        assert num_neighbors == expected_neighbors
