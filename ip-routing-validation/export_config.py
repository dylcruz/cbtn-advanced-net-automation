from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.tasks.files import write_file

nr = InitNornir('config.yaml')

cisco_filter = nr.filter(platform="ios")
junos_filter = nr.filter(platform="junos")

def get_cisco_config(task):
    results = task.run(task=send_command, command='show run')
    task.run(task=write_file, content=results.result, filename=f'configs/{task.host}-config.ios')

def get_junos_config(task):
    results = task.run(task=send_command, command='show configuration')
    task.run(task=write_file, content=results.result, filename=f'configs/{task.host}-config.junos')
    
cisco_filter.run(task=get_cisco_config)
junos_filter.run(task=get_junos_config)
