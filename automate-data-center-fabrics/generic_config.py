from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir('config.yaml')

def push_base_config(task):
    task.run(task=send_configs_from_file, file='basepusher.txt')

results = nr.run(push_base_config)
print_result(results)
