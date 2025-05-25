import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

nr.inventory.defaults.username = os.environ['USERNAME']
nr.inventory.defaults.password = os.environ['PASSWORD']

def run_command(task):
    if task.host.platform != 'ios':
        print('Unsupported OS')
    else:
        task.run(task=send_command, command='show ip interface brief')

results = nr.run(task=run_command)
print_result(results)
