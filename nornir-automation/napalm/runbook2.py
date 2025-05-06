from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def all_device_ping(task):
    task.run(task=napalm_ping, dest='10.0.0.1', vrf='MGMT')

results = nr.run(task=all_device_ping)
print_result(results)
