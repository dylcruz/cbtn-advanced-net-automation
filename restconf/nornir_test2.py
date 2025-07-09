from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
import requests


nr = InitNornir("config.yaml")
requests.packages.urllib3.disable_warnings()

headers = {"Accept": "application/yang-data+json"}


def restconf_test(task):
    url = f"https://{task.host.hostname}:443/restconf/data/native/router/Cisco-IOS-XE-bgp:bgp=65001/neighbor=1.1.1.1"
    response = requests.get(
        url=url,
        headers=headers,
        auth=((task.host.username, task.host.password)),
        verify=False,
    )
    task.host["facts"] = response.json()
    asn = task.host["facts"]["Cisco-IOS-XE-bgp:neighbor"]["remote-as"]
    peer_id = task.host["facts"]["Cisco-IOS-XE-bgp:neighbor"]["id"]
    print(f"Neighbor {peer_id} is part of remote ASN {asn}")
    return Result(task.host, response.json())


results = nr.run(restconf_test)
