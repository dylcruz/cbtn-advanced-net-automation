from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def send_configs_file_test(task):
     task.run(task=send_configs_from_file, file='configs.txt')

result = nr.run(send_configs_file_test)
print_result(result)
