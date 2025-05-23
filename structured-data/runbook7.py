from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.functions import print_structured_result
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def test_this(task):
    task.run(task=send_command, command='show ip interface')

results = nr.run(test_this)
print_structured_result(results, parser='genie')
