from nornir import InitNornir
from pygnmi.client import gNMIclient, telemetryParser

nr = InitNornir('config.yaml')

subscribe = {
    'subscription': [
        {
            'path': 'openconfig:interfaces',
            'mode': 'sample',
            'sample_interval': 1000000000
        }
    ],
    'mode': 'stream',
    'encoding': 'json'
}

def test(task):
    with gNMIclient(
        target=(task.host.hostname, task.host.port),
        username=task.host.username,
        password=task.host.password,
        insecure=True,
    ) as client:
        respone = client.subscribe(subscribe=subscribe)
        for rsp in respone:
            print(telemetryParser(rsp))

results = nr.run(task=test)
