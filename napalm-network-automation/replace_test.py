from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def replace_stuff(task):
    if task.host.platform == "ios":
        filename = f"backup-directory/{task.host}-running.ios"
    elif task.host.platform == "junos":
        filename = f"backup-directory/{task.host}-running.junos"
    else:
        filename = f"backup-directory/{task.host}-running.cfg"

    task.run(task=napalm_configure, filename=filename, replace=True)


results = nr.run(task=replace_stuff)
print_result(results)
