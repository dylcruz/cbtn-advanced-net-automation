from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def send_cmd(task):
    task.run(task=send_command, command='show cdp neighbors')

north_east_targets = nr.filter(region='north', coast='east')
results = north_east_targets.run(task=send_cmd)
print_result(results)
