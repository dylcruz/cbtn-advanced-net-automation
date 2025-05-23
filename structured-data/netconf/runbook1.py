from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def pull_netconf_stuff(task):
    result = task.run(task=netconf_get_config, source='running')

results = nr.run(task=pull_netconf_stuff)
print_result(results)
