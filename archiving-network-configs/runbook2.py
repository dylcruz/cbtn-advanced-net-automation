from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from datetime import date
import pathlib

nr = InitNornir(config_file='config.yaml')
cisco_devices = nr.filter(platform='ios')
junos_devices = nr.filter(platform='junos')

config_dir = 'config-backups'
date_dir = f'{config_dir}/{str(date.today())}'

def backup_configuration_cisco(task):
    cmds = ['show run', 'show version']
    for cmd in cmds:
        host_dir = f'{date_dir}/{task.host}'
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(host_dir).mkdir(exist_ok=True)
        results = task.run(task=send_command, command=cmd)
        task.run(task=write_file, 
                 content=results.result, 
                 filename=f'{host_dir}/{"-".join(cmd.split())}.ios')

def backup_configuration_junos(task):
    cmds = ['show configuration', 'show version']
    for cmd in cmds:
        host_dir = f'{date_dir}/{task.host}'
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(host_dir).mkdir(exist_ok=True)
        results = task.run(task=send_command, command=cmd)
        task.run(task=write_file,
                 content=results.result,
                 filename=f'{host_dir}/{"-".join(cmd.split())}.conf')

results = cisco_devices.run(task=backup_configuration_cisco)
print_result(results)
results = junos_devices.run(task=backup_configuration_junos)
print_result(results)
