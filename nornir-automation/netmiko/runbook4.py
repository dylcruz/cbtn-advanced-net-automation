from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

commands = ['router eigrp 12', 'network 10.0.0.0', 'network 192.168.55.0']

nr = InitNornir(config_file='config.yaml')

def test_send_config_nm(task):
    task.run(task=netmiko_send_config, config_file='configs.txt')

results = nr.run(task=test_send_config_nm)
print_result(results)
