import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')
euro_password= getpass.getpass(prompt='Enter the Euro Group password: ')
usa_password = getpass.getpass(prompt='Enter the USA Group password: ')

nr.inventory.groups['euro_group'].password = euro_password
nr.inventory.groups['usa_group'].password = usa_password

def credential_test(task):
    task.run(task=send_command, command='show ip interface brief')

results = nr.run(credential_test)
print_result(results)
