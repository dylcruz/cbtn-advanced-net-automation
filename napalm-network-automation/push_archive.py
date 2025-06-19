from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

ios_devices = nr.filter(platform="ios")


def test(task):
    task.run(task=send_configs_from_file, file="napalm-startup.txt")


results = ios_devices.run(task=test)
print_result(results)
