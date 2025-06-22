from nornir_scrapli.tasks import send_command
from pytest_check import check_func

NEIGHBOR_COUNT = {"Spine": 4, "Leaf": 2}


@check_func
def pull_ospf(task):
    neighbor_rids = []
    result = task.run(task=send_command, command="show ip ospf neighbor")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interfaces"]
    for intf in interfaces:
        ospf_neighbors = interfaces[intf]["neighbors"]
        for rid in ospf_neighbors:
            neighbor_rids.append(rid)
    num_neighbors = len(neighbor_rids)

    role = task.host["role"]
    expected_neighbors = NEIGHBOR_COUNT.get(role)
    assert num_neighbors == expected_neighbors, f"{task.host} FAILED"


def test_nornir(nr):
    nr.run(task=pull_ospf)
