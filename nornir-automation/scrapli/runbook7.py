from nornir import InitNornir
from nornir_scrapli.tasks import send_interactive
from nornir_utils.plugins.functions import print_result
from datetime import datetime

time_now = datetime.now()
time_formatted = time_now.strftime("%Y_%m_%d_%H_%M_%S")

nr = InitNornir(config_file='config.yaml')

def commit_flash(task):
    cmds = [(f'copy run flash:BACKUP_{time_formatted}.bak', 'Destination filename'), ('\n',f'{task.host}#')]
    task.run(task=send_interactive, interact_events=cmds)

results = nr.run(commit_flash)
print_result(results)
