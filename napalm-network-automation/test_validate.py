from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_validate
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def validate_test(task):
    task.run(task=napalm_validate, src=f'validate-{task.host}.yaml')

results = nr.run(task=validate_test)
print_result(results)
