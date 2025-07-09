import requests
from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir('config.yaml')
requests.packages.urllib3.disable_warnings()
headers = {
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json'
    }

def load_data(task):
    data = task.run(task=load_yaml, file=f'host_vars/{task.host}.yaml')
    task.host['facts'] = data.result

def configure_stuff(task, chained_url, headers):
    restconf_url = f'https://{task.host.hostname}:443/restconf/'
    response = requests.put(
        url=restconf_url+chained_url,
        headers=headers,
        auth=((
            task.host.username,
            task.host.password
            )),
        verify=False,
        json=task.host['facts']['configure_acl']
        )
    return (Result(task.host, response))

load_results = nr.run(load_data)
print_result(load_results)

configure_results = nr.run(
    task=configure_stuff,
    chained_url='data/openconfig-acl:acl',
    headers=headers
    )
print_result(configure_results)
