from ncclient import manager
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir('config.yaml')

def configure_stuff(task):
    DEVICE = {
    "host": task.host.hostname,
    "port": 830,
    "username": task.host.username,
    "password": task.host.password,
    "hostkey_verify": False
    }
    template_to_load = task.run(task=template_file, template='ospf.j2', path='templates')
    configuration = template_to_load.result
    with manager.connect(**DEVICE) as m:
        response = m.edit_config(target='running', config=configuration)
        return response
    
results = nr.run(configure_stuff)
print_result(results)
