from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def test_this(task):
    interface_results = task.run(task=netmiko_send_command, command_string='show ip interface', use_genie=True)
    task.host['facts'] = interface_results.result

results = nr.run(test_this)
print_result(results)
