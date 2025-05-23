from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def test_this(task):
    task.run(task=netmiko_send_command, command_string='show clock', use_textfsm=True)

results = nr.run(test_this)
print_result(results)
