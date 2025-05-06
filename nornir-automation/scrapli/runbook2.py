from nornir import InitNornir
from nornir_scrapli.tasks import send_commands
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

command_list = ['show ip interface brief', 'show version', 'show run']

def show_commands_test(task):
    task.run(task=send_commands, commands=command_list)

results = nr.run(show_commands_test)
print_result(results)
