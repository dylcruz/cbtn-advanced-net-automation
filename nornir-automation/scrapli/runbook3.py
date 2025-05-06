from nornir import InitNornir
from nornir_scrapli.tasks import send_commands_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file='config.yaml')

def send_command_file(task):
     task.run(task=send_commands_from_file, file='commands.txt')

result = nr.run(send_command_file)
print_result(result)
