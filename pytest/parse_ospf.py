from nornir import InitNornir
from nornir_scrapli.tasks import send_command

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
    print(f"{task.host} has {num_neighbors} OSPF neighbors\n\n")


# nr.run(task=pull_ospf)
# import ipdb
# ipdb.set_trace()
