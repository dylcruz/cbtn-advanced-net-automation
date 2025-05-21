from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print as rprint

nr = InitNornir(config_file='config.yaml')

def pull_structured_data(task):
    version_result = task.run(task=send_command, command='show ip bgp summary')
    task.host['facts'] = version_result.scrapli_response.genie_parse_output()
    neighbors = task.host['facts']['vrf']['default']['neighbor']
    for key in neighbors:
        updown = neighbors[key]['address_family']['']['up_down']
        rprint(f'{task.host} neighbor {key} updown vale is {updown}')

results = nr.run(pull_structured_data)
