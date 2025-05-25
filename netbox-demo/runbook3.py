from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result
from tqdm import tqdm

nr = InitNornir(config_file='config.yaml')

def random_configs(task, pbar):
    if task.host.platform != 'ios':
        print('Unsupported OS')
        pbar.update()
    else:
        task.run(task=send_configs_from_file, file='conf.txt')
        pbar.update()

with tqdm(total=len(nr.inventory.hosts)) as pbar:
    results = nr.run(task=random_configs, pbar=pbar)
    print_result(results)
