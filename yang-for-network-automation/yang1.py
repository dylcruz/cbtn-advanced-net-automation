from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir('config.yaml')

def yang_suite_test(task):
    task.run(task=netconf_get_config, source='running', filters='/native/hostname', filter_type='xpath')

results = nr.run(yang_suite_test)
print_result(results)
