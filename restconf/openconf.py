from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
import requests


nr = InitNornir('config.yaml')
requests.packages.urllib3.disable_warnings()

headers = { 'Accept': 'application/yang-data+json'}

def restconf_test(task):
    url = f'https://{task.host.hostname}:443/restconf/data/openconfig-interfaces:interfaces?content=config'
    response = requests.get(
        url=url,
        headers=headers,
        auth=((
            task.host.username,
            task.host.password
            )),
        verify=False
        )
    return (Result(task.host, response.text))

results = nr.run(restconf_test)
print_result(results)
