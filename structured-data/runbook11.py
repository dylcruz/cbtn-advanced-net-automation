from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file='config.yaml')

def pull_interfaces_info(task):
    interfaces_result = task.run(task=napalm_get, getters=['get_facts'])
    task.host['facts'] = interfaces_result.result
    uptime = task.host['facts']['get_facts']['uptime']
    vendor = task.host['facts']['get_facts']['vendor']

    if vendor == 'Juniper':
        rprint(f'{task.host} is a [green]Juniper[/green] device with an uptime of {uptime} seconds.')
    elif vendor == 'Cisco':
        rprint(f'{task.host} is a [yellow]Cisco[/yellow] device with an uptime of {uptime} seconds.')

resutls = nr.run(pull_interfaces_info)
# print_result(resutls)