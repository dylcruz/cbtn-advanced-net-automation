from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint
from tqdm import tqdm

nr = InitNornir('config.yaml')
ip_addresses = []

target_list = []
failed_list = []

def get_ip(task):
    result = task.run(task=send_command, command='show ip interface brief')
    task.host['facts'] = result.scrapli_response.genie_parse_output()
    interfaces = task.host['facts']['interface']
    for intf in interfaces:
        if intf == 'GigabitEthernet0/0':
            continue
        ip_addr = interfaces[intf]['ip_address']
        if ip_addr != 'unassigned':
            target_list.append(ip_addr)

def ping_test(task):
    for ip in tqdm(sorted(target_list), f'{task.host} - Ping Tests'):
        result = task.run(task=send_command, command=f'ping {ip}')
        response = result.result
        if not '!!!' in response:
            failed_list.append(f'{task.host} cannot ping {ip}')

print('Gathering IP addresses...')
nr.run(task=get_ip)
print('Starting ping tests...')
nr.run(task=ping_test)

print('\n\n\n\n\n\n')
if failed_list:
    for item in sorted(failed_list): rprint(item)
else:
    print('All pings succeeded.')
