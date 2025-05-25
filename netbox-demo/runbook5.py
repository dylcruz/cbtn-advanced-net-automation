from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def nuggets(task):
    if task.host.platform != 'ios':
        print('Unsupported OS')
    else:
        task.run(task=napalm_configure, filename='napalm-configs.txt', dry_run=True)

results = nr.run(task=nuggets)
print_result(results)
