from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def pull_structured_data(task):
    cdp_result = task.run(task=send_command, command='show cdp neighbor')
    task.host['facts'] = cdp_result.scrapli_response.genie_parse_output()
    cdp_index = task.host['facts']['cdp']['index']

    for device in cdp_index.values():
        local_interface = device['local_interface']
        remote_interface = device['port_id']
        remote_device = device['device_id']

        config_commands = [f'interface {local_interface}', f'description Connected to {remote_device} via its {remote_interface}']
        task.run(task=send_configs, configs=config_commands)


results = nr.run(pull_structured_data)
print_result(results)
