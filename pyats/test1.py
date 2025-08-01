import json
from genie.testbed import load
from rich import print as rprint

testbed = load('testbed.yaml')

for name in testbed.devices.keys():
    dev = testbed.devices[name]
    dev.connect(log_stdout=False)
    interfaces = dev.parse('show interfaces')
    pretty_interfaces = json.dumps(interfaces, indent=2)
    rprint(f'{name}\n{pretty_interfaces}\n\n')
